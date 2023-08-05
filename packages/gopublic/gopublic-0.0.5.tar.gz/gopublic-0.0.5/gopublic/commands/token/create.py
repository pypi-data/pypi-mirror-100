import click
from gopublic.cli import pass_context, json_loads
from gopublic.decorators import custom_exception, dict_output


@click.command('create')
@click.argument("username", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, username):
    """Get token

Output:

    Dictionnary containg the token
    """
    return ctx.gi.token.create(username)
