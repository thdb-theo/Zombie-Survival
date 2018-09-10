"""Includes the Baseclass for Zombie, Survivor, Bullet, PickUp, and Drop"""

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

    def get_centre(self) -> Vector:
        return self.pos + self._size.scale(0.5)

    centre = property(get_centre, doc="""Return a vector of the pos in the middle of self
                                         >>> a = BaseClass(x=0, y=0, width=10, height=10)
                                         >>> a.centre
                                         Vector(x=5, y=5)""")

    def get_number(self) -> int:
        """Return the index of tile that self is on"""
        return int(self.pos.x // Tile.length + self.pos.y // Tile.length * Options.tiles_x)

    def get_tile(self) -> Tile:
        """Return the tile on which self is"""
        return Tile.instances[self.get_number()]

    def offscreen(self) -> bool:
        return (self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x + self.width > Options.width or
                self.pos.y + self.height > Options.height)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    from timeit import timeit
    setup = """
from __main__ import BaseClass, Tile
Tile.create()
a = BaseClass(45, 91)
b = BaseClass(45, 90)
Options = Tile.instances[34]
"""
    print(timeit("a.collide(b)", setup=setup))
