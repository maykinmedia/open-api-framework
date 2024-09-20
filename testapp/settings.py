from pathlib import Path

from open_api_framework.conf.utils import config

BASE_DIR = Path(__file__).resolve(strict=True).parent

SECRET_KEY = config(
    "SECRET_KEY",
    "so-secret-i-cant-believe-you-are-looking-at-this",
    group="Required",
    help_text=("Secret key that's used for certain cryptographic utilities."),
)
DEBUG = config(
    "DEBUG",
    default=False,
    help_text=(
        "Only set this to ``True`` on a local development environment. "
        "Various other security settings are derived from this setting!"
    ),
)
IS_HTTPS = config(
    "IS_HTTPS",
    default=not DEBUG,
    help_text=(
        "Used to construct absolute URLs and controls a variety of security settings. "
        "Defaults to the inverse of ``DEBUG``."
    ),
    auto_display_default=False,
)

USE_TZ = config("USE_TZ", True, add_to_docs=False)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "open_api_framework.db",
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.admin",
    "open_api_framework",
    "sessionprofile",
    "testapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "sessionprofile.middleware.SessionProfileMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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

# These are excluded from generate_envvar_docs test by their group
VARIABLE_TO_BE_EXCLUDED = config("VARIABLE_TO_BE_EXCLUDED1", "foo", group="Excluded")
VARIABLE_TO_BE_EXCLUDED = config("VARIABLE_TO_BE_EXCLUDED2", "bar", group="Excluded")
