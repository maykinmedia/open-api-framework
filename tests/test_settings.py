import importlib
from importlib.util import find_spec
from unittest import TestCase

from django.conf import settings
from django.urls import reverse

import pytest
from django_webtest import WebTest


@pytest.mark.skipif(not find_spec("sentry_sdk"), reason="No sentry installed")
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


class TestLoggingConfiguration(TestCase):
    def test_notifications_api_common_logger_is_configured(self):
        module = importlib.import_module("open_api_framework.conf.base")

        self.assertIn(
            "notifications_api_common",
            module.LOGGING["loggers"],
        )
