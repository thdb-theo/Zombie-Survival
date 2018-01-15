from functools import partial
from random import random, randint, choice

import pygame

import init as _
from baseclass import BaseClass
from options import Options

try:
    from cython_ import collide
except ImportError:
    from python_ import collide
from miscellaneous import further_than, scale
from tile import Tile


class PickUp(BaseClass):
    """Creates a PickUp
    Params:
    x: x coordinate of the PickUp
    y: y coordinate of the PickUp
    spawn_tile: The index of the tile on which the PickUp is
    type_: A float between 0 and 1. If it is over 2/3 the PickUp is ammo else health
    Example:
    >>> tile = Tile.instances[PickUp.spawn_tiles[0]]
    >>> a = PickUp(*tile.pos, PickUp.spawn_tiles[0], type_=0.9)
    >>> a.type
    'health'

    TODO: Add more pick ups"""

    with open(Options.mappath) as file:
        spawn_tiles = [
            i for i, x in enumerate(file.read().replace('\n', '')) if x == 'P'
        ]

    init_round, left_round = 4, 4
    zombie_init_round = None

    images = {'ammo': scale(pygame.image.load('assets/Images/PickUps/ammo.png')),
              'health': scale(pygame.image.load('assets/Images/PickUps/health.png'))}
    sounds = {'ammo': pygame.mixer.Sound('assets/Audio/PickUp/ammo_short.ogg'),
              'health': pygame.mixer.Sound('assets/Audio/PickUp/health.ogg')}
    sounds['ammo'].set_volume(Options.volume)
    sounds['health'].set_volume(Options.volume)
    instances = set()

    def __init__(self, x, y, spawn_tile, type_):
        super().__init__(x, y)
        PickUp.instances.add(self)
        self.incr = randint(20, 35)
        self.spawn_tile = spawn_tile
        self.type = 'ammo' if type_ < 2 / 3 else 'health'
        PickUp.spawn_tiles.remove(spawn_tile)

    @classmethod
    def spawn(cls, survivor):
        _further_than = partial(further_than, survivor=survivor, min_dist=150)
        pos_spawn_tiles = list(filter(_further_than, cls.spawn_tiles))
        if not pos_spawn_tiles:  # If no pick-up spawn is far enough away
            if not cls.spawn_tiles:  # If all pick-up spawns are occupied, don't spawn
                return
            pos_spawn_tiles.extend(cls.spawn_tiles)
        cls.left_round -= 1
        type_ = random()
        spawn_tile = choice(pos_spawn_tiles)
        spawn_node = Tile.instances[spawn_tile]
        cls(*spawn_node.pos, spawn_tile, type_)

    @classmethod
    def update(cls, screen, survivor, total_frames):
        if cls.left_round:
            try:
                if total_frames % ((Options.fps * cls.zombie_init_round * 2) //
                                   cls.init_round) == 0:
                    cls.spawn(survivor)
            except ZeroDivisionError:
                if total_frames % Options.fps * 10 == 0:
                    cls.spawn(survivor)
        del_pick_up = set()
        for pick_up in cls.instances:
            screen.blit(cls.images[pick_up.type], pick_up.pos.as_ints())
            if collide(*pick_up.pos, *pick_up._size, *survivor.pos, *survivor._size):
                setattr(survivor, pick_up.type,
                        getattr(survivor, pick_up.type) + pick_up.incr)
                cls.sounds[pick_up.type].play()
                cls.spawn_tiles.append(pick_up.spawn_tile)
                del_pick_up.add(pick_up)
                del pick_up

        cls.instances -= del_pick_up


if __name__ == '__main__':
    Tile.create()
    import doctest
    doctest.testmod()
