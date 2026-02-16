from django.conf import settings
from django.http.request import HttpRequest


def admin_settings(request: HttpRequest) -> dict[str, str | bool | None]:
    show_version = request.user.is_staff  # pyright: ignore

    return {
        "show_environment": getattr(settings, "ENVIRONMENT_SHOWN_IN_ADMIN", None),
        "show_version": show_version,
        "git_sha": getattr(settings, "GIT_SHA", None),
        "version": getattr(settings, "RELEASE", None),
        "environment": getattr(settings, "ENVIRONMENT", None),
    }
