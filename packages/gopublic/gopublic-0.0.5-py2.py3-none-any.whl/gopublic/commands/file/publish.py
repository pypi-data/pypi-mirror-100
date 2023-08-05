import click
from gopublic.cli import pass_context, json_loads
from gopublic.decorators import custom_exception, dict_output


@click.command('publish')
@click.argument("path", type=str)
@click.option(
    "--version",
    help="Version of the file to publish",
    default="1",
    show_default=True,
    type=int
)
@click.option(
    "--contact",
    help="Contact email for this file",
    type=str
)
@click.option(
    "--email",
    help="Contact email for notification when publication is done",
    type=str
)
@click.option(
    "--token",
    help="You Gopublish token.",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, path, version=1, contact="", email="", token=""):
    """Launch a publish task

Output:

    Dictionnary containing the response
    """
    return ctx.gi.file.publish(path, version=version, contact=contact, email=email, token=token)
