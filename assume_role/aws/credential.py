from .profile import AWSProfile
import configparser
import os


class AWSCredential:
    """
        Credential is handles the storage of the access/secret/session_key
    """
    def __init__(self,profile, aws_access_key_id, aws_secret_access_key,aws_session_token, expiration):
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_session_token = aws_session_token
        self._expiration = expiration
        self._profile:'AWSProfile' = profile

    @property
    def access_key_id(self):
        return self._aws_access_key_id

    @property
    def secret_access_key(self):
        return self._aws_secret_access_key

    @property
    def session_token(self):
        return self._aws_session_token

    def save_to_file(self):
        config = _parse_credential_file()
        if self._profile.name not in config.sections():
            config.add_section(self._profile.name)
        config.set(self._profile.name, "aws_access_key_id", self.access_key_id)
        config.set(self._profile.name, "aws_secret_access_key", self.secret_access_key)
        config.set(self._profile.name, "aws_session_token", self.session_token)
        _save_credential_file(config)


def _parse_credential_file():
    """Parses AWS Config file and return the object"""
    config_file = os.path.expanduser(os.getenv("AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials"))

    config = configparser.RawConfigParser()
    config.read(config_file)

    return config


def _save_credential_file(config: 'configparser.RawConfigParser'):
    """Saves credential file"""
    config_file = os.path.expanduser(os.getenv("AWS_SHARED_CREDENTIALS_FILE", "~/.aws/credentials"))

    with open(config_file,"w") as file:
        config.write(file)
