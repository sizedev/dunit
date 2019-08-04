import os
import codecs
import re

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), "r") as f:
        return f.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="dunit",
    version=find_version("dunit", "__init__.py"),
    description="Decimal based unit conversion",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    keywords="physical quantities unit conversion science decimal",
    author="Natalie Fearnley",
    author_email="nfearnley@gmail.com",
    url="https://github.com/nfearnley/dunit",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: MIT LICENSE",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries"
    ]
)
