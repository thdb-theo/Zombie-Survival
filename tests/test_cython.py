import unittest
import math
from collections import namedtuple
from random import randint, random
import sys
import os
sys.path.insert(0, os.getcwd() + "/src")

try:
    from cython_ import angle_between as cyangle_between, collide as cycollide
    no_cython = False
except ImportError:
    no_cython = True
from python_ import angle_between as pyangle_between, collide as pycollide

rect = namedtuple("rect", "x y w h")
point = namedtuple("point", "x y")


class TestCython(unittest.TestCase):
    @unittest.skipIf(no_cython, "Cython isn't available")
    def test_cython_equal_python(self):
        args = 0, randint(1, 100000), -randint(1, 100000), random()
        self.assertTrue(math.isclose(cyangle_between(*args), pyangle_between(*args), abs_tol=1e-10))
        self.assertEqual(cycollide(*args, *args), pycollide(*args, *args))

    @unittest.skipIf(no_cython, "Cython isn't available")
    def test_collide(self):
        rect1 = rect(x=0, y=0, w=3, h=3)
        rect2 = rect(x=1, y=1, w=3, h=3)
        self.assertTrue(cycollide(*rect1, *rect2))
        self.assertTrue(cycollide(*rect2, *rect1))

        rect1 = rect(x=0, y=0, w=3, h=3)
        self.assertTrue(cycollide(*rect1, *rect1))

    @unittest.skipIf(no_cython, "Cython isn't available")
    def test_angle_between(self):
        a = point(1, 5)
        b = point(8, 0)
        self.assertEqual(cyangle_between(*a, *b), 0.6202494859828215)
        a, b = point(1, 0), point(1, 1)
        self.assertEqual(cyangle_between(*a, *b), math.pi * 3 / 2)


if __name__ == "__main__":
    unittest.main()