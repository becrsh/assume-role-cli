import click
from .aws.profile import AWSProfile
from .aws import assumed_role


@click.command()
@click.argument("assume_profile")
@click.option("-e", "--env", default=False, is_flag=True, help="print the export commands for the environments")
@click.option("--profile", default="default", help="The source profile to use")
@click.option("--account-id", default=None, help="The account id of the account you want to assume the role in")
@click.option("--role-name", default=None, help="The role name you want to assume")
@click.option("--external-id", default=None, help="The external id for the role")
@click.option("--mfa-serial", default=None, help="The MFA device that will generate a MFA code")
def assume_role(assume_profile, env, profile, account_id, role_name, external_id, mfa_serial):
    """
    CLI Command assume_role will return (based on passed cli options and arguments) valid AWS Credentials

    if no arguments are passed he will check if the assume profile is defined in the AWS Config file.

    """
    p: AWSProfile = AWSProfile.load_from_config(assume_profile)
    mfa_code = None

    if p is None:
        if account_id and role_name:
            p = AWSProfile(
                name=assume_profile,
                source_profile=profile,
                role_arn=f"arn:aws:iam::{account_id}:role/{role_name}",
                external_id=external_id,
                mfa_serial=mfa_serial
            )
        else:
            raise click.BadParameter("Unkown Profile and no --account-id or --role-name supplied")

    if p.mfa_serial:
        mfa_code = click.prompt(f"Enter MFA Code for {p.mfa_serial}", err=True)

    credential = assumed_role.AssumedRole(p, mfa_code).credential

    if env:
        _display_env_vars(credential)
    else:
        click.echo(f"Authenticating Profile: {p.name}")


def _display_env_vars(credential):
    click.echo(f"export AWS_ACCESS_KEY_ID={credential.access_key_id}")
    click.echo(f"export AWS_SECRET_ACCESS_KEY={credential.secret_access_key}")
    click.echo(f"export AWS_SESSION_TOKEN={credential.session_token}")


if __name__ == '__main__':
    assume_role()
