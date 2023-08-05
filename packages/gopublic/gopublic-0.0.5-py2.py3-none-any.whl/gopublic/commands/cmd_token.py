import click
from gopublic.commands.token.create import cli as create


@click.group()
def cli():
    """
    Manipulate files managed by Gopublish
    """
    pass


cli.add_command(create)
