import configparser
import boto3
import os

import logging

logger = logging.getLogger()

# Not really the best way but get_caller_identity can't be mocked atm
UNIT_TEST = True if os.getenv('TEST_RUN') == 'true' else False


class AWSProfile:
    """
        AWS Profile
    """

    @staticmethod
    def load_from_config(name) -> 'AWSProfile':
        search_section = "default" if name == "default" else "profile {}".format(name)
        config = _parse_config_file()
        logger.info(f"{search_section} in {config.sections()}")
        if search_section in config.sections():
            profile = AWSProfile(
                name,
                region=config.get(search_section,'region', fallback=config.get('default', 'region')),
                source_profile=config.get(search_section, 'source_profile'),
                role_arn=config.get(search_section, 'role_arn'),
                output=config.get(search_section, 'output', fallback=config.get('default', 'output')),
                mfa_serial=config.get(search_section, 'mfa_serial', fallback=None),
                duration_seconds=config.get(search_section, 'duration_seconds', fallback=3600),
                role_session_name=config.get(search_section,'role_session_name', fallback=None)
            )
        else:
            return None

        return profile

    @staticmethod
    def list():
        profiles = []
        config = _parse_config_file()
        for section in config.sections():
            name = 'default'
            if section.startswith("profile "):
                name = section[8:]

            profiles.append(
                AWSProfile(
                    name,
                    region=config.get(section, 'region', fallback=config.get('default', 'region')),
                    source_profile=config.get(section, 'source_profile'),
                    role_arn=config.get(section, 'role_arn'),
                    output=config.get(section, 'output', fallback=config.get('default', 'output')),
                    mfa_serial=config.get(section, 'mfa_serial', fallback='')
                )
            )

        return profiles

    @staticmethod
    def save_to_file(profile):
        pass

    def __init__(self, name, region=None, source_profile=None, role_arn=None, output=None, mfa_serial=None,
                 external_id=None, role_session_name=None, duration_seconds=3600):
        self._name = name
        self._region = region
        self._source_profile = source_profile
        self._role_arn = role_arn
        self._output = output
        self._mfa_serial = mfa_serial
        self._role_session_name = role_session_name
        self._external_id = external_id
        self._duration_seconds = duration_seconds

    def __str__(self):
        return f"{self._name}//{self._region}//{self._role_arn}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def role_arn(self):
        return self._role_arn

    @role_arn.setter
    def role_arn(self, value):
        self._role_arn = value

    @property
    def source_profile(self):
        return self._source_profile

    @source_profile.setter
    def source_profile(self, value):
        self._source_profile = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value):
        self._region = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    @property
    def mfa_serial(self):
        return self._mfa_serial

    @mfa_serial.setter
    def mfa_serial(self, value):
        self._mfa_serial = value

    @property
    def role_session_name(self):
        if not self._role_session_name:
            if not UNIT_TEST:
                session = boto3.session.Session(profile_name=self.source_profile)
                client = session.client('sts')
                response = client.get_caller_identity()
                if 'Arn' in response:
                    account_id = response['Account']
                    role_id = response['Arn'].split('/')[-1]
                    self._role_session_name = f"{role_id}@{account_id}"
            else:
                self._role_session_name = "UnitTesting@123456789012"

        return self._role_session_name

    @role_session_name.setter
    def role_session_name(self, value):
        self._role_session_name = value

    @property
    def external_id(self):
        return self._external_id

    @external_id.setter
    def external_id(self, value):
        self._external_id = value

    @property
    def duration_seconds(self):
        return self._duration_seconds

    @duration_seconds.setter
    def duration_seconds(self, value):
        self._duration_seconds = value


def _parse_config_file():
    """Parses AWS Config file and return the object"""
    config_file = os.path.expanduser(os.getenv("AWS_CONFIG_FILE", "~/.aws/config"))
    logger.info(f"Config file reading: {config_file}")
    config = configparser.RawConfigParser()
    config.read(config_file)

    return config