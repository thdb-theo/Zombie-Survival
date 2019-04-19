import unittest
import math
from random import random
from collections import Iterable
import sys
import os
sys.path.insert(0, os.getcwd() + "/src")
from maths import Vector


class TestVector(unittest.TestCase):
    def test_creation(self):
        v = Vector(3, 5.3)
        self.assertTrue(isinstance(v.x, int))
        self.assertTrue(isinstance(v.y, float))

    def test_get_and_setitem(self):
        v = Vector(3, 5.3)
        self.assertEqual(v.x, v[0])
        self.assertEqual(v.y, v[1])
        v.x = 3.2
        v.y = 5
        self.assertEqual(v.x, v[0])
        self.assertEqual(v.y, v[1])
        v[0] = 0.9
        self.assertEqual(v.x, v[0])

    def test_iter(self):
        v = Vector(2.0, 5.0)
        self.assertTrue(len(v) == 2)
        self.assertIsInstance(v, Iterable)
        self.assertTrue(5.0 in v)

    def test_cmp(self):
        v1 = Vector(4.3, 5.2)
        v2 = Vector(6.1, 2.8)
        self.assertFalse(v1 == v2)
        self.assertTrue(v1 != v2)
        self.assertTrue(Vector(2.0, 1.0) == Vector(2, 1))
        self.assertTrue(v1 > v2)
        self.assertTrue(v1 == (4.3, 5.2))

    def test_elem_wise(self):
        v1 = Vector(5, 2)
        v2 = Vector(1, 2)
        self.assertEqual(v1 + v2, v2 + v1)
        self.assertEqual(v1 + v2, (6, 4))
        self.assertEqual(v1.scale(*v2), (5, 4))
        v1 += v2
        self.assertEqual(v1, (6, 4))

    def test_funcs(self):
        v1 = Vector(5.3, 2.0)
        self.assertEqual(v1.as_ints(), Vector(5, 2))
        v2 = v1.copy()
        v2.x = 4.7
        self.assertNotEqual(v1.x, 4.7)
        v = Vector(6, 8)
        self.assertEqual(abs(v), v.magnitude(), 10.0)
        self.assertEqual(v.magnitude_squared(), v.magnitude() ** 2)
        self.assertEqual(abs(v), math.sqrt(v.magnitude_squared()))
        v.y = -5.3
        self.assertEqual(v.signs(), (1, -1))
        v.x = 0
        self.assertEqual(v.signs(), (0, -1))
        v1 = Vector(4.0, 2.0)
        v2 = Vector(3.0, 1.0)
        self.assertEqual((v1-v2).manhattan_dist(), 2)
        v2.x = 2.0
        self.assertEqual((v1-v2).manhattan_dist(), 3)
        self.assertEqual((v1-v1).manhattan_dist(), 0)
        v3 = Vector(1, 0)
        self.assertAlmostEqual(v3.rotated(math.pi/2), Vector(0, 1))
        self.assertAlmostEqual(v3.rotated(-math.pi/2), Vector(0, -1))
        v4 = Vector(2, 2)
        self.assertAlmostEqual(v4.rotated(math.pi), Vector(-2, -2))
        v5 = Vector(random(), random())
        self.assertAlmostEqual(v5.rotated(2*math.pi), v5)


if __name__ == "__main__":
    unittest.main(verbosity=3)
