import pytest
from click.testing import CliRunner, Result

from py_eveng.cli.cli import main as cli


@pytest.mark.usefixtures("authenticated_client")
class TestLabFolderCommands:
    """CLI Folder Commands"""

    def test_folder_list(self):
        """
        Arrange/Act: Run the `folder` command with the 'list' subcommand.
        Assert: The output indicates that folders are listed successfully.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli, ["folder", "list"])
        assert result.exit_code == 0, result.output

    def test_folder_create(self):
        """
        Arrange/Act: Run the `folder` command with the 'create' subcommand.
        Assert: The output indicates that folders are create successfully.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli, ["folder", "create"])
        assert result.exit_code == 0, result.output

    def test_folder_read(self):
        """
        Arrange/Act: Run the `folder` command with the 'read' subcommand.
        Assert: The output indicates that folders are retrieved successfully.
        """
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli, ["folder", "read", "/"])
        assert result.exit_code == 0, result.output

    def test_folder_edit(self):
        """
        Arrange/Act: Run the `folder` command with the 'edit' subcommand.
        Assert: The output indicates that folder is updated successfully.
        """
        runner: CliRunner = CliRunner()
        # Step 1: Create folder
        result_create = runner.invoke(
            cli, ["folder", "create", "--name", "test_folder"]
        )
        assert result_create.exit_code == 0, result_create.output

        # Step 2: Edit folder
        result = runner.invoke(
            cli,
            [
                "folder",
                "edit",
                "--folder-path",
                "test_folder",
                "--rename",
                "edited_folder",
            ],
        )
        assert result.exit_code == 0, result.output

        # Step 3: Delete folder
        result = runner.invoke(
            cli, ["folder", "delete", "--folder-name", "edited_folder"]
        )
        assert result.exit_code == 0, result.output

    def test_folder_delete(self):
        """
        Arrange/Act: Run the `folder` command with the 'delete' subcommand.
        Assert: The output indicates that folder is deleted successfully.
        """
        runner: CliRunner = CliRunner()
        # Step 1: Create folder
        result_create = runner.invoke(
            cli, ["folder", "create", "--name", "test_folder"]
        )
        assert result_create.exit_code == 0, result_create.output

        # Step 2: Delete folder
        result = runner.invoke(
            cli, ["folder", "delete", "--folder-name", "test_folder"]
        )
        assert result.exit_code == 0, result.output
