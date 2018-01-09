"""This file defines a bullet class"""

import logging
import math

import pygame

import init as _
from options import Options
from baseclass import BaseClass, get_number
from drop import Drop
from survivor import Survivor
try:
    from cython_ import collide
except ImportError:
    from python_ import collide
from zombie import Zombie
from miscellaneous import stats, scale, new_dir_func
from tile import Tile


class Bullet(BaseClass):
    """Creates a Bullet
    Params:
    pos: A Vector with a x and y attribute
    vel: The constant velocity of the bullet. A Vector with a x and y velocity
    type_: The type of bullet. An int between 0 and 3"""

    width, height = 7, 9
    instances = set()
    images = (
        scale(pygame.image.load('assets/Images/pistol_b.png'), Tile.size.scale(1/3, 1/5)),
        scale(pygame.image.load('assets/Images/shotgun_b2.png'), Tile.size.scale(1/3, 1/5)),
        scale(pygame.image.load('assets/Images/automatic_b.png'), Tile.size.scale(1/3, 1/5)),
        scale(pygame.image.load('assets/Images/sniper_b2.png'), Tile.size.scale(1/3, 1/5))
    )

    dmg_func = (lambda d: max((-0.0144 * d ** 2 + 7.2 * d + 680.4) / Tile.length, 15),
                lambda d: 4680 / Tile.length * (math.e ** (-0.02 * d)) + 13,
                lambda d: (-0.36 * d + 792) / Tile.length,
                lambda d: 36 / Tile.length * (40 * math.log(d + 40) - 100) / 1.1)

    min_bullet_dist = (Tile.length * 1.11, Tile.length * 1.66,
                       Tile.length * 0.55, Tile.length * 5)
    last_bullet = None

    new_keys = (0, -1), (0, 1), (-1, 0), (1, 0)
    vel2img = dict(zip(new_keys, new_dir_func.values()))
    # Exchange the keys of new_dir_func with new_keys

    def __init__(self, pos, vel, type_, survivor):
        if survivor.ammo_count[type_] <= 0:
            return  # Don't create bullet if there is no ammo
        try:
            dist = (Bullet.last_bullet[1] - Bullet.last_bullet[0]).magnitude()
            if Bullet.min_bullet_dist[type_] >= dist:
                return  # Don't create bullet if last_bullet is too close
        except TypeError:  # If Bulle.last_bullet hasn't been updated yet. 1st bullet
            dist = None

        survivor.ammo_count[type_] -= 1
        self.type = type_
        self.orgpos = pos
        self.vel = vel
        self.dmg_drop = 1
        self.hits = set()
        Bullet.instances.add(self)
        stats['Bullets Fired'] += 1
        self.vel_as_signs = vel.signs()  # Eg. (-3, 0) -> (-1, 0)
        self.img = Bullet.vel2img[self.vel_as_signs](Bullet.images[type_])
        super().__init__(*pos, Bullet.width, Bullet.height)
        Bullet.last_bullet = pos, pos.copy(), vel
        logging.debug('pos: %s, vel: %s, type: %s, dist: %s, last_bullet: %s, sign: %s' +
                      'survivor pos: %s',
                      pos, vel, type_, dist, Bullet.last_bullet, self.vel_as_signs, survivor.pos)

    def offscreen(self):
        return (self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x + self.width > Options.width or
                self.pos.y + self.height > Options.height)

    @classmethod
    def update(cls, screen):
        try:
            cls.last_bullet[1] += cls.last_bullet[2]
        except TypeError:  # If no bullets has been fired last_bullet is None
            pass
        del_bullets = set()

        for bullet in cls.instances:
            bullet.pos += bullet.vel
            screen.blit(bullet.img, bullet.pos)

            if get_number(bullet.pos + bullet.vel) in Tile.solid_nums and 'through walls' not in Drop.actives \
                    or bullet.offscreen():
                del_bullets.add(bullet)
                del bullet
                continue
            for zombie in Zombie.instances - bullet.hits:
                if collide(*bullet.pos, *bullet._size, *zombie.pos, *zombie._size):
                    dist = (bullet.orgpos - bullet.pos).magnitude()
                    dmg = cls.dmg_func[bullet.type](dist)
                    dmg *= bullet.dmg_drop
                    dmg *= ('double damage' in Drop.actives) + 1
                    assert dmg > 0
                    zombie.health -= dmg
                    logging.debug('type %s, dist %s, dmg %s, dmg_drop %s, zh %s, 2xd: %s',
                                  bullet.type, dist, dmg, bullet.dmg_drop, zombie.health,
                                  'double damage' in Drop.actives)
                    bullet.dmg_drop /= 1.1
                    if not bullet.hits:
                        stats['Bullets Hit'] += 1
                    bullet.hits.add(zombie)

        cls.instances -= del_bullets
