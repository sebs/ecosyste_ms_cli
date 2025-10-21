"""Utility for parsing Package URLs (PURLs)."""

import re
from typing import Optional, Tuple


def parse_purl(purl: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse a Package URL (PURL) to extract ecosystem and package name.

    PURL format: pkg:type/namespace/name@version?qualifiers#subpath

    Examples:
        pkg:npm/fsa -> ('npm', 'fsa')
        pkg:npm/@types/node -> ('npm', '@types/node')
        pkg:pypi/django@4.2.0 -> ('pypi', 'django')
        pkg:maven/org.apache.commons/commons-lang3 -> ('maven', 'org.apache.commons/commons-lang3')

    Args:
        purl: Package URL string

    Returns:
        Tuple of (ecosystem, package_name) or (None, None) if parsing fails
    """
    if not purl:
        return None, None

    # Basic PURL pattern: pkg:type/...rest
    # We want to extract type (ecosystem) and the package path
    pattern = r"^pkg:([^/]+)/(.+?)(?:@[^?#]*)?(?:\?[^#]*)?(?:#.*)?$"
    match = re.match(pattern, purl)

    if not match:
        return None, None

    ecosystem = match.group(1)
    package_name = match.group(2)

    return ecosystem, package_name
