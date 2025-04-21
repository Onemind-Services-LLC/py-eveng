import click

from evengsdk.exceptions import EvengApiError, EvengHTTPError
from evengsdk.cli.console import console
from evengsdk.cli.common import list_sub_command
from evengsdk.cli.console import cli_print_output
from evengsdk.cli.utils import get_client


@list_sub_command
@click.pass_context
def ls(ctx, output):
    """
    List folders on EVE-NG host

    \b
    Examples:
        eve-ng folder list
    """
    client = get_client(ctx)
    resp = client.api.list_folders()
    folder_data = resp["data"]["folders"]
    table_header = [
        ("Name", dict(justify="right", style="cyan", no_wrap=True)),
        ("Path", {}),
    ]
    cli_print_output(
        output,
        {"data": folder_data},
        header="Folders",
        table_header=table_header,
        table_title="Folders",
    )


@click.command()
@click.option("--name", default="/", help="Folder Name to create (e.g., /MyLabFolder)")
@click.pass_context
def create(ctx, name: str):
    """
    Create a folder on EVE-NG host.

    Example:
        eve-ng folder create --name MyNewFolder
    """
    client = get_client(ctx)
    try:
        with console.status("[bold green]Creating folder...") as status:
            response = client.api.create_folder(name=name)
            console.log(f"{response['status']}: {response['message']}")
            status.update("[bold green]Folder created successfully")
            cli_print_output("text", response)
    except (EvengHTTPError, EvengApiError) as err:
        console.print(f"Error: {err}")


@click.command()
@click.argument("folder")
@click.pass_context
def read(ctx, folder):
    """
    Get folder details EVE-NG host

    \b
    Examples:
        eve-ng folder read /path/to/folder
    """
    client = get_client(ctx)
    resp = client.api.get_folder(folder)
    cli_print_output("json", resp)


@click.command()
@click.option("--folder-path", help="Folder path")
@click.option("--rename", help="Folder name to be renamed")
@click.pass_context
def edit(ctx, folder_path: str, rename: str):
    """
    Edit folder on EVE-NG host

    \b
    Examples:
        eve-ng folder edit --folder-path YourFolderName --rename YourRenamedFolder
    """
    client = get_client(ctx)
    try:
        with console.status("[bold green]Editing folder...") as status:
            response = client.api.edit_folder(folder_path=folder_path, rename=rename)
            console.log(f"{response['status']}: {response['message']}")
            status.update("[bold green]folder edited successfully")
            cli_print_output("text", response)
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@click.command()
@click.option("--folder-name", default="/", help="folder to delete")
@click.pass_context
def delete(ctx, folder_name):
    """
    Delete folder on EVE-NG host

    \b
    Examples:
        eve-ng folder delete FolderName
    """
    client = get_client(ctx)
    try:
        with console.status("[bold green]wiping folders...") as status:
            response = client.api.delete_folder(folder_name)
            console.log(f"{response['status']}: {response['message']}")
            status.update("[bold green]folder deleted successfully")
            cli_print_output("text", response)
    except (EvengHTTPError, EvengApiError) as err:
        console.print_error(err)


@click.group()
@click.pass_context
def folder(ctx):
    """folder sub commands

    Manage EVE-NG folders
    """
    global client
    client = ctx.obj.client


folder.add_command(ls)
folder.add_command(create)
folder.add_command(read)
folder.add_command(edit)
folder.add_command(delete)
