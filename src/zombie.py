import logging
import math
from functools import partial
from random import randint, choice
import threading

import pygame

from init import main; main()
from options import Options, Colours
from astar import AStar
from baseclass import BaseClass
from pickup import PickUp
from maths import Vector
try:
    from cython_ import angle_between
except ImportError:
    from python_ import angle_between
from miscellaneous import stats, rotated, further_than, avg_zmb_poses, scale
from tile import Tile
from drop import Drop


def _get_vel_list():
    """Get the tuple from which a zombie's vel will be determined
    Example:
    >>> Options.speed = 4
    >>> Tile.length = 32
    >>> _get_vel_list()
    (2, 4, 2, 1)
    >>> Options.speed = 9
    >>> _get_vel_list()
    (4, 8, 4, 2)
    """
    base_speed = Options.speed / 4
    ts = base_speed * 2, base_speed * 3, base_speed * 2, base_speed

    def func(x):
        def cond(x):
            return Tile.length / x % 1 == 0

        iterable = (Tile.length // x for x in range(1, Tile.length + 1) if cond(x))
        return min(iterable, key=lambda k: abs(k - x))

    return tuple(map(func, ts))


class Zombie(BaseClass):
    """Create a Zombie
    Params:
    x: x coordinate of zombie
    y: y coordinate of zombie"""
    instances = set()  # set of all zombies
    with open(Options.mappath) as file:
        spawn_tiles = [
            i for i, x in enumerate(file.read().replace('\n', '')) if x == 'Z'
        ]
    imgs = tuple(scale(pygame.image.load('assets/Images/zombie{}.png'.format(i)))
                 for i in range(1, 5))

    speed_tuple = _get_vel_list()
    logging.debug('zombie speeds: %s', speed_tuple)
    health_func_tuple = (lambda h: h, lambda h: h / 2,
                         lambda h: h * 1.2, lambda h: h * 4)
    new_round_song = pygame.mixer.Sound('assets/Audio/new_round_short.ogg')
    new_round_song.set_volume(Options.volume)
    new_round_song_length = int(new_round_song.get_length())
    base_health = 100
    attack_range = Tile.length * 1.3  # Max distance from zombie for an attack, in pixels
    level = 1
    init_round = 0 if Options.no_zombies else 10  # How many zombies spawn on round 1
    left_round = init_round
    PickUp.zombie_init_round = init_round
    cool_down, play_song = False, True
    spawn_interval = Options.fps * 2  # Frames between spawns, decreses exponentially
    _info_font = pygame.font.SysFont('Monospace', Tile.length // 4)
    text = _info_font.render('avg zmb pos', 1, Colours.WHITE)
    AStarThread = None

    def __init__(self, x, y):
        self.direction = math.pi
        type_ = choice(range(4))
        self.type = type_
        self.org_img = Zombie.imgs[type_]
        self.img = self.org_img
        self.speed = Zombie.speed_tuple[type_]
        self.health_func = Zombie.health_func_tuple[type_]
        self.health = self.health_func(Zombie.base_health)
        self.org_health = self.health
        self.angle_to_vel = {0: (self.speed, 0),
                             math.pi / 2: (0, -self.speed),
                             math.pi: (-self.speed, 0),
                             math.pi * 3 / 2: (0, self.speed)}
        self.vel = Vector(0, 0)
        super().__init__(x, y)
        Zombie.instances.add(self)
        self.path = []
        self.last_angle = 0.
        self.path_colour = Colours.random(s=(0.5, 1))
        logging.debug('speed: %s type. %s', self.speed, self.type)

    def set_target(self, next_tile):
        self.to = next_tile.pos
        angle = angle_between(*self.pos, *next_tile.pos)
        assert angle % (math.pi / 2) == 0., 'angle: %s to: %s pos: %s mod %s' % (
                                            angle, self.to, self.pos, angle % math.pi / 2)
        self.vel = Vector(*self.angle_to_vel[angle])

    @classmethod
    def update(cls, screen, survivor):
        del_zmbs = set()
        avg_pos = Vector(0, 0)
        for zmb in cls.instances:
            if zmb.health <= 0.:
                Drop.spawn(zmb.pos)
                del_zmbs.add(zmb)
                stats['Zombies Killed'] += 1
                continue

            avg_pos += zmb.centre
            screen.blit(zmb.img, zmb.pos)
            zmb.health_bar(surface=screen)  # Health bar with rounded edges
            if Options.debug:
                for tile in zmb.path:
                    pygame.draw.circle(screen, zmb.path_colour, tile.get_centre(), Tile.length // 3)

            zmb_to_survivor_dist = (survivor.pos - zmb.pos).magnitude()

            if zmb_to_survivor_dist <= cls.attack_range:
                survivor.health -= 0.4

            if zmb.to is not None:  # if the zombie is not next to the player
                angle = angle_between(*zmb.pos, *(zmb.to + zmb.vel))
                if zmb.pos == zmb.to:  # If the zombie is directly on a tile
                    zmb.to = None  # Trigger A-Star, not run between tiles for performance
                else:
                    zmb.pos += zmb.vel
                if zmb.direction != angle:  # New direction, frame after a turn
                    zmb.rotate(angle)

            if cls.AStarThread is not None and threading.active_count() >= 2:
                # Finish the previous astar
                
                cls.AStarThread.join()

            if zmb.to is None and zmb_to_survivor_dist > Tile.length:
                cls.AStarThread = threading.Thread(target=AStar(zmb, survivor).solve,
                                                   daemon=True)
                cls.AStarThread.start()
        cls.instances -= del_zmbs
        if not Options.debug:
            return
        try:
            avg_pos //= len(cls.instances)
        except ZeroDivisionError:
            return
        pygame.draw.circle(screen, Colours.BLUE, avg_pos, Tile.length // 4)
        text_rect = cls.text.get_rect(center=avg_pos)
        screen.blit(cls.text, text_rect)
        avg_zmb_poses.append(avg_pos)

    @classmethod
    def spawn(cls, totalframes, survivor):
        """Spawning and rounds"""
        if Options.no_zombies:
            return

        if cls.left_round and not cls.cool_down:
            if totalframes % cls.spawn_interval == 0:
                cls.left_round -= 1
                if cls.play_song:
                    # filenanes are numbered in hexadecimal
                    file_nr = format(randint(0, 19), 'x')
                    sound = pygame.mixer.Sound(
                        'assets/Audio/zmb_spawn{}.wav'.format(file_nr)
                    )
                    sound.set_volume(Options.volume)
                    sound.play()
                cls.play_song = not cls.play_song  # Loop True and False
                further_than_ = partial(
                    further_than, survivor=survivor, min_dist=150)
                valid_tiles = list(filter(further_than_, cls.spawn_tiles))
                if not valid_tiles:
                    valid_tiles.extend(cls.spawn_tiles)
                spawn_idx = choice(valid_tiles)
                spawn_node = Tile.instances[spawn_idx]
                cls(*spawn_node.pos)
                logging.debug('spawn_idx: %s, spawn_node: %s, valid: %s, survivor: %s',
                              spawn_idx, spawn_node.pos, valid_tiles, survivor.pos)
        elif not (cls.instances or cls.cool_down):  # Round is over, start cooldown
            cls.cool_down = totalframes + Options.fps * cls.new_round_song_length
            cls.new_round_song.play()
            pygame.mixer.music.pause()
            cooldown_time = cls.cool_down - totalframes
            logging.debug('Round over, start cooldown; cooldown: %s frames, %s sec',
                          cooldown_time, cooldown_time // Options.fps)

        elif totalframes == cls.cool_down:  # Cooldown is over, start round
            pygame.mixer.music.unpause()
            cls.cool_down = False
            cls.base_health *= 1.16
            cls.init_round = 10 + cls.level * 3
            cls.left_round = cls.init_round
            cls.level += 1
            cls.spawn_interval //= 1.14
            PickUp.zombie_init_round = cls.init_round
            PickUp.init_round = cls.level // 2 + 3
            PickUp.left_round = PickUp.init_round
            logging.debug('level: %s, base health: %s, Zombies: %s, Pick-Ups: %s, Interval: %s',
                          cls.level, cls.base_health, cls.init_round, PickUp.init_round, cls.spawn_interval)

    def rotate(self, new_dir):
        """Rotate self.img, set self.direction to new_dir
        :param new_dir: The angle to rotate self clockwise from the x-axis in radians"""
        self.img = rotated(self.org_img, new_dir)
        self.direction = new_dir

    def health_bar(self, surface):
        """Draw a health bar with rounded egdes above the zombie"""
        colour = 170, 0, 0
        rect = pygame.Rect(
            *(self.pos - (0, 12)), self.width * self.health / self.org_health, self.height / 6
        )
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0, 0
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))

        corners = zeroed_rect.inflate(-6, -6)
        for attribute in ('topleft', 'topright', 'bottomleft', 'bottomright'):
            pygame.draw.circle(image, colour, getattr(corners, attribute), 3)
        image.fill(colour, zeroed_rect.inflate(-6, 0))
        image.fill(colour, zeroed_rect.inflate(0, -6))

        surface.blit(image, rect)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    for i in range(12, 100, 12):
        for f in range(1, 100):
            _divs_of_tl = [i // x for x in range(1, i)
                           if i / x % 1 == 0]
            Speed = min(_divs_of_tl, key=lambda x: abs(x - 240 / f))
            Options.speed = Speed
            Tile.length = i
            a = _get_vel_list()
            if len(set(a)) == 3 and max(a) != Speed:
                print(a, i, f, Speed)
