import click


@click.command()
@click.argument("assume_profile")
@click.option("--profile", default="default", help="The source profile to use")
def cli(assume_profile, profile):
    click.echo(f"Hello {assume_profile}!")
    click.echo(f"Whatsup from {profile}!")


if __name__ == '__main__':
    cli()
