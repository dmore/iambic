from noq_form.config.templates import TEMPLATE_TYPE_MAP
from noq_form.core.models import NoqTemplate
from noq_form.core.utils import yaml


def load_templates(template_paths: list[str]) -> list[NoqTemplate]:
    templates = []

    for template_path in template_paths:
        template_dict = yaml.load(open(template_path))
        template_cls = TEMPLATE_TYPE_MAP[template_dict["template_type"]]
        templates.append(template_cls(file_path=template_path, **template_dict))

    return templates
