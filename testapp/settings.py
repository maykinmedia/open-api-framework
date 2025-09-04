from pathlib import Path

from maykin_common.config import DocumentationParams, config

from open_api_framework.conf.base import *  # noqa: F403

BASE_DIR = Path(__file__).resolve(strict=True).parent

# base configures logging to (their) BASE_DIR / "log"
# relative testapp location is too different from default-project
del LOGGING  # noqa: F821

with suppress(NameError):
    # base configures redis if package is installed
    # CI doens't spinup a redis instance
    del CACHES  # noqa: F821

SECRET_KEY = config(
    "SECRET_KEY",
    default="so-secret-i-cant-believe-you-are-looking-at-this",
    documentation=DocumentationParams(
        group="Required",
        help_text=("Secret key that's used for certain cryptographic utilities."),
    ),
)
DEBUG = config(
    "DEBUG",
    default=False,
    documentation=DocumentationParams(
        help_text=(
            "Only set this to ``True`` on a local development environment. "
            "Various other security settings are derived from this setting!"
        )
    ),
)
IS_HTTPS = config(
    "IS_HTTPS",
    default=not DEBUG,
    documentation=DocumentationParams(
        help_text=(
            "Used to construct absolute URLs and controls a variety of security settings. "
            "Defaults to the inverse of ``DEBUG``."
        ),
        auto_display_default=False,
    ),
)
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

# These are excluded from generate_envvar_docs test by their group
VARIABLE_TO_BE_EXCLUDED = config(
    "VARIABLE_TO_BE_EXCLUDED1",
    default="foo",
    documentation=DocumentationParams(group="Excluded"),
)
VARIABLE_TO_BE_EXCLUDED = config(
    "VARIABLE_TO_BE_EXCLUDED2",
    default="bar",
    documentation=DocumentationParams(group="Excluded"),
)

SESSION_ENGINE = "django.contrib.sessions.backends.db"
