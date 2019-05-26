import click


@click.command()
@click.argument("assume_profile", help="The profile in credentials file")
@click.option("--profile", default="default", help="The source profile to use")
@click.option("--account-id", required=False, help="The account id of the account you want to assume the role in")
@click.option("--role-name", required=False, help="The role name you want to assume")
@click.option("--external-id", required=False, help="The external id for the role")
@click.option("--mfa-device", required=False, help="The MFA device that will generate a MFA code")
def cli(assume_profile, profile):
    pass


if __name__ == '__main__':
    cli()
