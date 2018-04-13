"""This file defines a bullet class"""

import logging
import math

import pygame
from recordclass import recordclass

import init as _
from options import Options
from baseclass import BaseClass
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
        scale(pygame.image.load("assets/Images/Bullets/pistol_b.png"), Tile.size.scale(0.33, 0.2)),
        scale(pygame.image.load("assets/Images/Bullets/shotgun_b2.png"), Tile.size.scale(0.33, 0.2)),
        scale(pygame.image.load("assets/Images/Bullets/automatic_b.png"), Tile.size.scale(0.33, 0.2)),
        scale(pygame.image.load("assets/Images/Bullets/sniper_b2.png"), Tile.size.scale(0.33, 0.2))
    )

    sounds = (
        pygame.mixer.Sound("assets/Audio/Gunshots/pistol.wav"),
        pygame.mixer.Sound("assets/Audio/Gunshots/shotgun2.wav"),
        pygame.mixer.Sound("assets/Audio/Gunshots/automatic.wav"),
        pygame.mixer.Sound("assets/Audio/Gunshots/sniper.wav")
    )
    for sound in sounds:
        sound.set_volume(Options.volume / 2)

    dmg_func = (lambda d: max((-0.00442 * d ** 2 - 1.4273 * d + 1433.3) / Tile.length, 12),
                lambda d: (432000 * math.exp(-1 / 20 * d) + 720) /
                           ((100 * math.exp(-1 / 20 * d) + 1) * Tile.length),
                lambda d: max((-2 * d + 1080) / Tile.length, 10),
                lambda d: 36 / Tile.length * (40 * math.log(d + 40) - 100) / 1.1)

    min_bullet_dist = (Tile.length * 2, Tile.length * 3,
                       Tile.length, Tile.length * 8)
    last_bullet = None

    new_keys = (0, -1), (0, 1), (-1, 0), (1, 0)
    vel2img = dict(zip(new_keys, new_dir_func.values()))
    last_bullet_class = recordclass("bullet", "org_pos pos vel")
    # Exchange the keys of new_dir_func with new_keys

    def __init__(self, pos, vel, type_, survivor):
        if survivor.ammo_count[type_] <= 0:
            return  # Don't create bullet if there is no ammo
        try:
            dist = (Bullet.last_bullet.pos - Bullet.last_bullet.org_pos).magnitude()
            if Bullet.min_bullet_dist[type_] >= dist:
                return  # Don't create bullet if last_bullet is too close
        except AttributeError:  # If Bulle.last_bullet hasn't been updated yet. 1st bullet
            dist = None

        Bullet.sounds[type_].play()
        survivor.ammo_count[type_] -= 1
        self.type = type_
        self.orgpos = pos
        self.vel = vel
        self.dmg_drop = 1
        self.hits = set()
        Bullet.instances.add(self)
        stats["Bullets Fired"] += 1
        self.vel_as_signs = vel.signs()  # Eg. (-3, 0) -> (-1, 0)
        self.img = Bullet.vel2img[self.vel_as_signs](Bullet.images[type_])
        super().__init__(*pos, Bullet.width, Bullet.height)
        Bullet.last_bullet = Bullet.last_bullet_class(pos, pos.copy(), vel)
        logging.debug("pos: %s, vel: %s, type: %s, dist: %s, last_bullet: %s," +
                      "sign: %s, survivor pos: %s",
                      pos, vel, type_, dist, Bullet.last_bullet,
                      self.vel_as_signs, survivor.pos)

    def offscreen(self):
        return (self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x + self.width > Options.width or
                self.pos.y + self.height > Options.height)

    def calc_dmg(self):
        dist = (self.orgpos - self.pos).magnitude()
        dmg = Bullet.dmg_func[self.type](dist)
        dmg *= self.dmg_drop
        dmg *= 4 if "quad" in Drop.actives else 1
        return dmg

    @classmethod
    def update(cls, screen):
        try:
            cls.last_bullet.pos += cls.last_bullet.vel
        except AttributeError:  # If no bullets has been fired last_bullet is None
            pass
        del_bullets = set()

        for bullet in cls.instances:
            bullet.pos += bullet.vel
            screen.blit(bullet.img, bullet.pos)

            if (Tile.get_number(bullet.pos + bullet.vel) in Tile.solid_nums
                    and "trans" not in Drop.actives or bullet.offscreen()):
                del_bullets.add(bullet)
                del bullet
                continue
            for zombie in Zombie.instances - bullet.hits:
                if collide(*bullet.pos, *bullet._size, *zombie.pos, *zombie._size):
                    dmg = bullet.calc_dmg()
                    assert dmg > 0
                    zombie.health -= dmg
                    logging.debug("type %s, dmg %s, dmg_drop %s, zh %s, 4xd: %s",
                                  bullet.type, dmg, bullet.dmg_drop, zombie.health,
                                  "quad" in Drop.actives)
                    bullet.dmg_drop /= 1.1
                    if not bullet.hits:
                        stats["Bullets Hit"] += 1
                    bullet.hits.add(zombie)

        cls.instances -= del_bullets
