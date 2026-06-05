from pathlib import Path

from maykin_common.config import config

from open_api_framework.conf.base import *  # noqa: F403

BASE_DIR = Path(__file__).resolve(strict=True).parent

# base configures logging to (their) BASE_DIR / "log"
# relative testapp location is too different from default-project
del LOGGING  # noqa: F821

with suppress(NameError):
    # base configures redis if package is installed
    # CI doens't spinup a redis instance
    del CACHES  # noqa: F821

STATIC_URL = "/static/"
LOGIN_URL = "admin:login"

USE_TZ = config("USE_TZ", default=True, documentation=no_doc)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "open_api_framework.db",
    }
}

INSTALLED_APPS += ["rosetta"]
dont_work_with_sqlite = ["mozilla_django_oidc_db", "notifications_api_common"]
for app in dont_work_with_sqlite:
    if app in INSTALLED_APPS:
        INSTALLED_APPS.pop(INSTALLED_APPS.index(app))


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "testapp.urls"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "privates": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": os.path.join(BASE_DIR, "private-media"),
            "base_url": "/private-media/",
        },
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"
