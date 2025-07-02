"""Tests for papers commands."""

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from ecosystems_cli.commands.papers import PapersCommands


class TestPapersCommands:
    """Test cases for papers commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        self.papers_commands = PapersCommands()

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_operations")
    def test_list_operations(self, mock_print_operations, mock_get_client):
        """Test listing operations."""
        mock_client = MagicMock()
        mock_client.list_operations.return_value = [
            {"id": "listPapers", "method": "GET", "path": "/papers", "summary": "List papers"},
            {"id": "getPaper", "method": "GET", "path": "/papers/{doi}", "summary": "Get paper"},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.papers_commands.group, ["list"], obj={"timeout": 20})

        assert result.exit_code == 0
        mock_client.list_operations.assert_called_once()
        mock_print_operations.assert_called_once()

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_list_papers(self, mock_print_output, mock_get_client):
        """Test listing papers."""
        mock_client = MagicMock()
        mock_papers = [
            {
                "doi": "10.1234/test1",
                "title": "Test Paper 1",
                "publication_date": "2023-01-01",
                "mentions_count": 5,
            },
            {
                "doi": "10.1234/test2",
                "title": "Test Paper 2",
                "publication_date": "2023-02-01",
                "mentions_count": 3,
            },
        ]
        mock_client.list_papers.return_value = mock_papers
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.papers_commands.group, ["list-papers"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_client.list_papers.assert_called_once_with(page=None, per_page=None, sort=None, order=None)
        mock_print_output.assert_called_once()

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_list_papers_with_options(self, mock_print_output, mock_get_client):
        """Test listing papers with pagination and sorting options."""
        mock_client = MagicMock()
        mock_client.list_papers.return_value = []
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.papers_commands.group,
            ["list-papers", "--page", "2", "--per-page", "50", "--sort", "publication_date", "--order", "desc"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_client.list_papers.assert_called_once_with(page=2, per_page=50, sort="publication_date", order="desc")

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_get_paper(self, mock_print_output, mock_get_client):
        """Test getting a specific paper."""
        mock_client = MagicMock()
        mock_paper = {
            "doi": "10.1234/test",
            "title": "Test Paper",
            "publication_date": "2023-01-01",
            "mentions_count": 5,
            "openalex_id": "W123456",
        }
        mock_client.get_paper.return_value = mock_paper
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.papers_commands.group, ["get", "10.1234/test"], obj={"timeout": 20, "format": "table"})

        assert result.exit_code == 0
        mock_client.get_paper.assert_called_once_with(doi="10.1234/test")
        mock_print_output.assert_called_once()

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_get_paper_json_output(self, mock_print_output, mock_get_client):
        """Test getting a paper with JSON output."""
        mock_client = MagicMock()
        mock_paper = {"doi": "10.1234/test", "title": "Test Paper"}
        mock_client.get_paper.return_value = mock_paper
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(self.papers_commands.group, ["get", "10.1234/test"], obj={"timeout": 20, "format": "json"})

        assert result.exit_code == 0
        mock_client.get_paper.assert_called_once_with(doi="10.1234/test")
        mock_print_output.assert_called_once_with(mock_paper, "json", console=self.papers_commands.console)

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_get_paper_mentions(self, mock_print_output, mock_get_client):
        """Test getting paper mentions."""
        mock_client = MagicMock()
        mock_mentions = [
            {"id": 1, "paper_url": "https://paper1.com", "project_url": "https://project1.com"},
            {"id": 2, "paper_url": "https://paper1.com", "project_url": "https://project2.com"},
        ]
        mock_client.get_paper_mentions.return_value = mock_mentions
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.papers_commands.group, ["mentions", "10.1234/test"], obj={"timeout": 20, "format": "table"}
        )

        assert result.exit_code == 0
        mock_client.get_paper_mentions.assert_called_once_with(doi="10.1234/test", page=None, per_page=None)
        mock_print_output.assert_called_once()

    @patch("ecosystems_cli.commands.base.get_client")
    @patch("ecosystems_cli.commands.base.print_output")
    def test_get_paper_mentions_with_pagination(self, mock_print_output, mock_get_client):
        """Test getting paper mentions with pagination."""
        mock_client = MagicMock()
        mock_client.get_paper_mentions.return_value = []
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.papers_commands.group,
            ["mentions", "10.1234/test", "--page", "3", "--per-page", "25"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_client.get_paper_mentions.assert_called_once_with(doi="10.1234/test", page=3, per_page=25)

    @patch("ecosystems_cli.cli._call_operation")
    def test_call_operation(self, mock_call_operation):
        """Test calling an arbitrary operation."""
        result = self.runner.invoke(
            self.papers_commands.group,
            ["call", "getPaper", "--path-params", '{"doi": "10.1234/test"}'],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_call_operation.assert_called_once()
        args = mock_call_operation.call_args[0]
        assert args[0] == "papers"
        assert args[1] == "getPaper"
        assert args[2] == '{"doi": "10.1234/test"}'
        assert args[3] is None  # query_params
        assert args[4] is None  # body
