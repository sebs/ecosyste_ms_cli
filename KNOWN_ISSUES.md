# Known Issues

This document tracks known issues and inconsistencies in the ecosyste_ms_cli codebase.

## OpenAPI Specification Inconsistencies

### 1. Repos API: Host/Registry Naming Mismatch

**File**: `apis/repos.openapi.yaml`
**Location**: Line 225
**Issue**: Semantic inconsistency between endpoint name and operation ID

#### Details:
- **Endpoint**: `/hosts`
- **Operation ID**: `getRegistries`
- **Returns**: Array of `Host` objects
- **Summary**: "list registies" (also contains a typo)

#### Impact:
This creates confusion in the Python client where:
- The method `get_hosts()` in `api_client.py:222` calls operation `getRegistries`
- This is semantically incorrect as "hosts" (GitHub, GitLab, etc.) and "registries" (npm, PyPI, etc.) are different concepts
- The packages API correctly uses "registries" for package registries

#### Current Implementation:
The Python code in `api_client.py` correctly follows the OpenAPI specification:
```python
def get_hosts(self) -> Dict[str, Any]:
    """Get all repository hosts (repos API)."""
    if self.api_name != "repos":
        raise InvalidAPIError(f"Method get_hosts is only available for 'repos' API, not '{self.api_name}'")
    return self.call("getRegistries")  # Calls the operation ID from OpenAPI spec
```

#### Recommendation:
The OpenAPI specification should be updated to use consistent terminology:
- Change `operationId: getRegistries` to `operationId: getHosts` or `operationId: listHosts`
- Fix the typo in summary from "list registies" to "list hosts"

#### Test Coverage:
This issue is documented and tested in `tests/test_api_client_method_mismatch.py`

---

## How to Handle These Issues

1. **Do NOT change the Python implementation** - it correctly follows the OpenAPI spec
2. **Document the inconsistency** (as done here and in tests)
3. **Report to API maintainers** for fixes in the OpenAPI specification
4. **Update this document** when issues are resolved
