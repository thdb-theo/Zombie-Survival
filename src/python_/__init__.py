import math

def angle_between(x1, y1, x2, y2):
    """Get angle of the hypotenuse to the adjecent side of v1 in a
    rigth triangle where v1 and v2 are the non-right angled corners

          v2
         / |
        /  |
       /   |
      /θ   |
    v1------

    >>> v1, v2 = Vector(1, 5), Vector(8, 0)
    >>> angle_between(v1, v2)
    0.6202494859828215

    NB: Takes in mind pygame's flipped y-axis
    angles appears anti-clockwise on normal coordinate systems
    Examples:
    >>> angle_between(Vector(1, 0), Vector(1, 1))
    4.71238898038469
    >>> angle_between(Vector(1, 1), (2, 0))
    0.7853981633974483

    :return the angle in radians. No negative angles"""
    return math.atan2(y1 - y2, x2 - x1) % (2 * math.pi)


def collide(x1, y1, w1, h1, x2, y2, w2, h2):
    """Return True if self and other overlap else False
       Returns False if self and other are side by side

       Examples:
       True if rect1 and rect2 partially covers eachother
       >>> a = 0, 0, 10, 10
       >>> b = 9, 9, 10, 10
       >>> collide(a, b)
       True
       >>> collide(b, a)
       True

       True if rect1 and rect2 are identical
       >>> a = 0, 0, 1, 1)
       >>> collide(a, a)
       True

       True if rect1 or rect2 entirely incaptures the other
       >>> a = 0, 0, 3, 3
       >>> b = 1, 1, 1, 1
       >>> collide(a, b)
       True
       >>> collide(b, a)
       True

       False if rect1 and rect2 are side by side
       >>> a = 0, 0, 10, height=10)
       >>> b = BaseClass(x=10, y=0, width=10, height=10)
       >>> a.collide(b)
       False
       >>> b.collide(a)
       False"""
    return ((x1 + w1 > x2) and (y1 < y2 + h2) and
            (y1 + h1 > y2) and (x1 < x2 + w2))
