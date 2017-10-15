"""Defines a Vector class, and some mathematical functions"""

import math


class Vector:
    """Create a 2d Vector
    Parameters:
    x: The x coordinate
    y: The y coordinate

    Returns:
    A Vector with two attributes; x and y

    Examples:
    >>> Vector(x=0, y=1)
    Vector(x=0, y=1)

    Notes:
    Ternary operators have been overloaded to be element-wise.
    Examples:
    >>> Vector(4, 2) + Vector(-7, 4)
    Vector(x=-3, y=6)
    >>> Vector(2, -1) * Vector(6, 4)
    Vector(x=12, y=-4)

    If the other variable of a ternary operator is a number,
    the number is added to x and y
    >>> a = Vector(4, 6)
    >>> a + 3
    Vector(x=7, y=9)

    The rich comparion methods, except eq and ne, are based on the length of the vectors
    eq and ne is based on position
    >>> a, b = Vector(2, 3), Vector(4, 1)
    >>> assert a < b
    >>> a, b = Vector(0, 1), Vector(0, -1)
    >>> assert a != b"""

    __slots__ = 'x', 'y'

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @classmethod
    def x_as_pair(cls, x_and_y):
        return cls(*x_and_y)

    def __getitem__(self, name):
        if isinstance(name, int):
            if name == 0:
                return self.x
            elif name == 1 or name == -1:
                return self.y
            else:
                raise IndexError('Index out of range')
        elif isinstance(name, str):
            return getattr(self, name)
        else:
            raise TypeError('name must be str or int')

    def __setitem__(self, name, value):
        if isinstance(name, int):
            if name == 0:
                self.x = value
            elif name == 1 or name == -1:
                self.y = value
            else:
                raise IndexError('Index out of range')
        elif isinstance(name, str):
            setattr(self, name, value)
        else:
            raise TypeError('name must be str or int')
        return self

    def __iter__(self):
        yield self.x
        yield self.y

    def __len__(self):
        return 2

    def __contains__(self, item):
        return item == self.x or item == self.y

    def __repr__(self):
        return 'Vector(x=%s, y=%s)' % (self.x, self.y)

    def __eq__(self, other):
        return self.x == other[0] and self.y == other[1]

    def __ne__(self, other):
        return self.x != other[0] or self.y != other[1]

    def __add__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return Vector(self.x + other, self.y + other)

    __radd__ = __add__

    def __iadd__(self, other):
        if hasattr(other, '__getitem__'):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other, self.y - other)

    def __rsub__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(other[0] - self.x, other[1] - self.y)
        else:
            return Vector(other - self.x, other - self.y)

    def __isub__(self, other):
        if hasattr(other, '__getitem__'):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    def __truediv__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(self.x / other[0], self.y / other[1])
        else:
            return Vector(self.x / other, self.y / other)

    def __rtruediv__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(other[0] / self.x, other[1] / self.y)
        else:
            return Vector(other / self.x, other / self.y)

    def __itruediv__(self, other):
        if hasattr(other, '__getitem__'):
            self.x /= other[0]
            self.y /= other[1]
        else:
            self.x /= other
            self.y /= other
        return self

    def __floordiv__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(self.x // other[0], self.y // other[1])
        else:
            return Vector(self.x // other, self.y // other)

    def __rfloordiv__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(other[0] // self.x, other[1] // self.y)
        else:
            return Vector(other // self.x, other // self.y)

    def __ifloordiv__(self, other):
        if hasattr(other, '__getitem__'):
            self.x //= other[0]
            self.y //= other[1]
        else:
            self.x //= other
            self.y //= other
        return self

    def __mul__(self, other):
        if hasattr(other, '__getitem__'):
            return Vector(self.x * other[0], self.y * other[1])
        else:
            return Vector(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __imul__(self, other):
        if hasattr(other, '__getitem__'):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self

    def __lt__(self, other):
        return self.magnitude_squared() < other.magnitude_squared()

    def __gt__(self, other):
        return self.magnitude_squared() > other.magnitude_squared()

    def __le__(self, other):
        return self.magnitude_squared() <= other.magnitude_squared()

    def __ge__(self, other):
        return self.magnitude_squared() >= other.magnitude_squared()

    def as_ints(self):
        return int(self.x), int(self.y)

    def copy(self):
        """Return a shallow copy of the vector
        >>> a = Vector(1, 0)
        >>> b = a.copy()
        >>> a.y = 2
        >>> b
        Vector(x=1, y=0)"""
        return Vector(*self)

    __copy__ = copy

    def magnitude(self):
        """returns length of vector
        Pythagoras' theorem to find the length
        Vector(6, 8).magnitude() = √(6² + 8²) = √100 = 10
        >>> Vector(3, 4).magnitude()
        5.0"""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    __abs__ = magnitude

    def magnitude_squared(self):
        """Return the length of the vector squared for better performance
        >>> Vector(x=3, y=2).magnitude_squared()
        13

        Good for find the shortest / longest vector
        >>> min(Vector(12, 17), Vector(10, 19), key=lambda x: x.magnitude_squared())
        Vector(x=12, y=17)

        Faster than self.magnitude()"""
        return self.x ** 2 + self.y ** 2

    def signs(self):
        """return signs of self as a tuple
        >>> Vector(-3, 9).signs()
        (-1, 1)"""
        return (self.x > 0) - (self.x < 0), (self.y > 0) - (self.y < 0)

    def manhattan_dist(self, other):
        """returns the Manhattan distance between self and other
        >>> Vector(3, 2).manhattan_dist(Vector(10, 11))
        16

        https://en.wikipedia.org/wiki/Taxicab_geometry"""
        return abs(other[0] - self.x) + abs(other[1] - self.y)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    a = Vector(1, 2)
    b = Vector(2, 1)
    a['x'] = 3
    print(a * b)
