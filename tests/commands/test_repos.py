"""Tests for the repos commands."""

from unittest import mock

from click.testing import CliRunner


class TestReposCommands:
    """Test cases for repos commands."""

    def setup_method(self):
        """Set up test dependencies."""
        self.runner = CliRunner()
        # Import the repos group to ensure commands are registered
        from ecosystems_cli.commands.repos import repos

        self.repos_group = repos

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_topics(self, mock_print_output, mock_get_client):
        """Test getting topics."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {"name": "python", "repository_count": 1500},
            {"name": "javascript", "repository_count": 2000},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_group,
            ["topics", "--page", "1", "--per-page", "20"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "topics",
            path_params={},
            query_params={
                "page": 1,
                "per_page": 20,
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_topic(self, mock_print_output, mock_get_client):
        """Test getting a specific topic."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "machine-learning",
            "repository_count": 500,
            "repositories": [
                {"name": "tensorflow/tensorflow", "stars": 180000},
                {"name": "pytorch/pytorch", "stars": 70000},
            ],
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_group,
            ["topic", "machine-learning"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "topic",
            path_params={"topic": "machine-learning"},
            query_params={},
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_repositories_lookup(self, mock_print_output, mock_get_client):
        """Test looking up a repository by URL."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "django/django",
            "host": "github.com",
            "language": "Python",
            "stars": 75000,
            "forks": 30000,
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_group,
            ["repositories_lookup", "--url", "https://github.com/django/django"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "repositoriesLookup",
            path_params={},
            query_params={
                "url": "https://github.com/django/django",
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_repositories_lookup_by_purl(self, mock_print_output, mock_get_client):
        """Test looking up a repository by purl."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = {
            "name": "facebook/react",
            "host": "github.com",
            "language": "JavaScript",
            "stars": 210000,
            "forks": 44000,
        }
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_group,
            ["repositories_lookup", "--purl", "pkg:github/facebook/react"],
            obj={"timeout": 20, "format": "json"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "repositoriesLookup",
            path_params={},
            query_params={
                "purl": "pkg:github/facebook/react",
            },
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_output")
    def test_usage(self, mock_print_output, mock_get_client):
        """Test getting package usage ecosystems."""
        mock_client = mock.MagicMock()
        mock_client.call.return_value = [
            {"ecosystem": "npm", "packages_count": 2500000},
            {"ecosystem": "pypi", "packages_count": 450000},
        ]
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_group,
            ["usage"],
            obj={"timeout": 20, "format": "table"},
        )

        assert result.exit_code == 0
        mock_get_client.assert_called_once_with("repos", base_url=None, timeout=20)
        mock_client.call.assert_called_once_with(
            "usage",
            path_params={},
            query_params={},
        )
        mock_print_output.assert_called_once()

    @mock.patch("ecosystems_cli.commands.execution.get_client")
    @mock.patch("ecosystems_cli.commands.execution.print_error")
    def test_topic_error(self, mock_print_error, mock_get_client):
        """Test error handling when getting a topic."""
        mock_client = mock.MagicMock()
        mock_client.call.side_effect = Exception("Topic not found")
        mock_get_client.return_value = mock_client

        result = self.runner.invoke(
            self.repos_group,
            ["topic", "nonexistent"],
            obj={"timeout": 20},
        )

        assert result.exit_code == 0
        mock_print_error.assert_called_once_with("Unexpected error: Topic not found", console=mock.ANY)
