import warnings
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.template import loader

from open_api_framework.conf.utils import EnvironmentVariable


def convert_group_to_rst(variables: set[EnvironmentVariable]) -> str:
    template = loader.get_template("open_api_framework/env_config.rst")
    grouped_vars = defaultdict(list)
    for var in variables:
        if not var.help_text:
            warnings.warn(f"missing help_text for environment variable {var}")
        grouped_vars[var.group].append(var)
    return template.render({"vars": grouped_vars.items()})


class Command(BaseCommand):
    help = "Generate documentation for all used envvars"

    def handle(self, *args, **options):
        from open_api_framework.conf.utils import ENVVAR_REGISTRY

        with open("docs/env_config.rst", "w") as f:
            f.write(convert_group_to_rst(ENVVAR_REGISTRY))
