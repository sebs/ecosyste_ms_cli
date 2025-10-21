"""Tests for package metadata."""

import sys
from pathlib import Path

# Use tomllib for Python 3.11+ or tomli for earlier versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


def test_license_in_setup():
    """Test that the license in pyproject.toml matches the LICENSE file."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Read pyproject.toml file
    pyproject_path = project_root / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)

    # Extract license from pyproject.toml
    project_license = pyproject_data.get("project", {}).get("license")

    # Read LICENSE file
    license_path = project_root / "LICENSE"
    with open(license_path, "r") as f:
        license_content = f.read().strip()

    # Check if LICENSE file contains MIT license text
    is_mit_license = "MIT License" in license_content

    # Assert license in pyproject.toml matches LICENSE file
    assert project_license == "MIT", f"License in pyproject.toml should be 'MIT', got '{project_license}'"
    assert is_mit_license, "LICENSE file should contain MIT license text"
