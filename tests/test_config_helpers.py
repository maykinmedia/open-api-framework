import itertools as it
import os

import pytest

from open_api_framework.conf.utils import (
    ENVVAR_REGISTRY,
    config,
    get_django_project_dir,
    undefined,
)


def test_empty_list_as_default():
    value = config("SOME_TEST_ENVVAR", split=True, default=[], add_to_docs=False)

    assert value == []


def test_non_empty_list_as_default():
    value = config("SOME_TEST_ENVVAR", split=True, default=["foo"], add_to_docs=False)

    assert value == ["foo"]


def test_string_list_from_env(monkeypatch):
    monkeypatch.setenv("SOME_TEST_ENVVAR", "foo,bar")

    value = config("SOME_TEST_ENVVAR", split=True, default=["foo"], add_to_docs=False)

    assert value == ["foo", "bar"]


def test_it_raises_warning_if_add_to_docs_module_is_not_present(monkeypatch):
    monkeypatch.setenv("FOO_TEST_ENVVAR", "value")
    with pytest.warns() as warnings:
        value = config("FOO_TEST_ENVVAR", default="value", add_to_docs="foo_module")
        assert value == "value"
        # not registered to document
        assert not any(var.name == "FOO_TEST_ENVAR" for var in ENVVAR_REGISTRY)

    # warning mentions key actionable info
    assert "FOO_TEST_ENVVAR" in str(warnings[0])
    assert "foo_module" in str(warnings[0])


@pytest.mark.parametrize(
    "default,split",
    it.product([None, "value", "", undefined], [False, True]),
)
def test_it_doesnt_warn_if_env_is_not_set(default, split):
    with pytest.WarningsRecorder() as warnings:
        config("FOO_TEST_ENVVAR", default=default, add_to_docs="foo_module", split=True)
    assert not warnings.list


def test_get_django_project_dir():
    project_path = get_django_project_dir()
    assert project_path.parts[-1] == "testapp"

    # still compatible with os.path.join
    settings = os.path.join(project_path, "settings.py")
    assert os.path.exists(settings)
