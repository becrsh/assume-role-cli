import profile


class AWSCredential:
    """
        Credential is handles the storage of the access/secret/session_key
    """
    @staticmethod
    def save_to_file(p: 'profile.AWSProfile', credential: 'AWSCredential'):
        pass

    def __init__(self, aws_access_key_id, aws_secret_access_key,aws_session_token, expiration):
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key
        self._aws_session_token = aws_session_token
        self._expiration = expiration

    @property
    def access_key_id(self):
        return self._aws_access_key_id

    @property
    def secret_access_key(self):
        return self._aws_secret_access_key

    @property
    def session_token(self):
        return self._aws_session_token
