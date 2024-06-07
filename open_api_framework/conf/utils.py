import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

from decouple import Csv, Undefined, config as _config, undefined
from sentry_sdk.integrations import DidNotEnable, django, redis


@dataclass
class EnvironmentVariable:
    name: str
    default: Any
    help_text: str
    group: Optional[str] = None

    def __post_init__(self):
        if not self.group:
            self.group = (
                "Required" if isinstance(self.default, Undefined) else "Optional"
            )

    def __eq__(self, other):
        return isinstance(other, EnvironmentVariable) and self.name == other.name


ENVVAR_REGISTRY = []


def config(
    option: str,
    default: Any = undefined,
    help_text="",
    group=None,
    add_to_docs=True,
    *args,
    **kwargs,
):
    """
    Pull a config parameter from the environment.

    Read the config variable ``option``. If it's optional, use the ``default`` value.
    Input is automatically cast to the correct type, where the type is derived from the
    default value if possible.

    Pass ``split=True`` to split the comma-separated input into a list.
    """
    if add_to_docs:
        variable = EnvironmentVariable(
            name=option, default=default, help_text=help_text, group=group
        )
        if variable not in ENVVAR_REGISTRY:
            ENVVAR_REGISTRY.append(variable)

    if "split" in kwargs:
        kwargs.pop("split")
        kwargs["cast"] = Csv()
        if isinstance(default, list):
            default = ",".join(default)

    if default is not undefined and default is not None:
        kwargs.setdefault("cast", type(default))
    return _config(option, default=default, *args, **kwargs)


def get_sentry_integrations() -> list:
    """
    Determine which Sentry SDK integrations to enable.
    """
    default = [
        django.DjangoIntegration(),
        redis.RedisIntegration(),
    ]
    extra = []

    try:
        from sentry_sdk.integrations import celery
    except DidNotEnable:  # happens if the celery import fails by the integration
        pass
    else:
        extra.append(celery.CeleryIntegration())

    return [*default, *extra]


def strip_protocol_from_origin(origin: str) -> str:
    parsed = urlparse(origin)
    return parsed.netloc


def get_project_dirname() -> str:
    return config("DJANGO_SETTINGS_MODULE", add_to_docs=False).split(".")[0]


def get_django_project_dir() -> str:
    # Get the path of the importing module
    base_dirname = get_project_dirname()
    return Path(sys.modules[base_dirname].__file__).parent
