from __future__ import annotations

import os
from typing import TYPE_CHECKING

from iambic.plugins.v0_1_0.okta.app.models import get_app_template
from iambic.plugins.v0_1_0.okta.app.utils import list_all_apps

if TYPE_CHECKING:
    from iambic.plugins.v0_1_0.okta.iambic_plugin import OktaConfig, OktaOrganization


async def generate_app_templates(
    config: OktaConfig, output_dir: str, okta_organization: OktaOrganization
):
    """List all apps in the domain, along with members and
    settings"""

    apps = await list_all_apps(okta_organization)

    base_path = os.path.expanduser(output_dir)
    for okta_app in apps:
        # TODO: Make sure we don't overwrite expiration on import
        app = await get_app_template(okta_app)
        file_path = os.path.expanduser(app.file_path)
        app.file_path = os.path.join(base_path, file_path)
        app.write()
    return apps