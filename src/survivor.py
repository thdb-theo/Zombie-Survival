import logging
from math import pi

import pygame

import init as _
from options import Options
from baseclass import BaseClass
from maths import Vector
from miscellaneous import rotated, scale
from tile import Tile

dir2chr = {0: "e", pi: "w", pi / 2: "n", pi * 3 / 2: "s"}
# Convert dir in radians to cardinal direction (nsew) because of file names


class Survivor(BaseClass):
    """Create the survivor
    Params:
    x: the x coordinate of the survivor
    y: the y coordinate of the survivor"""
    guns = (scale(pygame.image.load("assets/Images/Weapons/pistol2.png"), Tile.size.scale(1/2, 1/4)),
            scale(pygame.image.load("assets/Images/Weapons/shotgun.png"), Tile.size.scale(1/2, 1/4)),
            scale(pygame.image.load("assets/Images/Weapons/automatic2.png"), Tile.size.scale(1/2, 1/4)),
            scale(pygame.image.load("assets/Images/Weapons/sniper.png"), Tile.size.scale(1/2, 1/4)))
    imgs = {d: scale(pygame.image.load(
        "assets/Images/Players/player_{0}_{1}.png"
            .format(Options.gender, d))) for d in "nsew"}

    def __init__(self, x, y):
        self.current_gun = 0
        self.direction = pi * 3 / 1/2
        self.img = Survivor.imgs[dir2chr[self.direction]]
        super().__init__(x, y)
        self.health = 100 << 10 * Options.debug  # 100 if not debug, 10*2**10 if debug
        self.vel = Vector(0, 0)
        self.init_ammo_count = 100, 50, 150, 50
        self.ammo_count = list(self.init_ammo_count)

    def movement(self):
        """If survivor is between two tiles, or self.to hasn"t been updated:
              if survivor is on tile: Set self.to to None
              if survivor is between tile: Add self.vel to self.pos (Move)"""
        if self.to is not None:
            if self.pos == self.to:
                self.to = None
            else:
                self.pos += self.vel

    def draw(self, screen):
        """Draw survivor and survivor"s gun"""
        screen.blit(self.img, self.pos.as_ints())
        w = self.width
        h, q = w >> 1, w >> 2  # fractions of width for placing gun_img
        gun_pos = {pi: (-q, h), 0: (h + q, h), pi * 3 / 2: (h, w), pi / 2: (h, -h)}
        gun_img = Survivor.guns[self.current_gun]
        gun_img_rotated = rotated(gun_img, self.direction)
        screen.blit(gun_img_rotated, self.pos + gun_pos[self.direction])

    def rotate(self, new_dir):
        """If new_dir isn"t self.direction, update self.img to new_dir
        :param new_dir: direction of player in radians"""
        if self.direction != new_dir:
            self.img = Survivor.imgs[dir2chr[new_dir]]
            self.direction = new_dir

    @property
    def ammo(self):
        """Returns the ammo of the survivor"s current gun
        >>> a = Survivor(0, 0)
        >>> a.current_gun = 0
        >>> a.ammo
        100
        >>> a.current_gun = 2
        >>> a.ammo
        150"""
        return self.ammo_count[self.current_gun]

    @ammo.setter
    def ammo(self, value):
        """Set the ammo of survivors current_gun to value"""
        self.ammo_count[self.current_gun] = value

    def set_target(self, next_tile):
        """Set the tile to which the survivor will be moving to next_tile"""
        self.to = next_tile.pos
        logging.debug("self.pos: %s, self.to: %s", self.to, self.pos)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
