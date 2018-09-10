"""Defines a Vector class, and some mathematical functions"""

from math import (cos, sin, atan2, sqrt, pi, floor, exp, isclose, degrees,
                  radians, inf)
from random import randrange, random, uniform
from dataclasses import dataclass
from colorsys import rgb_to_hls, rgb_to_hsv, hls_to_rgb, hsv_to_rgb

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


class Colour:
    def __init__(self, *args):
        if len(args) == 1:
            s = args[0]
            self.r = int(s[1:3], 16)
            self.g = int(s[3:5], 16)
            self.b = int(s[5:7], 16)
        else:
            self.r, self.g, self.b = map(int, args)
        self.rgb = self.r, self.g, self.b

    def __str__(self):
        return "Colour(r={0.r}, g={0.g}, b={0.b})".format(self)

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.rgb[item]
        elif isinstance(item, str):
            return getattr(self, item)
        else:
            raise TypeError("list indices must be integers, strings or slices, not " + type(item).__name__)

    def euclidean_distance(self, other: "Colour"):
        x1, y1, z1 = self
        x2, y2, z2 = other
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def ciede2000(self, other: "Colour"):
        """Uses CIE's formula to find the differnce between two colours
        Takes into consideration that the eye is better at differenciating
        some colours than others
        Formula source: http://www2.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf
        :parameter other: Colour
        :rtype float"""
        class A:
            pass
        c1 = A()
        c2 = A()
        for i in range(3):
            setattr(c1, "Lab"[i], self.lab[i])
            setattr(c2, "Lab"[i], other.lab[i])

        k_L = 1
        k_C = 1
        k_H = 1
        c1.C = sqrt(c1.a ** 2 + c1.b ** 2)
        c2.C = sqrt(c2.a ** 2 + c2.b ** 2)
        avgC = (c1.C + c2.C) / 2
        G = 0.5 * (1 - sqrt(avgC ** 7 / (avgC ** 7 + 25 ** 7)))
        c1.aA = (1 + G) * c1.a
        c2.aA = (1 + G) * c2.a
        c1.CA = sqrt(c1.aA ** 2 + c1.b ** 2)
        c2.CA = sqrt(c2.aA ** 2 + c2.b ** 2)
        c1.hA = 0 if c1.b == c1.aA == 0 else degrees(atan2(c1.b, c1.aA) % (2 * pi))
        c2.hA = 0 if c2.b == c2.aA == 0 else degrees(atan2(c2.b, c2.aA) % (2 * pi))
        deltaLA = c2.L - c1.L
        deltaCA = c2.CA - c1.CA
        if c1.C * c2.C == 0:
            deltahA = 0
        elif abs(c2.hA - c1.hA) <= 180:
            deltahA = c2.hA - c1.hA
        elif c2.hA - c1.hA > 180:
            deltahA = c2.hA - c1.hA - 360
        elif c2.hA - c1.hA < -180:
            deltahA = c2.hA - c1.hA + 360
        else:
            raise ValueError("c1: %s, c2: %s" % (c1, c2))
        deltaHA = 2 * sqrt(c1.CA * c2.CA) * sin(radians(deltahA / 2))
        avgLA = (c1.L + c2.L) / 2
        avgCA = abs(c1.CA + c2.CA) / 2

        diffhA = abs(c1.hA - c2.hA)
        addhA = c1.hA + c2.hA

        if c1.CA * c2.CA == 0:
            avghA = addhA
        elif diffhA <= 180:
            avghA = addhA / 2
        elif diffhA > 180 and addhA < 360:
            avghA = (addhA + 360) / 2
        elif diffhA > 180 and addhA >= 360:
            avghA = (addhA - 360) / 2
        else:
            raise ValueError("c1: %s, c2: %s" % (c1, c2))
        T = 1 - 0.17 * cos(radians(avghA - 30)) + 0.24 * cos(radians(2 * avghA)) \
            + 0.32 * cos(radians((3 * avghA + 6))) - 0.2 * cos(radians(4 * avghA - 63))
        delta_theta = 30 * exp(-(((avghA - 275) / 25) ** 2))
        under_root = avgCA ** 7 / (avgCA ** 7 + 25 ** 7)
        if under_root <= 0:
            R_c = 0
        else:
            R_c = 2 * sqrt(under_root)
        S_L = 1 + (0.015 * (avgLA - 50) ** 2) / (sqrt(20 + (avgLA - 50) ** 2))
        S_C = 1 + 0.045 * avgCA
        S_H = 1 + 0.015 * avgCA * T
        R_T = -sin(radians(2 * delta_theta)) * R_c
        term1 = (deltaLA / (k_L * S_L)) ** 2
        term2 = (deltaCA / (k_C * S_C)) ** 2
        term3 = (deltaHA / (k_H * S_H)) ** 2
        term4 = (R_T * deltaCA * deltaHA) / (k_C * S_C * k_H * S_H)
        return sqrt(term1 + term2 + term3 + term4)

    def normalise(self):
        """normalises the color. Instead of r, g, b being between 0 and 255,
        the they between 0 and 1
        returns a tuple
        Example:
        >>> Colour(255, 0, 0).normalise()
        (1.0, 0.0, 0.0)
        >>> Colour(51, 204, 153).normalise()
        (0.2, 0.8, 0.6)"""
        return self.r / 255., self.g / 255., self.b / 255.

    @classmethod
    def from_normalised(cls, r, g, b):
        """From normalised RGB colour
        >>> str(Colour.from_normalised(1., 0.5, 0.))
        'Colour(r=255, g=127, b=0)'"""
        return cls(*map(lambda x: int(x * 255), [r, g, b]))

    @classmethod
    def from_hsv(cls, h, s, v):
        """To hsv colour space
        https://en.wikipedia.org/wiki/HSL_and_HSV"""
        return cls.from_normalised(*hsv_to_rgb(h, s, v))

    @classmethod
    def from_hls(cls, h, l, s):
        return cls.from_normalised(*hls_to_rgb(h, l, s))

    @classmethod
    def from_lab(cls, L, a, b):
        """From CIELAB (aka Lab) colour space
        https://en.wikipedia.org/wiki/CIELAB_color_space"""
        ref_x, ref_y, ref_z = 95.047, 100.000, 108.883
        var_Y = (L + 16) / 116
        var_X = a / 500 + var_Y
        var_Z = var_Y - b / 200

        if var_Y ** 3 > 0.008856:
            var_Y = var_Y ** 3
        else:
            var_Y = (var_Y - 16 / 116) / 7.787
        if var_X ** 3 > 0.008856:
            var_X = var_X ** 3
        else:
            var_X = (var_X - 16 / 116) / 7.787
        if var_Z ** 3 > 0.008856:
            var_Z = var_Z ** 3
        else:
            var_Z = (var_Z - 16 / 116) / 7.787

        X = var_X * ref_x
        Y = var_Y * ref_y
        Z = var_Z * ref_z

        var_X = X / 100
        var_Y = Y / 100
        var_Z = Z / 100

        var_R = var_X * 3.2406 + var_Y * -1.5372 + var_Z * -0.4986
        var_G = var_X * -0.9689 + var_Y * 1.8758 + var_Z * 0.0415
        var_B = var_X * 0.0557 + var_Y * -0.2040 + var_Z * 1.0570

        if var_R > 0.0031308:
            var_R = 1.055 * (var_R ** (1 / 2.4)) - 0.055
        else:
            var_R = 12.92 * var_R
        if var_G > 0.0031308:
            var_G = 1.055 * (var_G ** (1 / 2.4)) - 0.055
        else:
            var_G = 12.92 * var_G
        if var_B > 0.0031308:
            var_B = 1.055 * (var_B ** (1 / 2.4)) - 0.055
        else:
            var_B = 12.92 * var_B

        return cls.from_normalised(var_R, var_G, var_B)

    @classmethod
    def from_cmyk(cls, c, m, y, k):
        """From CMYK colour model
        https://en.wikipedia.org/wiki/CMYK_color_model"""
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return cls(r, g, b)

    @property
    def hex(self):
        """To web colour (aka hex)
        https://en.wikipedia.org/wiki/Web_colors"""
        return "#{0.r:02x}{0.g:02x}{0.b:02x}".format(self)

    @property
    def hsv(self):
        """To hsv colour space
        https://en.wikipedia.org/wiki/HSL_and_HSV"""
        return rgb_to_hsv(*self)

    @property
    def hls(self):
        """To HSL colour space
        https://en.wikipedia.org/wiki/HSL_and_HSV"""
        return rgb_to_hls(*self)

    @property
    def hcl(self):
        """To hcl colour space
        https://en.wikipedia.org/wiki/HCL_color_space"""
        r, b, g = self.rgb
        min_rgb = min(r, b, g)
        max_rgb = max(r, b, g)
        alpha = 1 / 100 * min_rgb / max_rgb
        gamma = 3
        Q = exp(alpha * gamma)
        h = atan2(g - b, r - g)
        c = (Q * (abs(r - g) + abs(g - b) + abs(b - r))) / 3
        l = (Q * max_rgb + (1 - Q) * min_rgb) / 2
        return h, c, l

    @property
    def lab(self):
        """To CIELAB (aka Lab) colour space
        https://en.wikipedia.org/wiki/CIELAB_color_space"""
        var_R, var_G, var_B = self.normalise()

        if var_R > 0.04045:
            var_R = pow(((var_R + 0.055) / 1.055), 2.4)
        else:
            var_R = var_R / 12.92
        if var_G > 0.04045:
            var_G = pow(((var_G + 0.055) / 1.055), 2.4)
        else:
            var_G = var_G / 12.92
        if var_B > 0.04045:
            var_B = pow(((var_B + 0.055) / 1.055), 2.4)
        else:
            var_B = var_B / 12.92

        var_R = var_R * 100.
        var_G = var_G * 100.
        var_B = var_B * 100.

        X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
        Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
        Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

        var_X = X / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
        var_Y = Y / 100.000  # ref_Y = 100.000
        var_Z = Z / 108.883  # ref_Z = 108.883

        if var_X > 0.008856:
            var_X = pow(var_X, (1. / 3.))
        else:
            var_X = (7.787 * var_X) + (16. / 116.)
        if var_Y > 0.008856:
            var_Y = pow(var_Y, (1. / 3.))
        else:
            var_Y = (7.787 * var_Y) + (16. / 116.)
        if var_Z > 0.008856:
            var_Z = pow(var_Z, (1. / 3.))
        else:
            var_Z = (7.787 * var_Z) + (16. / 116.)

        l_s = (116. * var_Y) - 16.
        a_s = 500. * (var_X - var_Y)
        b_s = 200. * (var_Y - var_Z)
        return l_s, a_s, b_s

    @property
    def cmyk(self):
        """To CMYK colour model
        https://en.wikipedia.org/wiki/CMYK_color_model"""
        r_f, g_f, b_f = self.normalise()
        k = 1 - max(r_f, g_f, b_f)
        c = (1 - r_f - k) / (1 - k)
        m = (1 - g_f - k) / (1 - k)
        y = (1 - b_f - k) / (1 - k)
        return c, m, y, k

    @classmethod
    def random(cls, h=(0, 1), l=(0, 1), s=(0, 1)):
        """Returns a random colour in rgb
        Params:
        ---------------------------------------------
        h: The uniform from which it gets a random hue
        s: The uniform from which it gets a random saturation
        l: The uniform from which it gets a random lightness"""
        hls = uniform(*h), uniform(*l), uniform(*s)
        return cls.from_hls(*hls)

    @classmethod
    def random_rgb(cls):
        return cls(randrange(0, 256), randrange(0, 256), randrange(0, 256))

    def contrasting(self):
        """return white (#ffffff) if the colour is dark and
        black (#000000) if the colour is light
        Uses W3C's technque to find a colour's brightness
        Source: https://www.w3.org/TR/AERT/#color-contrast"""
        r, g, b = self
        brighness = (r * 299 + g * 587 + b * 114) / 1000
        assert 0 <= brighness <= 256
        if brighness > 128:
            return Colour("#000000")
        else:
            return Colour("#ffffff")

    @classmethod
    def complementary(cls, *colours: "Colour", decrement=0.005):
        """Return a random colour that looks as different from the
        colours as possible
        The way it does this is creating a random colour and checking the
        difference. If it is not different enough, check new colour and decrement the
        required difference. This way it will not find the most different colour,
        but something that is different enough for my use."""
        len_colours = len(colours)
        tolerance = 120
        while True:
            i = 0
            new = cls.random_rgb()
            for colour in colours:
                d = colour.ciede2000(new)
                if d < tolerance:
                    tolerance -= decrement
                    break
            else:  # No break
                return new

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    c = Colour.random()
    print(c.ciede2000(c))
    _test_complementary(20, 12, fps=60)
