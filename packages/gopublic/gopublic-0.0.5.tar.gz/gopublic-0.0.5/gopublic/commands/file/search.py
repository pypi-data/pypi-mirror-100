import click
from gopublic.cli import pass_context, json_loads
from gopublic.decorators import custom_exception, dict_output


@click.command('search')
@click.argument("file_name", type=str)
@click.option(
    "--limit",
    help="Limit the results numbers",
    type=int
)
@click.option(
    "--offset",
    help="Offset for listing the results (used with limit)",
    type=int
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_name, limit="", offset=""):
    """Launch a pull task

Output:

    Dict with files and total count
    """
    return ctx.gi.file.search(file_name, limit=limit, offset=offset)
