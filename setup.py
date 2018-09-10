import os

from distutils.core import setup
from setuptools import find_packages

NAME = "ZombieSurvival"
DESCRIPTION = "A Zombie Survival game in pygame"
URL = "https://github.com/thdb-theo/zombie-survival"
EMAIL = "theo.tollers@gmail.com"
AUTHOR = "Theodor Tollersrud"
VERSION = "1.6.2"

with open("requirements.txt", encoding="utf-8") as file:
    REQUIRED = file.read().splitlines()

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, "README.md"), encoding="utf-8") as file:
    long_description = "\n" + file.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT"
)
