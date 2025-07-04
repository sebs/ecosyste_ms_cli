from setuptools import find_packages, setup

setup(
    name="ecosystems-cli",
    version="1.0.0",
    description="CLI for ecosyste.ms API",
    author="Sebastian Schürmann",
    author_email="sebastian.schurmann@gmail.com",
    url="https://github.com/sebs/ecosyste_ms_cli",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=[
        "click",
        "requests",
        "pyyaml",
        "rich",
    ],
    extras_require={
        "dev": ["pytest", "black", "isort", "flake8", "bandit", "complexipy"],
    },
    entry_points={
        "console_scripts": [
            "ecosystems=ecosystems_cli.cli:main",
        ],
    },
    python_requires=">=3.12",
)
