from importlib import import_module

from django.conf import settings as django_settings

import pytest


@pytest.fixture
def cache_session_store(settings):
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    return import_module(django_settings.SESSION_ENGINE).SessionStore


@pytest.fixture
def db_session_store(settings):
    settings.SESSION_ENGINE = "django.contrib.sessions.backends.db"
    return import_module(django_settings.SESSION_ENGINE).SessionStore
