from django.conf import settings


def project(request):
    django_settings = (
        "ENVIRONMENT_SHOWN_IN_ADMIN",
        "RELEASE",
        "GIT_SHA",
    )

    return {"project": {k: getattr(settings, k, None) for k in django_settings}}
