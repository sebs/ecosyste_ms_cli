"""Tests for the get_domain helper functions."""

from ecosystems_cli.helpers.get_domain import build_base_url, get_domain_with_precedence


class TestGetDomainWithPrecedence:
    """Test cases for get_domain_with_precedence function."""

    def test_no_domain_returns_none(self):
        """Test that None is returned when no domain is configured."""
        result = get_domain_with_precedence("repos", None)
        assert result is None

    def test_domain_override_used_when_provided(self):
        """Test that --domain parameter is used when provided."""
        result = get_domain_with_precedence("repos", "custom.domain.com")
        assert result == "custom.domain.com"

    def test_general_env_var_used_when_set(self, monkeypatch):
        """Test that general environment variable is used."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "env.domain.com")
        result = get_domain_with_precedence("repos", None)
        assert result == "env.domain.com"

    def test_api_specific_env_var_takes_precedence(self, monkeypatch):
        """Test that API-specific env var takes precedence over general."""
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "general.domain.com")
        monkeypatch.setenv("ECOSYSTEMS_REPOS_DOMAIN", "repos.domain.com")
        result = get_domain_with_precedence("repos", None)
        assert result == "repos.domain.com"

    def test_env_var_takes_precedence_over_domain_param(self, monkeypatch):
        """Test that env var takes precedence over --domain parameter."""
        monkeypatch.setenv("ECOSYSTEMS_REPOS_DOMAIN", "env.domain.com")
        result = get_domain_with_precedence("repos", "param.domain.com")
        assert result == "env.domain.com"

    def test_custom_env_prefix(self, monkeypatch):
        """Test using a custom environment variable prefix."""
        monkeypatch.setenv("CUSTOM_REPOS_DOMAIN", "custom.domain.com")
        result = get_domain_with_precedence("repos", None, env_prefix="CUSTOM")
        assert result == "custom.domain.com"

    def test_api_name_case_insensitive(self, monkeypatch):
        """Test that API name is converted to uppercase for env var."""
        monkeypatch.setenv("ECOSYSTEMS_PACKAGES_DOMAIN", "packages.domain.com")
        result = get_domain_with_precedence("packages", None)
        assert result == "packages.domain.com"

    def test_precedence_order_complete(self, monkeypatch):
        """Test complete precedence order: API env > general env > param."""
        # Set all three sources
        monkeypatch.setenv("ECOSYSTEMS_DOMAIN", "general.domain.com")
        monkeypatch.setenv("ECOSYSTEMS_REPOS_DOMAIN", "repos.domain.com")

        # API-specific env should win
        result = get_domain_with_precedence("repos", "param.domain.com")
        assert result == "repos.domain.com"

        # Remove API-specific, general env should win
        monkeypatch.delenv("ECOSYSTEMS_REPOS_DOMAIN")
        result = get_domain_with_precedence("repos", "param.domain.com")
        assert result == "general.domain.com"

        # Remove general env, param should win
        monkeypatch.delenv("ECOSYSTEMS_DOMAIN")
        result = get_domain_with_precedence("repos", "param.domain.com")
        assert result == "param.domain.com"


class TestBuildBaseUrl:
    """Test cases for build_base_url function."""

    def test_none_domain_returns_none(self):
        """Test that None is returned for None domain."""
        result = build_base_url(None, "repos")
        assert result is None

    def test_empty_domain_returns_none(self):
        """Test that None is returned for empty domain."""
        result = build_base_url("", "repos")
        assert result is None

    def test_domain_without_protocol_adds_https(self):
        """Test that HTTPS and /api/v1 are added to domain without protocol."""
        result = build_base_url("api.example.com", "repos")
        assert result == "https://api.example.com/api/v1"

    def test_domain_with_http_preserved(self):
        """Test that HTTP protocol is preserved."""
        result = build_base_url("http://api.example.com", "repos")
        assert result == "http://api.example.com"

    def test_domain_with_https_preserved(self):
        """Test that HTTPS protocol is preserved."""
        result = build_base_url("https://api.example.com", "repos")
        assert result == "https://api.example.com"

    def test_domain_with_path_preserved(self):
        """Test that existing path in URL is preserved."""
        result = build_base_url("https://api.example.com/v2", "repos")
        assert result == "https://api.example.com/v2"

    def test_domain_with_port_preserved(self):
        """Test that port number is preserved."""
        result = build_base_url("api.example.com:8080", "repos")
        assert result == "https://api.example.com:8080/api/v1"
