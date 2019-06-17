import boto3
from .profile import AWSProfile
from .credential import AWSCredential
from boto3.exceptions import Boto3Error


class AssumedRole:
    def __init__(self, p: 'AWSProfile', mfa_code: str = None, source_type: str = ""):
        self._profile = p
        self._credential = None
        session = boto3.session.Session(profile_name=p.source_profile)
        self._client = session.client('sts')
        if source_type != 'federated':
            self.__assume_role(mfa_code)

    def __assume_role(self, mfa_code):

        # This is a way to get around the strange way of handling arguments (not accepting none)
        assume_role_args = {
            "RoleArn": self._profile.role_arn,
            "RoleSessionName": self._profile.role_session_name,
            "DurationSeconds": self._profile.duration_seconds,
        }
        if self._profile.external_id:
            assume_role_args['ExternalId'] = self._profile.external_id
        if self._profile.mfa_serial:
            assume_role_args['SerialNumber'] = self._profile.mfa_serial
        if mfa_code:
            assume_role_args['TokenCode'] = mfa_code

        response = self._client.assume_role(**assume_role_args)
        if 'Credentials' in response:
            self._credential = AWSCredential(
                aws_access_key_id=response['Credentials']['AccessKeyId'],
                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                aws_session_token=response['Credentials']['SessionToken'],
                expiration=response['Credentials']['Expiration'],
                profile=self
            )
        else:
            raise Boto3Error("No Credential in STS response found")

    @property
    def credential(self) -> 'AWSCredential':
        return self._credential
