"""Includes a class for tiles"""

import random
import logging
from itertools import groupby

import pygame

from init import main; main()
from options import Options, Colours
from maths import Vector


class Tile:
    """Create a tile
    Tile.create() creates all tiles that fit in the map
    Should not be created seperately only through Tile.create()
    Params:
    x: x coordinate of the tile
    y: y coordinate of the tile
    is_solid: True if the tile is not walkable else False
    idx: the index of the tile starting at 0 in the topleft like this:
    012
    345
    678"""
    instances, solids, opens, solids_list = [], set(), set(), []
    length = Options.tile_length
    size = Vector(length, length)
    amnt_tiles = 0  # Incremented when a tile is created

    with open(Options.mappath) as file:
        file_str = file.read()
        map_ = [x == '#' for x in file_str.replace('\n', '')]

    solid_nums = set(i for i, x in enumerate(map_) if x)
    # Set of the indices of all solid tiles

    @classmethod
    def create(cls):
        """Create tiles and set some class variables when finished"""
        map_gen = iter(cls.map_)
        for y in range(0, Options.height, cls.length):
            for x in range(0, Options.width, cls.length):
                cls(x, y, next(map_gen))
        cls.solids = set(cls.solids_list)
        cls.loop_set = cls.compress_solids()

    @classmethod
    def delete(cls):
        cls.instances = []
        cls.solids_list = []
        cls.solids = set()
        cls.opens = set()
        cls.loop_set = set()
        cls.amnt_tiles = 0

    @classmethod
    def compress_solids(cls):
        """returns a comressed cls.solids to be used when drawing
        It returns a list of a tuple with the first tile in a long line of solids and
        then how many solids are after it in the line for all lines on the map
        example:
        ##..### -> [(tile.Tile object at 0x0..., 2), (tile obj..., 3)]
        It ignores open tiles

        NOTE: A new group starts at a newline
        TODO: Make it so the loop_list is the type of tile with the fewest intances

        rtype: set
        """

        splitted_map = zip(*([iter(cls.map_)] * Options.line_length))
        # Split map on every newline

        compressed_map = []
        # A compressed list with True if solid and False if open
        # Looks something like this -> [(True, 5), (False, 2), (True, 9), ...]
        for row in splitted_map:
            for group in groupby(row):
                compressed_map.append((group[0], len(list(group[1]))))

        filtered_opens = (j for i, j in compressed_map if i)  # filter open tiles
        solids_iter = iter(cls.solids_list)
        # Map solids onto compressed map
        loop_set = set()
        for length, tile in zip(filtered_opens, solids_iter):
            loop_set.add((tile, length))
            for _ in range(length - 1):
                next(solids_iter)
        return loop_set

    def __init__(self, x, y, is_solid):
        self.parent = None
        self.h, self.g, self.f = 0, 0, 0
        self.walkable = not is_solid
        self.pos = Vector(x, y)
        self.number = Tile.amnt_tiles
        Tile.amnt_tiles += 1
        if is_solid:
            Tile.solids_list.append(self)
        else:
            Tile.opens.add(self)
        Tile.instances.append(self)

    def __hash__(self):
        return self.number

    def __lt__(self, other):
        """Necesary for the heapq in astar for determeting what path to take if two tiles
        have equal cost. Current implementation favours the tile with the lowest number.
        In other words the tile furthest up, and if equal, then the one furthest to the left."""
        return self.number < other.number

    @classmethod
    def random_open_tile(cls):
        """:return: location of a random walkable tile
        The tile at the returned coordinate is walkable"""
        return random.choice(tuple(cls.opens)).pos

    def get_centre(self):
        """Return a vector of the pos in the middle of the tile
        >>> Tile.length = 20
        >>> a = Tile(0, 0, 0)
        >>> a.get_centre()
        Vector(x=10, y=10)"""
        return self.pos + Tile.length // 2

    @classmethod
    def draw_all(cls, screen):
        """Fill the screen in light tiles, then draws the solid tiles over"""
        screen.fill(Colours.LIGHT_GREY)
        length, dark_grey, draw_rect = cls.length, Colours.DARK_GREY, pygame.draw.rect
        for tile, i in cls.loop_set:
            draw_rect(screen, dark_grey, (*tile.pos, length * i, length))


if __name__ == '__main__':
    Tile.create()
    import doctest
    doctest.testmod()