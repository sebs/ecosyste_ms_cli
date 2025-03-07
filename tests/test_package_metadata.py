"""Tests for package metadata."""

import re
from pathlib import Path


def test_license_in_setup():
    """Test that the license in setup.py matches the LICENSE file."""
    # Get the project root directory
    project_root = Path(__file__).parent.parent

    # Read setup.py file
    setup_path = project_root / "setup.py"
    with open(setup_path, 'r') as f:
        setup_content = f.read()

    # Extract license from setup.py using regex
    license_match = re.search(r'license\s*=\s*["\']([^"\']*)["\'\s]', setup_content)
    setup_license = license_match.group(1) if license_match else None

    # Extract license classifier from setup.py
    classifier_match = re.search(r'"License\s*::\s*OSI\s*Approved\s*::\s*([^"\']*)\s*License"', setup_content)
    license_classifier = classifier_match.group(1) if classifier_match else None

    # Read LICENSE file
    license_path = project_root / "LICENSE"
    with open(license_path, 'r') as f:
        license_content = f.read().strip()

    # Check if LICENSE file contains MIT license text
    is_mit_license = "MIT License" in license_content

    # Assert license in setup.py matches LICENSE file
    assert setup_license == "MIT", f"License in setup.py should be 'MIT', got '{setup_license}'"
    assert license_classifier.strip() == "MIT", f"License classifier should be 'MIT', got '{license_classifier}'"
    assert is_mit_license, "LICENSE file should contain MIT license text"
