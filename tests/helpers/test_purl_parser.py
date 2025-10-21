"""Tests for PURL parser."""

from ecosystems_cli.helpers.purl_parser import parse_purl


def test_parse_purl_simple():
    """Test parsing a simple PURL."""
    ecosystem, package_name = parse_purl("pkg:npm/fsa")
    assert ecosystem == "npm"
    assert package_name == "fsa"


def test_parse_purl_scoped():
    """Test parsing a scoped package PURL."""
    ecosystem, package_name = parse_purl("pkg:npm/@babel/traverse")
    assert ecosystem == "npm"
    assert package_name == "@babel/traverse"


def test_parse_purl_with_version():
    """Test parsing a PURL with version."""
    ecosystem, package_name = parse_purl("pkg:pypi/django@4.2.0")
    assert ecosystem == "pypi"
    assert package_name == "django"


def test_parse_purl_with_namespace():
    """Test parsing a PURL with namespace (Maven style)."""
    ecosystem, package_name = parse_purl("pkg:maven/org.apache.commons/commons-lang3")
    assert ecosystem == "maven"
    assert package_name == "org.apache.commons/commons-lang3"


def test_parse_purl_with_qualifiers():
    """Test parsing a PURL with qualifiers."""
    ecosystem, package_name = parse_purl("pkg:npm/fsa@1.0.0?arch=x86_64")
    assert ecosystem == "npm"
    assert package_name == "fsa"


def test_parse_purl_with_subpath():
    """Test parsing a PURL with subpath."""
    ecosystem, package_name = parse_purl("pkg:npm/fsa@1.0.0#some/subpath")
    assert ecosystem == "npm"
    assert package_name == "fsa"


def test_parse_purl_empty():
    """Test parsing an empty PURL."""
    ecosystem, package_name = parse_purl("")
    assert ecosystem is None
    assert package_name is None


def test_parse_purl_none():
    """Test parsing None."""
    ecosystem, package_name = parse_purl(None)
    assert ecosystem is None
    assert package_name is None


def test_parse_purl_invalid():
    """Test parsing an invalid PURL."""
    ecosystem, package_name = parse_purl("not-a-purl")
    assert ecosystem is None
    assert package_name is None


def test_parse_purl_missing_package():
    """Test parsing a PURL without package name."""
    ecosystem, package_name = parse_purl("pkg:npm/")
    assert ecosystem is None
    assert package_name is None
