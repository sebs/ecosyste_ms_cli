"""Handler for repos API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class ReposOperationHandler(OperationHandler):
    """Handler for repos API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for repos API operations.

        Args:
            operation_id: The operation identifier
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (path_params, query_params)
        """
        path_params = {}
        query_params = {}

        # Handle path parameters for specific operations
        if operation_id == "topic":
            # The topic is a path parameter
            if args:
                path_params["topic"] = args[0]
            elif "topic" in kwargs:
                path_params["topic"] = kwargs.pop("topic")

        elif operation_id == "getHost":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostOwners":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "lookupHostOwner":
            # The host name is a path parameter
            if args:
                path_params["HostName"] = args[0]
            elif "HostName" in kwargs:
                path_params["HostName"] = kwargs.pop("HostName")
            elif "hostname" in kwargs:
                path_params["HostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostOwner":
            # The host name and owner login are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["ownerLogin"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "ownerLogin" in kwargs:
                    path_params["ownerLogin"] = kwargs.pop("ownerLogin")
                elif "ownerlogin" in kwargs:
                    path_params["ownerLogin"] = kwargs.pop("ownerlogin")

        elif operation_id == "getHostOwnerRepositories":
            # The host name and owner login are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["ownerLogin"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "ownerLogin" in kwargs:
                    path_params["ownerLogin"] = kwargs.pop("ownerLogin")
                elif "ownerlogin" in kwargs:
                    path_params["ownerLogin"] = kwargs.pop("ownerlogin")

        elif operation_id == "getHostRepositories":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostRepositoryNames":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostOwnerNames":
            # The host name is a path parameter
            if args:
                path_params["hostName"] = args[0]
            elif "hostName" in kwargs:
                path_params["hostName"] = kwargs.pop("hostName")
            elif "hostname" in kwargs:
                path_params["hostName"] = kwargs.pop("hostname")

        elif operation_id == "getHostRepository":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositoryManifests":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositoryTags":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositoryTag":
            # The host name, repository name, and tag are path parameters
            if len(args) >= 3:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
                path_params["tag"] = args[2]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")
                if "tag" in kwargs:
                    path_params["tag"] = kwargs.pop("tag")

        elif operation_id == "getHostRepositoryTagManifests":
            # The host name, repository name, and tag are path parameters
            if len(args) >= 3:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
                path_params["tag"] = args[2]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")
                if "tag" in kwargs:
                    path_params["tag"] = kwargs.pop("tag")

        elif operation_id == "getHostRepositoryReleases":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositorySbom":
            # The host name and repository name are path parameters
            if len(args) >= 2:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")

        elif operation_id == "getHostRepositoryRelease":
            # The host name, repository name, and release are path parameters
            if len(args) >= 3:
                path_params["hostName"] = args[0]
                path_params["repositoryName"] = args[1]
                path_params["release"] = args[2]
            else:
                if "hostName" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostName")
                elif "hostname" in kwargs:
                    path_params["hostName"] = kwargs.pop("hostname")
                if "repositoryName" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryName")
                elif "repositoryname" in kwargs:
                    path_params["repositoryName"] = kwargs.pop("repositoryname")
                if "release" in kwargs:
                    path_params["release"] = kwargs.pop("release")

        elif operation_id == "usageEcosystem":
            # The ecosystem is a path parameter
            if args:
                path_params["ecosystem"] = args[0]
            elif "ecosystem" in kwargs:
                path_params["ecosystem"] = kwargs.pop("ecosystem")

        elif operation_id == "usagePackage":
            # The ecosystem and package are path parameters
            if len(args) >= 2:
                path_params["ecosystem"] = args[0]
                path_params["package"] = args[1]
            else:
                if "ecosystem" in kwargs:
                    path_params["ecosystem"] = kwargs.pop("ecosystem")
                if "package" in kwargs:
                    path_params["package"] = kwargs.pop("package")

        elif operation_id == "usagePackageDependencies":
            # The ecosystem and package are path parameters
            if len(args) >= 2:
                path_params["ecosystem"] = args[0]
                path_params["package"] = args[1]
            else:
                if "ecosystem" in kwargs:
                    path_params["ecosystem"] = kwargs.pop("ecosystem")
                if "package" in kwargs:
                    path_params["package"] = kwargs.pop("package")

        # For all operations, remaining kwargs are query parameters
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value

        return path_params, query_params
