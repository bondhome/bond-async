"""Setup script for bond-async."""

import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="bond_async",
    version="0.2.0",
    packages=find_packages(exclude=['tests']),

    author="Olibra LLC",
    author_email="mobiledev@olibra.io",
    description="Asynchronous Python wrapper library over Bond Local API",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="bond local api async",

    install_requires=[
        "orjson>=3.8.7",
        "aiohttp>=3.6.1"
    ],

    url="https://github.com/bondhome/bond-async",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Home Automation"
    ]
)
