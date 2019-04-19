"""Defines a Vector class, and some mathematical functions"""

from math import cos, sin, atan2, sqrt, pi
from random import randrange, random, uniform
from dataclasses import dataclass
import logging

SMALL_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97}

@dataclass
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
    Pluss and minus are overloaded to be element-wise.
    Examples:
    >>> Vector(4, 2) + Vector(-7, 4)
    Vector(x=-3, y=6)
    >>> Vector(2, -1) - Vector(6, 4)
    Vector(x=-4, y=-5)

    If the other variable of a ternary operator is a number,
    the number is added to x and y
    >>> a = Vector(4, 6)
    >>> a + 3
    Vector(x=7, y=9)

    Division is not defined, and * is overloaded to dot multiplication
    >>> Vector(-5, 2) * Vector(-1, 8)
    21

    For element-wise multiplication use self.scale(n)
    >>> v = Vector(9, 6)
    >>> v.scale(3)
    Vector(x=27, y=18)

    For element-wise division use self.scale(1/n)
    NOTE: x and y become floats
    >>> v = Vector(9, 6)
    >>> v.scale(1/3)
    Vector(x=3.0, y=2.0)

    The rich comparion methods, except eq and ne, are based on the length of the vectors
    eq and ne is based on the position
    >>> a, b = Vector(2, 3), Vector(4, 1)
    >>> assert a < b
    >>> a, b = Vector(0, 1), Vector(0, -1)
    >>> assert a != b"""
    x: float
    y: float

    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, idx):
        return (self.x, self.y)[idx]

    def __len__(self):
        return 2

    @classmethod
    def random_unit_vector(cls):
        """A random vector on the unit circle. its lengtth is always 1"""
        v = cls(1, 0)
        a = random() * 2 * pi
        v.rotate(a)
        return v

    def __add__(self, other):
        if hasattr(other, "__getitem__"):
            return Vector(self.x + other[0], self.y + other[1])
        else:
            return Vector(self.x + other, self.y + other)

    __radd__ = __add__

    def __iadd__(self, other):
        if hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self

    def __sub__(self, other):
        if hasattr(other, "__getitem__"):
            return Vector(self.x - other[0], self.y - other[1])
        else:
            return Vector(self.x - other, self.y - other)

    def __rsub__(self, other):
        if hasattr(other, "__getitem__"):
            return Vector(other[0] - self.x, other[1] - self.y)
        else:
            return Vector(other - self.x, other - self.y)

    def __isub__(self, other):
        if hasattr(other, "__getitem__"):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self

    def scale(self, scalar_or_x, y=None):
        if y is None:
            return Vector(self.x * scalar_or_x, self.y * scalar_or_x)
        return Vector(self.x * scalar_or_x, self.y * y)

    def dot(self, other: "Vector"):
        return self.x * other.x + self.y * other.y

    __mul__ = __rmul__ = dot

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
        return sqrt(self.x ** 2 + self.y ** 2)

    __abs__ = magnitude

    def magnitude_squared(self):
        """Return the length of the vector squared for better performance
        >>> Vector(x=3, y=2).magnitude_squared()
        13

        Good for finding the shortest / longest vector
        >>> min(Vector(12, 17), Vector(10, 19))
        Vector(x=12, y=17)

        Faster than self.magnitude()"""
        return self.x ** 2 + self.y ** 2

    def signs(self):
        """return signs of self as a tuple
        >>> Vector(-3, 9).signs()
        (-1, 1)"""
        return (self.x > 0) - (self.x < 0), (self.y > 0) - (self.y < 0)

    def manhattan_dist(self):
        """returns the Manhattan of the vector
        >>> Vector(3, 2).manhattan_dist()
        5
        >>> Vector(-4, -2).manhattan_dist()
        6

        https://en.wikipedia.org/wiki/Taxicab_geometry"""
        return abs(self.x) + abs(self.y)

    def angle(self):
        """Angle of the vector in radians"""
        return atan2(self.y, self.x)

    def polar(self):
        return self.magnitude(), self.angle()

    def rotate(self, angle: float):
        """Rotates the vector 'angle' radians anti-clockwise
        is very prone to rounding errors
        >>> v = Vector(1, 1)
        >>> v.rotate(pi)
        >>> v
        Vector(x=-1.0000000000000002, y=-0.9999999999999999)
        """
        x, y = self.x, self.y
        self.x = cos(angle) * x - sin(angle) * y
        self.y = sin(angle) * x + cos(angle) * y

    def rotated(self, angle: float):
        """Returns a vector rotated 'angle' radians anti-clockwise
        is very prone to rounding errors
        >>> v = Vector(1, 1)
        >>> v.rotated(pi)
        Vector(x=-1.0000000000000002, y=-0.9999999999999999)
        """
        x = cos(angle) * self.x - sin(angle) * self.y
        y = sin(angle) * self.x + cos(angle) * self.y
        return Vector(x, y)


@dataclass
class Ray:
    pos: Vector
    angle: float


def isprime(n, k=10):
    """test if n is a prime number
    if n is less than 100, check if n is in a set of small primes
    else check if n is prime using the Miller-Rabin test
    >>> isprime(2) and isprime(2**1279-1)
    True
    >>> isprime(1) or isprime(-2)
    False"""
    if n == 2:
        return True
    if not n % 2:
        return False
    if n < 100:
        return n in SMALL_PRIMES

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for i in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = n - 1
    while not d % 2:
        d >>= 1
        s += 1
    for i in range(k):
        a = randrange(2, n - 1)
        if not check(a, s, d, n):
            return False
    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    c = Color(255, 255, 255)
    print(c.norm())