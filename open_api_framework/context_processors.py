from django.conf import settings
from django.http.request import HttpRequest


def admin_settings(request: HttpRequest) -> dict:
    resolver = request.resolver_match
    show_version = False

    if resolver:
        if resolver.app_name:
            url_name = f"{resolver.app_name}:{resolver.url_name}"
        else:
            url_name = resolver.url_name

        # Note that only views that use the open-api-framework's
        # `base_site.html` template are listed here
        excluded_version_urls = [
            "admin_password_reset",
            "password_reset_done",
        ]

        show_version = bool(url_name not in excluded_version_urls)

    return {
        "show_environment": getattr(settings, "ENVIRONMENT_SHOWN_IN_ADMIN", None),
        "show_version": show_version,
        "git_sha": getattr(settings, "GIT_SHA", None),
        "version": getattr(settings, "RELEASE", None),
        "environment": getattr(settings, "ENVIRONMENT", None),
    }
