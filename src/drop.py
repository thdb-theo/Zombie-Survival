import random
import logging

import pygame

from init import main; main()
from options import Options
from baseclass import BaseClass
from survivor import Survivor
try:
    from cython_ import collide
except ModuleNotFoundError:
    from python_ import collide
from tile import Tile
from miscellaneous import scale


def full_ammo():
    new_ammo = []
    for i, ammo in enumerate(Survivor.ammo_count):
        init_ammo = Survivor.init_ammo_count[i]
        if ammo < init_ammo:
            new_ammo.append(init_ammo)
        else:
            new_ammo.append(ammo)
    Survivor.ammo_count = new_ammo


def double_dmg():
    Survivor.power_ups['double_dmg'] = [True, Options.fps * 5]


class Drop(BaseClass):
    """Drop power ups similar to power ups in call of duty
    Current power ups are double damage for 5 seconds and max ammo
    params:
    ---------------
    pos: The tile on which the power is
    type_: The type of power up as an integer

    TODO: Add more types of power ups"""

    instances = set()
    imgs = (scale(pygame.image.load('assets/Images/max_ammo.png')),
            scale(pygame.image.load('assets/Images/double_damage.png')))
    effects = full_ammo, double_dmg

    def __init__(self, pos, type_):
        self.pos = pos
        self.type_ = type_
        self.countdown = Options.fps * 5
        Drop.instances.add(self)
        super().__init__(*pos)

    @classmethod
    def spawn(cls, pos):
        if random.random() < 0.95:
            return
        type_ = random.randint(0, 1)
        cls(pos, type_)

    @classmethod
    def update(cls, screen, survivor):
        del_drops = set()
        for drop in cls.instances:
            drop.countdown -= 1
            if drop.countdown == 0:
                del_drops.add(drop)
                continue
            screen.blit(cls.imgs[drop.type_], drop.pos)
            if collide(*drop.pos, *drop._size, *survivor.pos, *survivor._size):
                cls.effects[drop.type_]()
                del_drops.add(drop)
                continue
        cls.instances -= del_drops
        for power_up, value in Survivor.power_ups.items():
            if value[0]:
                Survivor.power_ups[power_up][1] -= 1
                if Survivor.power_ups[power_up][1] == 0:
                    Survivor.power_ups[power_up] = [False, False]
