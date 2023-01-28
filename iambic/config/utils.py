from __future__ import annotations

import asyncio
import os
import pathlib

from git import Repo

from iambic.config.models import Config
from iambic.core.git import clone_git_repos, get_origin_head
from iambic.core.utils import gather_templates, yaml


async def resolve_config_template_path(repo_dir: str) -> pathlib.Path:
    config_template_file_path = await gather_templates(repo_dir, "Core::Config")
    if len(config_template_file_path) == 0:
        raise RuntimeError(
            f"Unable to discover Iambic Configuration in {repo_dir}. "
            "Please create a configuration with the `NOQ::Core::Config` template type."
        )
    if len(config_template_file_path) > 1:
        raise RuntimeError(
            f"Too many NOQ::Core::Config templates discovered. Found ({len(config_template_file_path)}). Expected 1. Files: {','.join(config_template_file_path)}"
        )
    # Currently NOQ supports 1 configuration per repo
    return pathlib.Path(config_template_file_path[0])


async def load_template(repo_dir: str, plugins_configured: bool = False) -> Config:
    repo = Repo(repo_dir)
    previous_head = repo.head
    main_branch = get_origin_head(repo)
    if previous_head != main_branch:
        repo.git.checkout(main_branch)
    config_template_file_path = await resolve_config_template_path(repo_dir)
    c = Config(
        file_path=str(config_template_file_path),
        **yaml.load(open(str(config_template_file_path))),
    )
    repo.git.checkout(previous_head)
    if plugins_configured:
        c.configure_plugins()
    return c


async def store_template(config: Config, repo_dir: str, repo_name: str):
    # clone_git_repos will pull if repos exist versus cloning
    repo_path = pathlib.Path(repo_dir)
    config_path = repo_path / "config" / "config.yml"
    repo_base_path = repo_path.parent
    if not config.secrets:
        raise ValueError("No secrets configured")
    if repo_path.name not in [
        x.get("name") for x in config.secrets.get("git", {}).get("repositories", [])
    ]:
        raise ValueError(
            f"Invalidly formed configuration; expect config.secrets.git.repositories to have {repo_path.name}"
        )
    repos = await clone_git_repos(config, repo_base_path)
    if repos is None:
        raise RuntimeError(f"Unable to clone {repo_path}")
    os.makedirs(config_path.parent, exist_ok=True)
    repo = repos.get(repo_name)
    if not repo:
        raise RuntimeError(f"Cannot find {repo_name} in repos: {list(repos.keys())}")
    previous_head = repo.head
    main_branch = get_origin_head(repo)
    if previous_head != main_branch:
        repo.git.checkout(main_branch)
    config_template_file_path = config_path
    with open(config_template_file_path, "w") as fp:
        yaml.dump(config.dict(), fp)
    # TODO: Setup a PR request
    repo.git.checkout(previous_head)


async def multi_config_loader(config_paths: list[str]) -> list[Config]:
    """Load multiple config files into a list of Config objects."""
    configs = []
    for config_path in config_paths:
        config = Config.load(config_path)
        configs.append(config)

    await asyncio.gather(*[config.setup_aws_accounts() for config in configs])

    identity_center_detail_set_tasks = []
    for config in configs:
        if config.aws and config.aws.accounts:
            identity_center_detail_set_tasks.extend(
                [
                    account.set_identity_center_details()
                    for account in config.aws.accounts
                ]
            )
    await asyncio.gather(*identity_center_detail_set_tasks)

    return configs