import warnings
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader
from django.utils.module_loading import import_string

from django_setup_configuration.config_settings import ConfigSettings
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


class SetupConfigDocs(ConfigDocBase):

    def generate_config_file(self) -> str:

        full_rendered_content = ""

        if not hasattr(settings, "SETUP_CONFIGURATION_STEPS"):
            return full_rendered_content

        for config_string in settings.SETUP_CONFIGURATION_STEPS:
            config_step = import_string(config_string)

            config_settings = getattr(config_step, "config_settings", None)
            if not config_settings or not config_settings.independent:
                continue

            rendered_content = self.render_doc(config_settings, config_step)
            full_rendered_content += rendered_content

        template = loader.get_template("open_api_framework/setup_config.rst")
        rendered = template.render(
            {"rendered_configuration_steps": full_rendered_content}
        )

        return rendered

    def render_doc(self, config_settings, config_step) -> str:
        """
        Render a `ConfigSettings` documentation template with the following variables:
            1. enable_setting
            2. required_settings
            3. optional_settings
            4. detailed_info
            5. title
        """
        # 1.
        enable_setting = getattr(config_settings, "enable_setting", None)

        # 2.
        required_settings = [
            name for name in getattr(config_settings, "required_settings", [])
        ]

        # additional settings from related configuration steps to embed
        # the documentation of several steps into one
        related_config_settings = [
            config for config in getattr(config_settings, "related_config_settings", [])
        ]
        required_settings_related = self.extract_unique_settings(
            [config.required_settings for config in related_config_settings]
        )
        # optional_settings_related = self.extract_unique_settings(
        #     [config.optional_settings for config in related_config_settings]
        # )

        required_settings.extend(required_settings_related)
        required_settings.sort()

        optional_settings = config_settings.optional_settings
        optional_settings.sort()

        # 4.
        detailed_info = self.get_detailed_info(
            config_settings,
            related_config_settings,
        )

        # 5.
        title = self.format_display_name(config_step.verbose_name)

        template_variables = {
            "enable_setting": enable_setting,
            "required_settings": required_settings,
            "optional_settings": optional_settings,
            "detailed_info": detailed_info,
            "title": title,
        }

        template = loader.get_template(
            "open_api_framework/components/setup_config_step.rst"
        )
        rendered = template.render(template_variables)

        return rendered

    def format_display_name(self, display_name: str) -> str:
        """Underlines title with '=' to display as heading in rst file"""

        heading_bar = "-" * len(display_name)
        display_name_formatted = f"{display_name}\n{heading_bar}"
        return display_name_formatted

    def get_detailed_info(
        self,
        config_settings: ConfigSettings,
        related_config_settings: list[ConfigSettings],
    ) -> dict[dict[str]]:
        """
        Get information about the configuration settings:
            1. from model fields associated with the `ConfigSettings`
            2. from information provided manually in the `ConfigSettings`
            3. from information provided manually in the `ConfigSettings` of related
               configuration steps
        """
        result = dict()
        for field in config_settings.config_fields:
            part = dict()
            variable = config_settings.get_config_variable(field.name)
            part["setting"] = field.verbose_name
            part["description"] = field.description or "No description"
            part["possible_values"] = field.field_description
            part["default_value"] = field.default_value

            result[variable] = part

        self.add_additional_info(config_settings, result)
        for config_settings in related_config_settings:
            self.add_additional_info(config_settings, result)

        return result

    @staticmethod
    def add_additional_info(
        config_settings: ConfigSettings, result: dict[dict[str]]
    ) -> None:
        """Convenience/helper function to retrieve additional documentation info"""

        additional_info = config_settings.additional_info

        for key, value in additional_info.items():
            result[key] = value


class Command(BaseCommand):
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

    @staticmethod
    def generate_regular_config_docs(*args, **options):
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

    @staticmethod
    def generate_setup_config_docs(*args, **options) -> None:

        file_path = options["config_file"]
        doc_generator = SetupConfigDocs()

        full_rendered_content = doc_generator.generate_config_file()

        if len(full_rendered_content) > 0:
            with open(file_path, "w") as f:
                f.write(full_rendered_content)
