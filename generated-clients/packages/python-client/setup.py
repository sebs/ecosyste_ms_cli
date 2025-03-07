# coding: utf-8

"""
    Ecosyste.ms: Packages

    An open API service providing package, version and dependency metadata of many open source software ecosystems and registries.

    The version of the OpenAPI document: 1.1.0
    Contact: support@ecosyste.ms
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "ecosystems-packages-client"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3 >= 1.25.3, < 3.0.0",
    "python-dateutil >= 2.8.2",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Ecosyste.ms: Packages",
    author="Ecosyste.ms",
    author_email="support@ecosyste.ms",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "Ecosyste.ms: Packages"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="CC-BY-SA-4.0",
    long_description_content_type='text/markdown',
    long_description="""\
    An open API service providing package, version and dependency metadata of many open source software ecosystems and registries.
    """,  # noqa: E501
    package_data={"ecosyste_ms_cli.clients.packages": ["py.typed"]},
)