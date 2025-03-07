from setuptools import find_packages, setup

setup(
    name="ecosystems-cli",
    version="0.3.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "pyyaml",
        "rich",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "isort",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "ecosystems=ecosystems_cli.cli:main",
        ],
    },
    python_requires=">=3.12",
)
