import configparser
import os


class AWSProfile:
    """
        AWS Profile
    """

    @staticmethod
    def load_from_config(name):
        search_section = "default" if name == "default" else "profile {}".format(name)
        config_file = os.path.expanduser(os.getenv("AWS_CONFIG_FILE", "~/.aws/config"))

        config = configparser.RawConfigParser()
        config.read(config_file)

        if search_section in config.sections():
            profile = AWSProfile(
                name,
                region=config.get(search_section,'region', fallback=config.get('default', 'region')),
                source_profile=config.get(search_section, 'source_profile'),
                role_arn=config.get(search_section,'role_arn'),
                output=config.get(search_section,'output', fallback=config.get('default','output')),
                mfa_serial=config.get(search_section,'mfa_serial')
            )
        else:
            return None

        return profile

    @staticmethod
    def save_to_file(profile):
        pass

    def __init__(self, name, region=None, source_profile=None, role_arn=None, output=None, mfa_serial=None, role_session_name=None):
        self._name = name
        self._region = region
        self._source_profile = source_profile
        self._role_arn = role_arn
        self._output = output
        self._mfa_serial = mfa_serial
        self._role_session_name = role_session_name

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
        return self._role_session_name

    @role_session_name.setter
    def role_session_name(self,value):
        self._role_session_name = value