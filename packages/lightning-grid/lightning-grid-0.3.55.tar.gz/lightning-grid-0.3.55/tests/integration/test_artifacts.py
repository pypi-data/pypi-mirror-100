from click.testing import CliRunner
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
from grid.client import Grid

RUNNER = CliRunner()
create_test_credentials()


def monkey_patch_download_artifacts(_self, *args, **kwargs):
    """Monkey patch the client download."""
    return


def test_artifacts_succeeds(monkeypatch):
    """grid train without arguments fails"""
    monkeypatch.setattr(Grid, '_init_client', monkey_patch_client)
    monkeypatch.setattr(Grid, 'download_experiment_artifacts',
                        monkey_patch_download_artifacts)

    result = RUNNER.invoke(cli.artifacts, ['foo-bar-exp0'])
    assert result.exit_code == 0
    assert not result.exception
