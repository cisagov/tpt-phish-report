"""
This is the setup module for the tpt-reports project.

Based on:

- https://packaging.python.org/distributing/
- https://github.com/pypa/sampleproject/blob/master/setup.py
- https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure
"""

# Standard Python Libraries
import codecs
from glob import glob
from os.path import abspath, basename, dirname, join, splitext

# Third-Party Libraries
from setuptools import find_packages, setup


def readme():
    """Read in and return the contents of the project's README.md file."""
    with open("README.md", encoding="utf-8") as f:
        return f.read()


# Below two methods were pulled from:
# https://packaging.python.org/guides/single-sourcing-package-version/
def read(rel_path):
    """Open a file for reading from a given relative path."""
    here = abspath(dirname(__file__))
    with codecs.open(join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(version_file):
    """Extract a version number from the given file path."""
    for line in read(version_file).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="tpt_reports",
    # Versions should comply with PEP440
    version=get_version("src/tpt_reports/_version.py"),
    description="tpt_reports Python library",
    long_description=readme(),
    long_description_content_type="text/markdown",
    # Landing page for CISA's cybersecurity mission
    url="https://www.cisa.gov/cybersecurity",
    # Additional URLs for this project per
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#project-urls
    project_urls={
        "Source": "https://github.com/cisagov/tpt-reports",
        "Tracker": "https://github.com/cisagov/tpt-reports/issues",
    },
    # Author details
    author="Cybersecurity and Infrastructure Security Agency",
    author_email="github@cisa.dhs.gov",
    license="License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        # Pick your license as you wish (should match "license" above)
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.9",
    # What does your project relate to?
    keywords="tpt technical payload testing report",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"tpt_reports": ["assets/*.png", "fonts/*.ttf"]},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
<<<<<<< HEAD
    install_requires=[
        "docopt",
        "numpy",
        "pandas",
        "reportlab",
        "schema",
        "setuptools >= 24.2.0",
        "validator-collection",
    ],
=======
    install_requires=["docopt", "schema", "setuptools"],
>>>>>>> 0da26c3a45b9a9c2a7d41ed2687b177a6f597116
    extras_require={
        # IMPORTANT: Keep type hinting-related dependencies of the dev section
        # in sync with the mypy pre-commit hook configuration (see
        # .pre-commit-config.yaml). Any changes to type hinting-related
        # dependencies here should be reflected in the additional_dependencies
        # field of the mypy pre-commit hook to avoid discrepancies in type
        # checking between environments.
        "dev": [
            "types-docopt",
            "types-setuptools",
        ],
        "test": [
            "coverage",
            "coveralls",
            "pre-commit",
            "pytest-cov",
            "pytest",
        ],
    },
    # Conveniently allows one to run the CLI tool as `tpt-reports`
    entry_points={"console_scripts": ["tpt-reports = tpt_reports.tpt_reports:main"]},
)
