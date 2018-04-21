import logging
from math import pi, radians
from recordclass import recordclass

import pygame

import init as _
from options import Options
from baseclass import BaseClass
from maths import Vector
from miscellaneous import rotated, scale
from tile import Tile
from drop import Drop

dir2chr = {0: "e", pi: "w", pi * 0.5: "n", pi * 1.5: "s"}
# Convert dir in radians to cardinal direction (nsew) because of file names


class Survivor(BaseClass):
    """Create the survivor
    Params:
    x: the x coordinate of the survivor
    y: the y coordinate of the survivor"""
    guns = (scale(pygame.image.load("assets/Images/Weapons/pistol2.png"), Tile.size.scale(0.5, 0.25)),
            scale(pygame.image.load("assets/Images/Weapons/shotgun.png"), Tile.size.scale(0.5, 0.25)),
            scale(pygame.image.load("assets/Images/Weapons/automatic2.png"), Tile.size.scale(0.5, 0.25)),
            scale(pygame.image.load("assets/Images/Weapons/sniper.png"), Tile.size.scale(0.5, 0.25)))
    imgs = {d: scale(pygame.image.load(
        "assets/Images/Players/player_{0}_{1}.png"
            .format(Options.gender, d))) for d in "nsew"}
    human_fov = radians(130)
    # Information on the internet on the FOV varies vastly. From 100 deg to 200 deg
    # Some sources include our far peripheral vision, some don't, for example.
    # I found that 130 deg looks natural

    lower, upper, n_points = -human_fov / 2, human_fov / 2, Options.n_points

    angle_linspace = []
    for x in range(n_points):
        angle_linspace.append(lower + x * (upper - lower) / n_points)
        # Create an evenly spaced range of floats between lower and upper.
        # Equivalent to numpy.linspace(lower, upper, length)

    right_facing_vector = Vector(Options.line_increment, 0)
    surface = pygame.Surface(Options.screen_size, pygame.SRCALPHA)
    if pygame.display.get_surface() is not None:  # Only if the screen has been created
        surface.convert()
    darkness_rect = pygame.Rect(0, 0, Options.width, Options.height)
    darkness_colour = (0, 0, 0, Options.night_darkness)
    torch_colour = (0, 0, 0, Options.torch_darkness)

    def __init__(self, x, y):
        self.current_gun = 0
        self.direction = pi / 2
        self.img = Survivor.imgs[dir2chr[self.direction]]
        super().__init__(x, y)
        self.health = 100 << 10 * Options.debug  # 100 if not debug, else 10*2**10
        self.vel = Vector(0, 0)
        self.init_ammo_count = 100, 50, 150, 50
        self.ammo_count = list(self.init_ammo_count)

    def update(self, screen):
        self.movement()
        self.draw(screen)
        if Options.night:
            self.night_mode(screen)

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
        gun_pos = {pi: (-q, h), 0: (h + q, h), pi * 1.5: (h, w), pi * 0.5: (h, -h)}
        gun_img = Survivor.guns[self.current_gun]
        gun_img_rotated = rotated(gun_img, self.direction)
        screen.blit(gun_img_rotated, self.pos + gun_pos[self.direction])

    def rotate(self, new_dir):
        """If new_dir isn't self.direction, update self.img to new_dir
        :param new_dir: direction of player in radians"""
        if self.direction != new_dir:
            self.img = Survivor.imgs[dir2chr[new_dir]]
            self.direction = new_dir

    @property
    def ammo(self):
        """Returns the ammo of the survivor's current gun
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
        """Set the ammo of survivor's current_gun to value"""
        self.ammo_count[self.current_gun] = value

    def set_target(self, next_tile):
        """Set the tile to which the survivor will be moving to next_tile"""
        self.to = next_tile.pos
        logging.debug("self.pos: %s, self.to: %s", self.to, self.pos)

    def night_mode(self, screen):
        points = [self.get_centre()]
        line = recordclass("line", "pos angle")
        v = Survivor.right_facing_vector
        if "trans" in Drop.actives:
            for i in (0, -1):
                angle = Survivor.angle_linspace[i]
                vector = v.rotated(-self.direction-angle)
                p = vector.scale(max(Options.width, Options.height))
                # scale it by width or height depending on which one is bigger
                # To ensure that the point is outside of the screen
                points.append(p)
        else:
            for angle in Survivor.angle_linspace:
                this_line = line(self.get_centre(), self.direction + angle)
                num = Tile.get_number(this_line.pos)
                increment_vector = v.rotated(-this_line.angle)
                # -this_line.angle because of flipped y-axis
                while num not in Tile.solid_nums and Tile.on_screen(self.direction, num):
                    this_line.pos += increment_vector
                    num = Tile.get_number(this_line.pos)
                points.append(this_line.pos)
        pygame.draw.rect(Survivor.surface, Survivor.darkness_colour, Survivor.darkness_rect)
        pygame.draw.polygon(Survivor.surface, Survivor.torch_colour, points)
        screen.blit(Survivor.surface, (0, 0))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
