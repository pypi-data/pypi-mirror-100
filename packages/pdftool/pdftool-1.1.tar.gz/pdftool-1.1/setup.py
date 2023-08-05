from os import path
import setuptools
from setuptools import version
from pathlib import Path

setuptools.setup(
    name="pdftool",

    version=1.1,

    long_description=Path('README.md').read_text(),

    package=setuptools.find_packages(exclude=['tests', 'data'])

)
