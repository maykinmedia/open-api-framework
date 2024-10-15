from django.contrib.sessions.models import Session
from django.urls import reverse

import pytest
from pytest_django.fixtures import admin_user
from sessionprofile.models import SessionProfile

from .factories import SessionProfileFactory


@pytest.fixture
def session_changelist_url():
    return reverse("admin:sessionprofile_sessionprofile_changelist")


def test_session_profile_sanity(client, admin_user, session_changelist_url):

    client.force_login(admin_user)
    response = client.get(session_changelist_url)
    assert response.status_code == 200

    assert SessionProfile.objects.count() == 1

    session = SessionProfile.objects.get()
    assert client.session.session_key == session.session_key


admin_user2 = admin_user


def test_only_session_profile_of_user_shown(
    client, admin_user, django_user_model, session_changelist_url
):

    other_admin = django_user_model.objects.create_superuser("garry")

    client.force_login(other_admin)
    response = client.get(session_changelist_url)
    assert response.status_code == 200

    client.force_login(admin_user)
    response = client.get(session_changelist_url)
    assert response.status_code == 200

    # two sessions, one for each user
    assert SessionProfile.objects.count() == 2

    # Session created after response, needs to be called again
    response = client.get(session_changelist_url)

    admin_user_session = SessionProfile.objects.get(user=admin_user)
    assert admin_user_session.session_key in response.content.decode()

    other_user_session = SessionProfile.objects.get(user=other_admin)
    assert other_user_session.session_key not in response.content.decode()


def test_delete_with_session_db_backend(
    client, admin_user, session_changelist_url, db_session_store
):
    client.force_login(admin_user)

    session = SessionProfileFactory(user=admin_user)

    assert SessionProfile.objects.count() == 1
    # sesison created by login
    assert Session.objects.count() == 2
    assert db_session_store().exists(session.session_key)

    url = reverse("admin:sessionprofile_sessionprofile_delete", args=[session.pk])

    response = client.post(url, {"post": "yes"})
    assert response.status_code == 302

    # new session saved upon request
    assert SessionProfile.objects.count() == 1
    assert SessionProfile.objects.count() != session
    assert Session.objects.count() == 1
    assert not db_session_store().exists(session.session_key)


def test_delete_with_session_cache_backend(
    client, admin_user, session_changelist_url, cache_session_store
):
    client.force_login(admin_user)

    session = SessionProfileFactory(user=admin_user)

    assert SessionProfile.objects.count() == 1
    assert Session.objects.count() == 0
    assert cache_session_store().exists(session.session_key)

    url = reverse("admin:sessionprofile_sessionprofile_delete", args=[session.pk])

    response = client.post(url, {"post": "yes"})
    assert response.status_code == 302

    # new session saved upon request
    assert SessionProfile.objects.count() == 1
    assert SessionProfile.objects.count() != session
    assert Session.objects.count() == 0
    assert not cache_session_store().exists(session.session_key)


def test_delete_action_with_session_db_backend(
    client, admin_user, session_changelist_url, db_session_store
):
    client.force_login(admin_user)
    sessions = SessionProfileFactory.create_batch(5, user=admin_user)

    # one created from user login
    assert Session.objects.count() == 6
    assert SessionProfile.objects.count() == 5

    session_keys = [session.session_key for session in sessions]
    for session_key in session_keys:
        assert db_session_store().exists(session_key)

    response = client.post(
        session_changelist_url,
        {"action": "delete_selected", "_selected_action": session_keys, "post": "yes"},
    )
    assert response.status_code == 302

    # one is created as the post request is sent
    assert SessionProfile.objects.count() == 1
    assert Session.objects.count() == 1

    for session_key in session_keys:
        assert not db_session_store().exists(session_key)


def test_delete_action_with_session_cache_backend(
    client, admin_user, session_changelist_url, cache_session_store
):

    client.force_login(admin_user)
    sessions = SessionProfileFactory.create_batch(5, user=admin_user)

    # no db sessions are created
    assert Session.objects.count() == 0
    assert SessionProfile.objects.count() == 5

    session_keys = [session.session_key for session in sessions]

    # sessions are created
    for session_key in session_keys:
        assert cache_session_store().exists(session_key)

    response = client.post(
        session_changelist_url,
        {"action": "delete_selected", "_selected_action": session_keys, "post": "yes"},
    )
    assert response.status_code == 302

    # one is created as the post request is sent
    assert SessionProfile.objects.count() == 1
    assert Session.objects.count() == 0

    # sessions should be deleted
    for session_key in session_keys:
        assert not cache_session_store().exists(session_key)
