import math
from collections import namedtuple

_square = namedtuple("square", "x y w h")
_vector = namedtuple("vector", "x y")

def angle_between(x1, y1, x2, y2):
    """Get angle of the hypotenuse to the adjecent side of v1 in a
    rigth triangle where v1 and v2 are the not-right-angled corners

          v2
         / |
        /  |
       /   |
      /θ   |
    v1------

    >>> v1, v2 = _vector(1, 5), _vector(8, 0)
    >>> angle_between(*v1, *v2)
    0.6202494859828215

    NB: Takes in mind pygame's flipped y-axis
    angles appears anti-clockwise on normal coordinate systems
    Examples:
    >>> angle_between(*_vector(1, 0), *_vector(1, 1))
    4.71238898038469
    >>> angle_between(*_vector(1, 1), *_vector(2, 0))
    0.7853981633974483

    :return the angle in radians. No negative angles"""
    return math.atan2(y1 - y2, x2 - x1) % (2 * math.pi)


def collide(x1, y1, w1, h1, x2, y2, w2, h2):
    """Return True if self and other overlap else False
       Returns False if self and other are side by side

       Examples:
       True if rect1 and rect2 partially covers eachother
       >>> a = _square(x=0, y=0, w=10, h=10)
       >>> b = _square(x=9, y=9, w=10, h=10)
       >>> collide(*a, *b)
       True
       >>> collide(*b, *a)
       True

       True if rect1 and rect2 are identical
       >>> a = _square(x=0, y=0, w=1, h=1)
       >>> collide(*a, *a)
       True

       True if rect1 or rect2 entirely incaptures the other
       >>> a = _square(x=0, y=0, w=3, h=3)
       >>> b = _square(x=1, y=1, w=1, h=1)
       >>> collide(*a, *b)
       True
       >>> collide(*b, *a)
       True

       False if rect1 and rect2 are side by side
       >>> a = _square(x=0, y=0, w=10, h=10)
       >>> b = _square(x=10, y=0, w=10, h=10)
       >>> collide(*a, *b)
       False
       >>> collide(*b, *a)
       False"""
    return ((x1 + w1 > x2) and (y1 < y2 + h2) and
            (y1 + h1 > y2) and (x1 < x2 + w2))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
