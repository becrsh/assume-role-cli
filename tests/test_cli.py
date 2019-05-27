from click.testing import CliRunner
import pytest
import traceback

from assume_role import commands


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


def test_no_profile(runner):
    result = runner.invoke(commands.cli, ["my_profile"])
    if result.exception:
        traceback.print_exception(*result.exc_info)

    assert result.exit_code == 0
    assert result.output == 'export AWS_ACCESS_KEY_ID='
