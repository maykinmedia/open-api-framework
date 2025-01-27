from importlib import import_module

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase
from django.utils.module_loading import import_string


def get_session_store() -> SessionBase:
    return import_module(settings.SESSION_ENGINE).SessionStore


def get_configuraton_step_context(step_path: str) -> dict:
    step = import_string(step_path)

    context = {
        "step_title": step_path.split(".")[-1],
        "step_description": step.verbose_name,
        "step_path": step_path,
    }
    return context
