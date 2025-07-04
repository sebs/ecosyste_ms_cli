#!/bin/bash
# security-audit.sh - Audit all dependencies for security issues
ORG="sebs"

echo "# Security Audit for $ORG"
echo "Generated: $(date)"
echo

# Get all repos for the org
.venv/bin/python ecosystems_cli repos hosts github-owners "$ORG" -o json | jq -r '.[] | .full_name' | while read repo; do
    echo "## Checking $repo"
    # Get dependencies from the repo
    .venv/bin/python ecosystems_cli  repos lookup "https://github.com/$repo" -o json | jq -r '.dependencies[]?.package_name' | sort | uniq | while read pkg; do
        # Check each package for advisories
        advisories=$(.venv/bin/python ecosystems_cli  packages lookup-name "$pkg" -o json | jq '.advisories // []')
        if [ "$advisories" != "[]" ]; then
            echo "⚠️  $pkg has security advisories:"
            echo "$advisories" | jq -r '.[] | "   - \(.severity // "unknown"): \(.title)"'
        fi
    done
    echo
done
