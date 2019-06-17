from click.testing import CliRunner
import pytest
import os
import traceback
from moto import mock_sts

from assume_role import commands

AWS_CONFIG = """
[default]
output = json
region = eu-west-1

[profile test]
region=eu-west-1
output=json
source_profile = default
role_session_name = pytest
role_arn = arn:aws:iam::123456789012:role/dummy
mfa_serial = arn:aws:iam::123456789012:mfa/dummy
"""

AWS_BASE_CREDS = """
[default]
aws_access_key_id = dummy-access-key-id
aws_secret_access_key = dummy-secret-key-id

"""


@pytest.fixture(scope="function")
def runner(tmp_path):
    aws_config_file = tmp_path / "config_test"
    aws_cred_file = tmp_path / "credentials_test"
    aws_env = {
        "AWS_SHARED_CREDENTIALS_FILE": str(aws_cred_file),
        "AWS_CONFIG_FILE": str(aws_config_file)
    }
    cli_runner: 'CliRunner' = CliRunner(env=aws_env)
    aws_config_file.write_text(AWS_CONFIG)
    aws_cred_file.write_text(AWS_BASE_CREDS)
    return cli_runner


def test_no_profile(runner):
    result = runner.invoke(commands.assume_role, catch_exceptions=False)

    assert result.exit_code == 2


def test_unkown_profile(runner):
    result = runner.invoke(commands.assume_role, args=["unknown_profile"])

    assert result.exit_code == 2

@mock_sts
def test_known_profile(runner):
    result = runner.invoke(commands.assume_role, args=["test", "-e"], input='123456\n')
    if result.exception:
        traceback.print_exception(*result.exc_info)

    print(result.output)
    assert result.exit_code == 0
    assert "export AWS_ACCESS_KEY_ID=" in result.output
    assert "export AWS_SECRET_ACCESS_KEY" in result.output
    assert "export AWS_SESSION_TOKEN" in result.output
