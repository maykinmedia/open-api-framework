from django.conf import settings
from django.http import HttpResponse
from django.test import Client
from django.urls import path, reverse

import csp.constants
from django_webtest import WebTest


def test_sentry_settings():
    """
    test that sentry settings are initialized
    """

    assert hasattr(settings, "SENTRY_CONFIG") is True
    assert hasattr(settings, "SENTRY_DSN") is True


class RosettaTests(WebTest):
    def test_rosetta_redirect_fails_with_lazy_login_url(self):
        response = self.app.get("/admin/rosetta/files/project/")

        expected_login_url = (
            reverse(settings.LOGIN_URL) + "?next=/admin/rosetta/files/project/"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, expected_login_url)


def dummy_view(request):
    return HttpResponse("OK")


urlpatterns = [
    path("dummy/", dummy_view),
]


def test_csp_default(settings):
    settings.MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "csp.middleware.CSPMiddleware",
    ]
    settings.ROOT_URLCONF = __name__

    settings.CONTENT_SECURITY_POLICY = {
        "DIRECTIVES": {
            "default-src": ["'self'"],
            "script-src": ["'self'", csp.constants.NONCE, "'unsafe-inline'"],
            "style-src": ["'self'", csp.constants.NONCE, "'unsafe-inline'"],
            "img-src": ["'self'", "data:"],
            "connect-src": ["'self'"],
            "object-src": ["'none'"],
            "form-action": ["'self'"],
        },
        "REPORT_PERCENTAGE": 100,
    }

    client = Client()
    response = client.get("/dummy/")
    csp_header = response.headers.get("Content-Security-Policy")
    assert csp_header is not None
    assert "default-src 'self'" in csp_header
    assert "object-src 'none'" in csp_header
    assert "form-action 'self'" in csp_header


def test_csp_with_report_uri(settings):
    settings.MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "csp.middleware.CSPMiddleware",
    ]
    settings.ROOT_URLCONF = __name__

    settings.CONTENT_SECURITY_POLICY = {
        "DIRECTIVES": {
            "default-src": ["'self'"],
            "script-src": ["'self'", csp.constants.NONCE],
            "style-src": ["'self'"],
            "report-uri": ["https://example.com/csp-report"],
        },
        "REPORT_PERCENTAGE": 100,
    }

    client = Client()
    response = client.get("/dummy/")
    csp_header = response.headers.get("Content-Security-Policy")
    assert csp_header is not None
    assert "default-src 'self'" in csp_header
    assert "script-src 'self'" in csp_header
    assert "style-src 'self'" in csp_header
    assert "report-uri https://example.com/csp-report" in csp_header
