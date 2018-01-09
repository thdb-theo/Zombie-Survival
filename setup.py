import os

from distutils.core import setup
# from distutils.extension import Extension
from setuptools import find_packages, Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext

NAME = 'ZombieSurvival'
DESCRIPTION = 'A Zombie Survival game in pygame'
URL = 'https://github.com/thdb-theo/zombie-survival'
EMAIL = 'theo.tollers@gmail.com'
AUTHOR = 'Theodor Tollersrud'
VERSION = '1.2.0'

REQUIRED = [
    'pygame', 'cython', 'pyqt', 'tkcolorpicker'
]

current_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

extensions = [Extension('src.cython_.angle_between', ['src/cython_/angle_between.pyx']),
              Extension('src.cython_.collide', ['src/cython_/collide.pyx']),
              Extension('tests.experiment.testcy', ['tests/experiment/testcy.pyx'])]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=('test',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    cmdclass={'build_ext': build_ext},
    ext_modules=cythonize(extensions)
)
