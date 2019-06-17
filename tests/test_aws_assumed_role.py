from moto import mock_sts
from assume_role.aws.assumed_role import AssumedRole
from assume_role.aws.profile import AWSProfile

@mock_sts
def test_assume_known_role():
    p = AWSProfile("mock", "eu-west-1", role_arn="arn:aws:iam::221607635191:role/AdminRole", output="json")
    a = AssumedRole(p)

    assert None is not a.credential
