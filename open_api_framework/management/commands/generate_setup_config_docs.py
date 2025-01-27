from django.conf import settings
from django.core.management.base import BaseCommand
from django.template import loader

from open_api_framework.utils import get_configuraton_step_context


def render_step_info(step_name: str) -> str:
    template = loader.get_template(
        "open_api_framework/components/setup_config_step.rst"
    )

    context = get_configuraton_step_context(step_name)
    return template.render(context)


def convert_setup_configuration_steps_to_rst(
    project_name: str, config_steps: list[str]
) -> str:
    template = loader.get_template("open_api_framework/setup_configuration.rst")
    return template.render(
        {"project_name": project_name, "setup_configuraiton_steps": config_steps}
    )


class Command(BaseCommand):
    help = "Generate documentation for all used envvars"

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--file",
            help="Name and path of the file to which the documentation will be written.",
            nargs="?",
            default="docs/setup_configuration.rst",
        )

    def handle(self, *args, **options):
        file_path = options["file"]

        configuration_steps = getattr(settings, "SETUP_CONFIGURATION_STEPS", [])

        project_name = getattr(settings, "PROJECT_NAME", settings.PROJECT_DIRNAME)

        with open(file_path, "w") as f:
            f.write(
                convert_setup_configuration_steps_to_rst(
                    project_name, configuration_steps
                )
            )
