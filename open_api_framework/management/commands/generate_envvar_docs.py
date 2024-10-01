import warnings
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader
from django.utils.module_loading import import_string

from django_setup_configuration.management.commands.generate_config_docs import (
    ConfigDocBase,
)

from open_api_framework.conf.utils import EnvironmentVariable


def convert_variables_to_rst(variables: list[EnvironmentVariable]) -> str:
    template = loader.get_template("open_api_framework/env_config.rst")
    grouped_vars = defaultdict(lambda: defaultdict(list))
    for var in variables:
        if not var.help_text:
            warnings.warn(f"missing help_text for environment variable {var}")
        grouped_vars[var.group][var.sub_group].append(var)

    vars = []
    for group, group_vars in grouped_vars.items():
        vars.append((group, group_vars.items()))
    return template.render({"vars": vars})


class Command(ConfigDocBase, BaseCommand):
    help = "Generate documentation for all used envvars"

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--envvar-file",
            help="Name and path of the file to which the envvar documentation will be written.",
            nargs="?",
            default="docs/env_config.rst",
        )
        parser.add_argument(
            "--config-file",
            help="Name and path of the file to which the setup configuration documentation will be written.",
            nargs="?",
            default="docs/setup_config.rst",
        )
        parser.add_argument(
            "--exclude-group",
            help="Names of groups that should not be excluded in the generated docs.",
            action="append",
        )

    def handle(self, *args, **options):
        self.generate_regular_config_docs(*args, **options)
        self.generate_setup_config_docs(*args, **options)

    def generate_regular_config_docs(self, *args, **options):
        from open_api_framework.conf.utils import ENVVAR_REGISTRY

        file_path = options["envvar_file"]
        exclude_groups = options["exclude_group"] or []

        def _sort(envvar):
            match envvar.group:
                case "Required":
                    return 0
                case "Optional":
                    return 2
                case _:
                    return 1

        sorted_registry = sorted(
            [var for var in ENVVAR_REGISTRY if var.group not in exclude_groups],
            key=_sort,
        )
        with open(file_path, "w") as f:
            f.write(convert_variables_to_rst(sorted_registry))

    def generate_setup_config_docs(self, *args, **options) -> None:
        full_rendered_content = ""

        file_path = options["config_file"]
        if not hasattr(settings, "SETUP_CONFIGURATION_STEPS"):
            return

        for config_string in settings.SETUP_CONFIGURATION_STEPS:
            config_step = import_string(config_string)

            config_settings = getattr(config_step, "config_settings", None)
            if not config_settings or not config_settings.independent:
                continue

            rendered_content = self.render_doc(config_settings, config_step)
            full_rendered_content += rendered_content

        if len(full_rendered_content) > 0:
            with open(file_path, "w") as f:
                f.write(full_rendered_content)
