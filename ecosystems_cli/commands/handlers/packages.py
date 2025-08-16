"""Handler for packages API operations."""

from typing import Any, Dict, Tuple

from .base import OperationHandler


class PackagesOperationHandler(OperationHandler):
    """Handler for packages API operations."""

    def build_params(self, operation_id: str, args: tuple, kwargs: dict) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Build parameters for packages API operations.

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
        if operation_id == "getKeyword":
            # The keyword name is a path parameter
            if args:
                path_params["keywordName"] = args[0]
            elif "keywordName" in kwargs:
                path_params["keywordName"] = kwargs.pop("keywordName")
            elif "keywordname" in kwargs:
                # Handle lowercased version from click
                path_params["keywordName"] = kwargs.pop("keywordname")

        elif operation_id == "getRegistry":
            # The registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "lookupRegistryPackage":
            # Registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "getRegistryMaintainers":
            # Registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "getRegistryMaintainer":
            # Registry name and maintainer login/UUID are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["MaintainerLoginOrUUID"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "MaintainerLoginOrUUID" in kwargs:
                    path_params["MaintainerLoginOrUUID"] = kwargs.pop("MaintainerLoginOrUUID")
                elif "maintainerloginoruuid" in kwargs:
                    path_params["MaintainerLoginOrUUID"] = kwargs.pop("maintainerloginoruuid")

        elif operation_id == "getRegistryMaintainerPackages":
            # Registry name and maintainer login/UUID are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["MaintainerLoginOrUUID"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "MaintainerLoginOrUUID" in kwargs:
                    path_params["MaintainerLoginOrUUID"] = kwargs.pop("MaintainerLoginOrUUID")
                elif "maintainerloginoruuid" in kwargs:
                    path_params["MaintainerLoginOrUUID"] = kwargs.pop("maintainerloginoruuid")

        elif operation_id == "getRegistryNamespaces":
            # Registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "getRegistryNamespace":
            # Registry name and namespace name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["namespaceName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "namespaceName" in kwargs:
                    path_params["namespaceName"] = kwargs.pop("namespaceName")
                elif "namespacename" in kwargs:
                    path_params["namespaceName"] = kwargs.pop("namespacename")

        elif operation_id == "getRegistryNamespacePackages":
            # Registry name and namespace name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["namespaceName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "namespaceName" in kwargs:
                    path_params["namespaceName"] = kwargs.pop("namespaceName")
                elif "namespacename" in kwargs:
                    path_params["namespaceName"] = kwargs.pop("namespacename")

        elif operation_id == "getRegistryPackages":
            # Registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "getRegistryPackageNames":
            # Registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "getRegistryRecentVersions":
            # Registry name is a path parameter
            if args:
                path_params["registryName"] = args[0]
            elif "registryName" in kwargs:
                path_params["registryName"] = kwargs.pop("registryName")
            elif "registryname" in kwargs:
                path_params["registryName"] = kwargs.pop("registryname")

        elif operation_id == "getRegistryPackage":
            # Registry name and package name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")

        elif operation_id == "getRegistryPackageDependentPackages":
            # Registry name and package name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")

        elif operation_id == "getRegistryPackageDependentPackageKinds":
            # Registry name and package name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")

        elif operation_id == "getRegistryPackageRelatedPackages":
            # Registry name and package name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")

        elif operation_id == "getRegistryPackageVersionNumbers":
            # Registry name and package name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")

        elif operation_id == "getRegistryPackageVersions":
            # Registry name and package name are path parameters
            if len(args) >= 2:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")

        elif operation_id == "getRegistryPackageVersion":
            # Registry name, package name, and version number are path parameters
            if len(args) >= 3:
                path_params["registryName"] = args[0]
                path_params["packageName"] = args[1]
                path_params["versionNumber"] = args[2]
            else:
                if "registryName" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryName")
                elif "registryname" in kwargs:
                    path_params["registryName"] = kwargs.pop("registryname")
                if "packageName" in kwargs:
                    path_params["packageName"] = kwargs.pop("packageName")
                elif "packagename" in kwargs:
                    path_params["packageName"] = kwargs.pop("packagename")
                if "versionNumber" in kwargs:
                    path_params["versionNumber"] = kwargs.pop("versionNumber")
                elif "versionnumber" in kwargs:
                    path_params["versionNumber"] = kwargs.pop("versionnumber")

        # For all operations, remaining kwargs are query parameters
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value

        return path_params, query_params
