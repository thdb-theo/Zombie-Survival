from distutils.core import setup
from setuptools import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext


extensions = [
    Extension("src.cython_.angle_between", ["src/cython_/angle_between.pyx"]),
    Extension("src.cython_.collide", ["src/cython_/collide.pyx"]),
    Extension("tests.experiment.testcy", ["tests/experiment/testcy.pyx"])
]

setup(
    ext_modules=cythonize(extensions),
    cmdclass={"build_ext": build_ext},
)
