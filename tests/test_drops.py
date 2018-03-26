import unittest
import sys
import os

sys.path.insert(0, os.getcwd() + "/src")
from bullet import Bullet
from maths import Vector
from survivor import Survivor
from drop import Drop, full_ammo


class TestDrops(unittest.TestCase):
    def test_quad_damage(self):
        survivor = Survivor(0, 0)
        bullet = Bullet(Vector(0, 0), Vector(3, 0), 0, survivor)
        bullet.pos += bullet.vel
        before_4x = bullet.calc_dmg()
        Drop.actives["4x"] = 1
        after4x = bullet.calc_dmg()
        self.assertEqual(after4x / before_4x, 4.0)
        self.assertTrue(after4x > before_4x)

    def test_full_ammo(self):
        survivor = Survivor(0, 0)
        survivor.ammo_count = [0, 0, 0, 0]
        full_ammo(survivor)
        self.assertEqual(survivor.ammo_count, list(survivor.init_ammo_count))
        survivor.ammo_count[0] += 1
        full_ammo(survivor)
        self.assertNotEqual(survivor.ammo_count, list(survivor.init_ammo_count))

if __name__ == "__main__":
    unittest.main()