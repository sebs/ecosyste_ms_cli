#!/usr/bin/env python3
"""
Script to fetch registry names from the Ecosyste.ms API and save them as YAML.
This file is used to provide allowed values for the --registry parameter in the CLI help.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


def fetch_registries() -> List[Dict[str, str]]:
    """Fetch registry names and PURL types using the ecosystems CLI."""
    try:
        result = subprocess.run(
            ["ecosystems", "packages", "get_registries", "--per-page", "200", "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
        registries = json.loads(result.stdout)
        registry_list = [{"name": registry["name"], "purl_type": registry["purl_type"]} for registry in registries]
        return sorted(registry_list, key=lambda x: x["name"])
    except subprocess.CalledProcessError as e:
        print(f"Error fetching registries: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError as e:
        print(f"Unexpected data structure: {e}", file=sys.stderr)
        sys.exit(1)


def save_registries_yaml(registries: List[Dict[str, str]], output_path: Path) -> None:
    """Save registry names and PURL types to a YAML file."""
    yaml_content = "# Auto-generated list of available registries\n"
    yaml_content += "# Generated from: https://packages.ecosyste.ms/api/v1/registries\n"
    yaml_content += "# Run: python scripts/fetch_registries.py to update\n\n"
    yaml_content += "registries:\n"

    for registry in registries:
        yaml_content += f"  - name: {registry['name']}\n"
        yaml_content += f"    purl_type: {registry['purl_type']}\n"

    output_path.write_text(yaml_content)
    print(f"✓ Saved {len(registries)} registries to {output_path}")


def main():
    """Main function."""
    # Get the project root (parent of scripts directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    apis_dir = project_root / "apis"

    # Ensure apis directory exists
    apis_dir.mkdir(exist_ok=True)

    # Fetch and save registries
    print("Fetching registries from Ecosyste.ms API...")
    registries = fetch_registries()

    output_path = apis_dir / "registries.yaml"
    save_registries_yaml(registries, output_path)


if __name__ == "__main__":
    main()
