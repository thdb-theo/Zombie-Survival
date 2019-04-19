"""Includes a class for tiles"""

import random
from itertools import groupby
from textwrap import dedent
from typing import Container

import pygame

import init as _
from options import Options
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
    instances, solids, opens, solids_list, loop_set = [], set(), set(), [], set()
    length = Options.tile_length
    size = Vector(length, length)
    amnt_tiles = 0  # Incremented when a tile is created

    with open(Options.mappath) as file:
        file_str = file.read()
        map_ = [x == "#" for x in file_str.replace("\n", "")]

    solid_nums = {i for i, x in enumerate(map_) if x}

    # Set of the indices of all solid tiles

    @classmethod
    def create(cls):
        """Create tiles and set some class variables when finished"""
        error_msg = """len(cls.map_) is not equal to the amount of
        tiles vertically multiplied by the amount of tiles horizontally.

        This is usually caused by tile.py being initiated before
        init_screen.py or options.py.
        note that tile.py is initiated by e.g. miscellaneous.py

        It could also be caused by the map file having a blank line at
        the end, or some lines being longer than others."""
        assert len(cls.map_) == Options.tiles_x * Options.tiles_y, dedent(error_msg)
        assert not cls.instances, "Tile.create has already been called"
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
        then how many solids are after it in the line for all lines on the map.
        This makes the drawing much faster,
        example:
        ##..###
        ####.#.
           |
           v
        {(tile.Tile object at 0x0..., 2), (tile.Tile ..., 3), (tile.Tile ..., 4), (tile.Tile ..., 1)}
        It ignores open tiles
        It is not necessary to compress opens since they are drawn by
        filling the screen.

        NOTE: A new group starts at a newline
        TODO: Make it so the loop_list is the type of tile with the fewest intances
        rtype: set
        """

        splitted_map = zip(*([iter(cls.map_)] * Options.tiles_x))
        # Split map on every newline

        compressed_map = []
        # A compressed list with True if solid and False if open
        # Looks something like this -> [(True, 5), (False, 2), (True, 9), ...]
        for row in splitted_map:
            for group in groupby(row):
                compressed_map.append((group[0], len(list(group[1]))))

        filtered_opens = (j for i, j in compressed_map if i)  # filter open tiles and remove the "True"
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
        In other words the tile furthest up, and then the one furthest to the left."""
        return self.number < other.number

    def __eq__(self, other):
        return self is other

    def __repr__(self):
        return "Tile: pos=%s, num=%s, walkable=%s" \
               % (self.pos, self.number, self.walkable)

    __str__ = __repr__

    @classmethod
    def random_open_tile(cls):
        """:return: location of a random walkable tile"""
        return random.choice(tuple(cls.opens)).pos

    def get_centre(self):
        """Return a vector of the pos in the centre of the tile
        >>> Tile.length = 20
        >>> a = Tile(x=0, y=0, is_solid=0)
        >>> a.get_centre()
        Vector(x=10, y=10)"""
        return self.pos + Tile.length // 2

    def closest_open_tile(self):
        return min(Tile.opens,
                   key=lambda x: (self.pos - x.pos).magnitude_squared())

    @classmethod
    def on_screen(cls, direction: int, tile_num: int):
        """Return False if the tile is outside of the screen else True
        A direction is needed as a tile on the right border is outside
        if the direction is west
        Params:
        direction: int of direction in the list NSEW. For example South has index 1.
        tile_num: index of tile in Tile.instances"""
        if direction == 2:  # East
            return tile_num % Options.tiles_x != 0
        if direction == 3:  # West
            return tile_num % Options.tiles_x != Options.tiles_x - 1
        return 0 <= tile_num <= cls.amnt_tiles  # North and South

    @classmethod
    def draw_all(cls, screen):
        """Fill the screen in light tiles, then draws the solid tiles over"""
        screen.fill(Options.fillcolor)
        length, loopcolor, draw_rect = cls.length, Options.loopcolor, pygame.draw.rect
        for tile, i in cls.loop_set:
            draw_rect(screen, loopcolor, (*tile.pos, length * i, length))

    @classmethod
    def get_number(cls, pos: Container):
        """Return the index in Tile.instances of the tile pos is on
        :param pos: a container with two items
        >>> Tile.get_number([0, 0])
        0"""
        return int(pos[0] // cls.length + pos[1] // cls.length * Options.tiles_x)


if __name__ == "__main__":
    Tile.create()
    print(len(Tile.instances))
    import doctest
    doctest.testmod()
