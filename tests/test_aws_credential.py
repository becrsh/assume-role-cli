from assume_role.aws.credential import AWSCredential
from assume_role.aws.profile import AWSProfile
import datetime
import os
import configparser

AWS_BASE_CREDS = """
    [default]
    aws_access_key_id = dummy-access-key-id
    aws_secret_access_key = dummy-secret-key-id

    """


def test_save_credential(tmp_path, monkeypatch):
    aws_cred_file = tmp_path / "credentials_test"
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(aws_cred_file))
    aws_cred_file.write_text(AWS_BASE_CREDS)

    p = AWSProfile(
        name="mock",
        source_profile="profile",
        role_arn="rolearn"
    )
    c = AWSCredential(
        aws_access_key_id="AAA",
        aws_secret_access_key="SSS",
        aws_session_token="TTT",
        expiration=datetime.date.today(),
        profile=p
    )
    c.save_to_file()

    config_file = os.path.expanduser(os.getenv("AWS_SHARED_CREDENTIALS_FILE"))

    config = configparser.RawConfigParser()
    config.read(config_file)

    assert "mock" in config.sections()
    assert "AAA" in config.get("mock", "aws_access_key_id")
    assert "SSS" in config.get("mock", "aws_secret_access_key")
    assert "TTT" in config.get("mock", "aws_session_token")


def test_overwrite_existing_credential(tmp_path,monkeypatch):
    aws_cred_file = tmp_path / "credentials_test"
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(aws_cred_file))
    aws_cred_file.write_text(AWS_BASE_CREDS)

    p = AWSProfile(
        name="default",
        source_profile="profile",
        role_arn="rolearn"
    )
    c = AWSCredential(
        aws_access_key_id="not-default",
        aws_secret_access_key="no-secret",
        aws_session_token="session",
        expiration=datetime.date.today(),
        profile=p
    )
    c.save_to_file()

    config_file = os.path.expanduser(os.getenv("AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials"))

    config = configparser.RawConfigParser()
    config.read(config_file)

    assert "default" in config.sections()
    assert "dummy-access-key-id" not in config.get("default", "aws_access_key_id")
    assert "dummy-secret-key-id" not in config.get("default", "aws_secret_access_key")
