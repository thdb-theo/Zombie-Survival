"""Includes the Baseclass for Zombie, Survivor, Bullet, and PickUp"""

import init as _
from options import Options
from maths import Vector
from tile import Tile


class BaseClass:
    """The Baseclass for the Survivor, Zombie, Bullet and PickUp classes
    Params:
    x: The x coordinate
    y: The y coordinate
    width: (Optional) Used by the Bullet Class as it has another size. Defaults to Tile.length
    height: (Optional) Used by the Bullet Class as it has another size. Defaults to Tile.length"""

    def __init__(self, x, y, width=None, height=None):

        if width is None and height is None:
            self.width, self.height = Tile.length, Tile.length
        else:
            self.width, self.height = width, height
        self._size = Vector(self.width, self.height)
        self.to = None
        self.pos = Vector(x, y)

    def get_centre(self):
        return self.pos + self._size.scale(1/2)

    centre = property(get_centre, doc="""Return a vector of the pos in the middle of self
                                         >>> a = BaseClass(x=0, y=0, width=10, height=10)
                                         >>> a.centre
                                         Vector(x=5, y=5)""")

    def get_number(self):
        """Return the index of tile that self is on"""

        return int(self.pos.x // Tile.length + self.pos.y // Tile.length * Options.tiles_x)

    def get_tile(self):
        """Return the tile on which self is"""
        return Tile.instances[self.get_number()]


def get_number(pos):
    """Return the index in Tile.instances of the tile pos is on
    :param pos: a container with two items
    >>> get_number([0, 0])
    0"""
    x, y = pos
    return x // Tile.length + y // Tile.length * Options.tiles_x


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    from timeit import timeit
    setup = """
from __main__ import BaseClass, get_number, Tile
Tile.create()
a = BaseClass(45, 91)
b = BaseClass(45, 90)
Options = Tile.instances[34]
"""
    print(timeit("a.collide(b)", setup=setup))
