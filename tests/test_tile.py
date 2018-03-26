import unittest
import sys
import os
sys.path.insert(0, os.getcwd() + "/src")
from tile import Tile
from maths import Vector


class TileTest(unittest.TestCase):
    def setUpClass():
        Tile.create()

    def tearDownClass():
        Tile.delete()

    def test_class_attrs(self):
        self.assertTrue(len(Tile.instances) == Tile.amnt_tiles)
        self.assertTrue(len(Tile.solids) == len(Tile.solid_nums) == len(Tile.solids_list))
        self.assertTrue(len(Tile.solids) + len(Tile.opens) == len(Tile.instances))

    def test_attrs(self):
        a = Tile.instances[0]
        self.assertEqual(a.pos, (0, 0))
        self.assertIsInstance(a.pos, Vector)
        self.assertEqual(a.number, 0)

    def test_funcs(self):
        a = Tile.instances[0]
        self.assertTrue(hasattr(a, "__hash__"))
        b = Tile.instances[1]
        self.assertTrue(b > a)


if __name__ == "__main__":
    unittest.main()