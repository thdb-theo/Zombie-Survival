import random

import pygame

import init as _
from baseclass import BaseClass
from options import Options

try:
    from cython_ import collide
except ImportError:
    from python_ import collide
from miscellaneous import scale


def full_ammo(survivor, *_):
    """Fills the players amme to the start amount unless
    the current amme is higher than what it started with.
    For example if the amme count is: [5, 17, 12, 0] and the
    player started with [10, 8, 5, 3], the ammo will be refilled to:
    [10, 17, 12, 3]"""
    new_ammo = []
    for i, ammo in enumerate(survivor.ammo_count):
        init_ammo = survivor.init_ammo_count[i]
        if ammo < init_ammo:
            new_ammo.append(init_ammo)
        else:
            new_ammo.append(ammo)
    survivor.ammo_count = new_ammo


def quad_dmg(*_):
    Drop.actives["quad"] = Options.fps * 5


def freeze(*_):
    Drop.actives["freeze"] = Options.fps * 5


def through_walls(*_):
    Drop.actives["trans"] = Options.fps * 5


class Drop(BaseClass):
    """Drop power ups similar to power ups in call of duty
    Current power ups are double damage for 5 seconds and max ammo and
    walking through walls

    The order of the drops in all lists is:
    0th max_ammo, 1st quad damage, 2nd freeze, 3rd through_walls

    params:
    ---------------
    pos: The tile on which the power is
    type_: An integer indicating the type of the drop as its index in Drop.effects

    TODO: Add more types of power ups"""

    instances = set()

    load_img = lambda s: scale(pygame.image.load("assets/Images/Drops/%s.png" % s))
    imgs = (load_img("max_ammo"), load_img("quad_damage"),
            load_img("freeze"), load_img("through_walls"))

    load_sound = lambda s: pygame.mixer.Sound("assets/Audio/Drop/%s.ogg" % s)
    sounds = (load_sound("max_ammo"),load_sound("quad_damage"),
              load_sound("freeze"),load_sound("through_walls"))
    for sound in sounds:
        sound.set_volume(Options.volume)

    effects = full_ammo, quad_dmg, freeze, through_walls
    probability = 2/3 if Options.debug else 9/10
    actives = {}

    def __init__(self, pos, type_):
        self.type_ = type_
        self.countdown = Options.fps * 5
        Drop.instances.add(self)
        super().__init__(*pos)

    @classmethod
    def spawn(cls, pos):
        if random.random() < cls.probability:
            return
        type_ = random.randint(0, len(cls.effects) - 1)
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
                cls.effects[drop.type_](survivor)
                cls.sounds[drop.type_].play()
                del_drops.add(drop)
                continue
        cls.instances -= del_drops
        for power_up, value in tuple(cls.actives.items()):
            cls.actives[power_up] -= 1
            if value == 0:
                if power_up == "trans":
                    new_tile = survivor.get_tile().closest_open_tile()
                    survivor.pos = new_tile.pos.copy()
                    survivor.to = None
                del cls.actives[power_up]
