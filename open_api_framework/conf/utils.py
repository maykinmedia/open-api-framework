import logging  # noqa: TID251
import sys
from importlib.util import find_spec
from pathlib import Path
from urllib.parse import urlparse

from maykin_common.config import config
from sentry_sdk.integrations import DidNotEnable, Integration, django, redis
from sentry_sdk.integrations.logging import LoggingIntegration


def is_installed(module_name: str) -> bool:
    """
    Return a boolean to indicate if a module is installed or not
    """
    return bool(find_spec(module_name))


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
