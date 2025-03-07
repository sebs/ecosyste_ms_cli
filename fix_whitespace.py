#!/usr/bin/env python3
"""Script to remove trailing whitespace from Python files."""

import os
from pathlib import Path


def fix_whitespace(file_path):
    """Remove trailing whitespace from a file."""
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Remove trailing whitespace
    fixed_lines = [line.rstrip() + "\n" for line in lines]

    # Write back to file
    with open(file_path, "w") as f:
        f.writelines(fixed_lines)

    print(f"Fixed whitespace in {file_path}")


def main():
    """Find and fix Python files."""
    root_dir = Path(__file__).parent

    # Find all Python files
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                fix_whitespace(file_path)


if __name__ == "__main__":
    main()
