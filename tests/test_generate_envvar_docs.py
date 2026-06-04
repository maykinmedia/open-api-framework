from importlib.util import find_spec
from unittest.mock import mock_open, patch

from django.core.management import call_command

import pytest
from syrupy.extensions.amber import AmberSnapshotExtension

extras_installed = bool(find_spec("csp"))


@pytest.fixture
def snapshot(snapshot):
    extras = "extras" if extras_installed else "no_extras"

    class CustomSnaphotDir(AmberSnapshotExtension):
        snapshot_dirname = f"__snapshot_{extras}__"

    return snapshot.use_extension(CustomSnaphotDir)


def test_generate_envvar_docs(snapshot):
    mock_file = mock_open()

    with patch(
        "open_api_framework.management.commands.generate_envvar_docs.open", mock_file
    ):
        call_command(
            "generate_envvar_docs", file="some/file/path.txt", exclude_group="Excluded"
        )

        mock_file.assert_called_once_with("some/file/path.txt", "w")

        handle = mock_file()

        # Check the entire content written to the mock file
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)

    assert written_content == snapshot

    if not extras_installed:
        assert "Cross-Origin-Resource-Sharing" not in written_content
        assert "Content Security Policy" not in written_content
