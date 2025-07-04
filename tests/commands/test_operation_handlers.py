"""Tests for operation handlers."""

from ecosystems_cli.commands.handlers import (
    ArchivesOperationHandler,
    DefaultOperationHandler,
    OperationHandler,
    OperationHandlerFactory,
    ResolverOperationHandler,
)


class TestResolverOperationHandler:
    """Test resolver operation handler."""

    def test_create_job_with_args(self):
        """Test createJob operation with positional arguments."""
        handler = ResolverOperationHandler()
        path_params, query_params = handler.build_params("createJob", ("package_name_value", "registry_value"), {})

        assert path_params == {}
        assert query_params == {"package_name": "package_name_value", "registry": "registry_value"}

    def test_create_job_with_optional_params(self):
        """Test createJob operation with optional parameters."""
        handler = ResolverOperationHandler()
        path_params, query_params = handler.build_params(
            "createJob", ("package_name_value", "registry_value"), {"before": "2023-01-01", "version": "1.0.0"}
        )

        assert path_params == {}
        assert query_params == {
            "package_name": "package_name_value",
            "registry": "registry_value",
            "before": "2023-01-01",
            "version": "1.0.0",
        }

    def test_get_job(self):
        """Test getJob operation."""
        handler = ResolverOperationHandler()
        path_params, query_params = handler.build_params("getJob", ("job123",), {})

        assert path_params == {"jobID": "job123"}
        assert query_params == {}

    def test_unknown_operation(self):
        """Test unknown operation returns empty params."""
        handler = ResolverOperationHandler()
        path_params, query_params = handler.build_params("unknownOp", ("arg1",), {})

        assert path_params == {}
        assert query_params == {}


class TestArchivesOperationHandler:
    """Test archives operation handler."""

    def test_list_with_args(self):
        """Test list operation with positional arguments."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("list", ("http://example.com",), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}

    def test_list_with_kwargs(self):
        """Test list operation with keyword arguments."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("list", (), {"url": "http://example.com"})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}

    def test_contents_with_args(self):
        """Test contents operation with positional arguments."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("contents", ("http://example.com", "/path/to/file"), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com", "path": "/path/to/file"}

    def test_contents_with_kwargs(self):
        """Test contents operation with keyword arguments."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("contents", (), {"url": "http://example.com", "path": "/path/to/file"})

        assert path_params == {}
        assert query_params == {"url": "http://example.com", "path": "/path/to/file"}

    def test_readme_operation(self):
        """Test readme operation."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("readme", ("http://example.com",), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}

    def test_changelog_operation(self):
        """Test changelog operation."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("changelog", ("http://example.com",), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}

    def test_repopack_operation(self):
        """Test repopack operation."""
        handler = ArchivesOperationHandler()
        path_params, query_params = handler.build_params("repopack", ("http://example.com",), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}


class TestDefaultOperationHandler:
    """Test default operation handler."""

    def test_get_project(self):
        """Test getProject operation."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("getProject", ("project123",), {})

        assert path_params == {"id": "project123"}
        assert query_params == {}

    def test_get_topic(self):
        """Test getTopic operation."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("getTopic", ("topic-slug",), {})

        assert path_params == {"slug": "topic-slug"}
        assert query_params == {}

    def test_get_collective(self):
        """Test getCollective operation."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("getCollective", ("collective123",), {})

        assert path_params == {"id": "collective123"}
        assert query_params == {}

    def test_get_collective_projects(self):
        """Test getCollectiveProjects operation."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("getCollectiveProjects", ("collective-slug",), {})

        assert path_params == {"slug": "collective-slug"}
        assert query_params == {}

    def test_lookup_project(self):
        """Test lookupProject operation."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("lookupProject", ("http://example.com",), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}

    def test_create_job(self):
        """Test createJob operation for default handler."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("createJob", ("http://example.com",), {})

        assert path_params == {}
        assert query_params == {"url": "http://example.com"}

    def test_get_job(self):
        """Test getJob operation for default handler."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("getJob", ("job123",), {})

        assert path_params == {"jobID": "job123"}
        assert query_params == {}

    def test_with_kwargs(self):
        """Test operation with kwargs."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("getProject", (), {"id": "project123"})

        assert path_params == {"id": "project123"}
        assert query_params == {}

    def test_empty_args(self):
        """Test operation with no arguments."""
        handler = DefaultOperationHandler()
        path_params, query_params = handler.build_params("someOperation", (), {})

        assert path_params == {}
        assert query_params == {}


class TestOperationHandlerFactory:
    """Test operation handler factory."""

    def test_get_resolver_handler(self):
        """Test getting resolver handler."""
        handler = OperationHandlerFactory.get_handler("resolver")
        assert isinstance(handler, ResolverOperationHandler)

    def test_get_archives_handler(self):
        """Test getting archives handler."""
        handler = OperationHandlerFactory.get_handler("archives")
        assert isinstance(handler, ArchivesOperationHandler)

    def test_get_default_handler(self):
        """Test getting default handler for unknown API."""
        handler = OperationHandlerFactory.get_handler("unknown_api")
        assert isinstance(handler, DefaultOperationHandler)

    def test_handler_is_operation_handler(self):
        """Test all handlers inherit from OperationHandler."""
        for api_name in ["resolver", "archives", "unknown"]:
            handler = OperationHandlerFactory.get_handler(api_name)
            assert isinstance(handler, OperationHandler)
