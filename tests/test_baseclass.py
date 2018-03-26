import unittest
import sys
import os
sys.path.insert(0, os.getcwd() + "/src")
from baseclass import BaseClass
from tile import Tile
from maths import Vector


class BaseClassTest(unittest.TestCase):
    def setUpClass():
        Tile.create()

    def tearDownClass():
        Tile.delete()

    def test_creation(self):
        a = BaseClass(3, 2)
        b = BaseClass(2, 6, 9, 3)
        self.assertEqual(a.width, Tile.length)
        self.assertNotEqual(b.width, Tile.length)
        self.assertIsNone(b.to)
        self.assertIsInstance(a.pos, Vector)
        self.assertIsInstance(a._size, Vector)
        self.assertEqual(a._size, (a.width, a.height))

    def test_funcs(self):
        a = BaseClass(x=1, y=1, width=2, height=2)
        self.assertEqual(a.centre, (2, 2))
        self.assertIsInstance(a.centre, Vector)
        b = BaseClass(x=0, y=0)
        self.assertEqual(b.get_number(), 0)
        self.assertIs(b.get_tile(), Tile.instances[0])


if __name__ == "__main__":
    unittest.main()