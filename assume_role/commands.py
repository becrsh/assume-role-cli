import click
from aws_profile import AWSProfile


@click.command()
@click.argument("assume_profile")
@click.option("--profile", default="default", help="The source profile to use")
@click.option("--account-id", default=None, help="The account id of the account you want to assume the role in")
@click.option("--role-name", default=None, help="The role name you want to assume")
@click.option("--external-id", default=None, help="The external id for the role")
@click.option("--mfa-device", default=None, help="The MFA device that will generate a MFA code")
def assume_role(assume_profile, profile, account_id, role_name, external_id, mfa_device):
    profile: AWSProfile = AWSProfile.load_from_config(assume_profile)
    click.echo(f"Assume Profile: {profile.mfa_serial}")


if __name__ == '__main__':
    assume_role()
