from django.conf import settings


def project(request):
    settings = (
        "ENVIRONMENT_SHOWN_IN_ADMIN",
        "RELEASE",
        "GIT_SHA",
    )

    return {"project": {k: getattr(settings, k, None) for k in settings}}
