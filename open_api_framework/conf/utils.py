import logging  # noqa: TID251
import os
import sys
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path
from typing import Any, Optional, TypeVar, assert_never
from urllib.parse import urlparse
from warnings import warn

from decouple import Csv, Undefined, config as _config, undefined
from sentry_sdk.integrations import DidNotEnable, Integration, django, redis
from sentry_sdk.integrations.logging import LoggingIntegration


@dataclass
class EnvironmentVariable:
    name: str
    default: Any
    help_text: str
    group: Optional[str] = None
    auto_display_default: bool = True

    def __post_init__(self):
        if not self.group:
            self.group = (
                "Required" if isinstance(self.default, Undefined) else "Optional"
            )

    def __eq__(self, other):
        return isinstance(other, EnvironmentVariable) and self.name == other.name


ENVVAR_REGISTRY: list[EnvironmentVariable] = []

_T = TypeVar("_T")


def config(
    option: str,
    default: _T = undefined,
    help_text: str = "",
    group: str | None = None,
    add_to_docs: str | bool = True,
    auto_display_default: bool = True,
    *args,
    **kwargs,
) -> _T:
    """
    An override of ``decouple.config``, with custom options to construct documentation
    for environment variables.

    Pull a config parameter from the environment.

    Read the config variable ``option``. If it's optional, use the ``default`` value.
    Input is automatically cast to the correct type, where the type is derived from the
    default value if possible.

    Pass ``split=True`` to split the comma-separated input into a list.

    Additionally, the variable is added to a registry that is used to construct documentation
    via the ``generate_envvar_docs`` management command. The following arguments are added for this:

    :param help_text: The help text to be displayed for this variable in the documentation. Default `""`
    :param group: The name of the section under which this variable will be grouped. Default ``None``
    :param add_to_docs: Whether or not this variable will be displayed in the documentation. Default ``True``
                        If a string is passed, it will only be displayed if it is importable as a module,
                        and will raise a Warning when it is still passed in from the environment.
    :param auto_display_default: Whether or not the passed ``default`` value is displayed in the docs, this can be
        set to ``False`` in case a default needs more explanation that can be added to the ``help_text``
        (e.g. if it is computed or based on another variable). Default ``True``
    """
    variable = EnvironmentVariable(
        name=option,
        default=default,
        help_text=help_text,
        group=group,
        auto_display_default=auto_display_default,
    )

    def document():
        if variable not in ENVVAR_REGISTRY:
            ENVVAR_REGISTRY.append(variable)
        else:
            # If the same variable is defined again (i.e. because a project defines a custom default), override it
            ENVVAR_REGISTRY[ENVVAR_REGISTRY.index(variable)] = variable

    if "split" in kwargs:
        kwargs.pop("split")
        kwargs["cast"] = Csv()
        if isinstance(default, list):
            default = ",".join(default)

    if default is not undefined and default is not None:
        kwargs.setdefault("cast", type(default))

    match add_to_docs:
        case str(module) if find_spec(module):
            document()
        case str(module):
            # not installed
            if option in os.environ:
                warn(
                    f"{variable.name} found, but required {add_to_docs} is not installed",
                    RuntimeWarning,
                )
            if default is undefined:
                return default  # don't call _config it will require variable.name!
        case True:
            document()
        case False:
            pass
        case _:
            assert_never(add_to_docs)

    return _config(option, default=default, *args, **kwargs)  # type: ignore


def importable(*items: str) -> list[str]:
    "Return the dotted paths that start from an installed package"

    split_items = (item.split(".") for item in items)
    return [".".join(item) for item in split_items if find_spec(item[0])]


def get_sentry_integrations() -> list[Integration]:
    """
    Determine which Sentry SDK integrations to enable.
    """
    extra = []

    if find_spec("redis"):  # does not raise DidNotEnable if redis is not installed
        extra.append(redis.RedisIntegration())

    try:
        from sentry_sdk.integrations import celery
    except DidNotEnable:  # happens if the celery import fails by the integration
        pass
    else:
        extra.append(celery.CeleryIntegration())

    if find_spec("structlog"):
        extra.append(
            LoggingIntegration(
                level=logging.INFO,  # breadcrumbs
                # do not send any logs as event to Sentry at all - these must be scraped by
                # the (container) infrastructure instead.
                event_level=None,
            ),
        )

    return [django.DjangoIntegration(), *extra]


def strip_protocol_from_origin(origin: str) -> str:
    parsed = urlparse(origin)
    return parsed.netloc


def get_project_dirname() -> str:
    return config("DJANGO_SETTINGS_MODULE", add_to_docs=False).split(".")[0]  # pyright: ignore


def get_django_project_dir() -> Path:
    # Get the path of the importing module
    base_dirname = get_project_dirname()
    return Path(sys.modules[base_dirname].__file__).parent  # pyright: ignore[reportArgumentType]


def mute_logging(config: dict) -> None:  # pragma: no cover
    """
    Disable (console) output from logging.
    :arg config: The logging config, typically the django LOGGING setting.
    """

    # set up the null handler for all loggers so that nothing gets emitted
    for name, logger in config["loggers"].items():
        if name == "flaky_tests":
            continue
        logger["handlers"] = ["null"]

    # some tooling logs to a logger which isn't defined, and that ends up in the root
    # logger -> add one so that we can mute that output too.
    config["loggers"].update(
        {
            "": {"handlers": ["null"], "level": "CRITICAL", "propagate": False},
        }
    )
