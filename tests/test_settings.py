def test_sentry_settings():
    """
    test that sentry settings are initialized
    """
    from django.conf import settings

    assert "SENTRY_DSN" in settings
