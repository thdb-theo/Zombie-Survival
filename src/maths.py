"""Defines a Vector class, and some mathematical functions"""

from math import (cos, sin, atan2, sqrt, pi, floor, exp, isclose, degrees,
                  radians)
from random import randrange, random, uniform

import pygame
from recordclass import recordclass

SMALL_PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                53, 59, 61, 67, 71, 73, 79, 83, 89, 97}


class Vector(recordclass("Vector", "x y")):
    """Create a 2d Vector
    Inherits:
    A recordclass with name "Vector" and fields "x" and "y"
    recordclass is a fast mutatable namedtuple
    its source code can be found here:
    https://bitbucket.org/intellimath/recordclass/src/

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

    def dot(self, other):
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

    def rotate(self, angle):
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

    def rotated(self, angle):
        """Rotates a vector 'angle' radians anti-clockwise
        is very prone to rounding errors
        >>> v = Vector(1, 1)
        >>> v.rotated(pi)
        Vector(x=-1.0000000000000002, y=-0.9999999999999999)
        """
        x = cos(angle) * self.x - sin(angle) * self.y
        y = sin(angle) * self.x + cos(angle) * self.y
        return Vector(x, y)


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


def dcos(x):
    """return the cosine of x degrees"""
    return cos(radians(x))


def dsin(x):
    """Return the sine of x degrees"""
    return sin(radians(x))


def datan2(x, y):
    """return atan2(x, y) as degrees from 0 to 360"""
    return degrees(atan2(x, y) % (2 * pi))


class NameSpace:
    def __init__(self, a):
        self.__dict__ = a

    def __str__(self):
        return str(self.__dict__)


class Colour():
    def __init__(self, *args):
        if len(args) == 1:
            s = args[0]
            if s == "random":
                s = Colour.random().hex
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
        if isinstance(item, int):
            return self.rgb[item]
        elif isinstance(item, str):
            return getattr(self, item)
        else:
            raise TypeError

    def euclidean_distance(self, other):
        x1, y1, z1 = self
        x2, y2, z2 = other
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    def ciede2000(self, other):
        """Uses CIE's formula to find the differnce between two colours
        Takes into consideration that the eye is better at differenciating
        some colours than others
        Source: http://www2.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf
        :parameter other: Colour
        :rtype float"""
        c1 = NameSpace(dict(zip(["L", "a", "b"], self.lab)))
        c2 = NameSpace(dict(zip(["L", "a", "b"], other.lab)))
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
        c1.hA = 0 if c1.b == c1.aA == 0 else datan2(c1.b, c1.aA)
        c2.hA = 0 if c2.b == c2.aA == 0 else datan2(c2.b, c2.aA)
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
        deltaHA = 2 * sqrt(c1.CA * c2.CA) * dsin(deltahA / 2)
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
        T = 1 - 0.17 * dcos(avghA - 30) + 0.24 * dcos(2 * avghA) \
            + 0.32 * dcos(3 * avghA + 6) - 0.20 * dcos(4 * avghA - 63)
        delta_theta = 30 * exp(-(((avghA - 275) / 25) ** 2))
        under_root = avgCA ** 7 / (avgCA ** 7 + 25 ** 7)
        if isclose(under_root, 0, abs_tol=1e-5) and under_root < 0:
            R_c = 0
        else:
            R_c = 2 * sqrt(under_root)
        S_L = 1 + (0.015 * (avgLA - 50) ** 2) / (sqrt(20 + (avgLA - 50) ** 2))
        S_C = 1 + 0.045 * avgCA
        S_H = 1 + 0.015 * avgCA * T
        R_T = -dsin(2 * delta_theta) * R_c
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
        return self.r / 255, self.g / 255, self.b / 255

    @classmethod
    def from_normalised(cls, r, g, b):
        return cls(*map(lambda x: int(x * 255), [r, g, b]))

    @classmethod
    def from_hsv(cls, h, s, v):
        i = floor(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i % 6)]

        return cls.from_normalised(r, g, b)

    @classmethod
    def from_hsl(cls, h, s, l):
        def hue_to_rgb(p, q, t):
            t += 1 if t < 0 else 0
            t -= 1 if t > 1 else 0
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        if s == 0:
            r, g, b = l, l, l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1 / 3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1 / 3)
        return cls.from_normalised(r, g, b)

    @classmethod
    def from_lab(cls, L, a, b):
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

        sR = var_R * 255
        sG = var_G * 255
        sB = var_B * 255

        return cls(sR, sG, sB)

    @classmethod
    def from_cmyk(cls, c, m, y, k):
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return cls(r, g, b)

    @property
    def hex(self):
        return "#{0.r:02x}{0.g:02x}{0.b:02x}".format(self)

    @property
    def hsv(self):
        r, g, b = self.normalise()
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = high, high, high

        d = high - low
        s = 0 if high == 0 else d / high

        if high == low:
            h = 0.0
        else:
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return h, s, v

    @property
    def hsl(self):
        r, g, b = self.normalise()
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, v = ((high + low) / 2,) * 3

        if high == low:
            h = 0.0
            s = 0.0
        else:
            d = high - low
            s = d / (2 - high - low) if low > 0.5 else d / (high + low)
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6

        return h, s, v

    @property
    def hcl(self):
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
        r_f, g_f, b_f = self.normalise()
        k = 1 - max(r_f, g_f, b_f)
        c = (1 - r_f - k) / (1 - k)
        m = (1 - g_f - k) / (1 - k)
        y = (1 - b_f - k) / (1 - k)
        return c, m, y, k

    @classmethod
    def random(cls, h=(0, 1), s=(0, 1), l=(0, 1)):
        """Returns a random colour in rgb
        Params:
        ---------------------------------------------
        h: The uniform from which it gets a random hue
        s: The uniform from which it gets a random saturation
        l: The uniform from which it gets a random lightness

        :rtype: tuple"""
        hsl = uniform(*h), uniform(*s), uniform(*l)
        return cls.from_hsl(*hsl)

    def contrasting(self):
        """return white (#ffffff) if the colour is dark and
        black (#000000) if the colour is light
        Uses W3C's technque to find a colour's brightness
        Source: https://www.w3.org/TR/AERT/#color-contrast
        :returns: hex as a string"""
        r, g, b = self
        brighness = (r * 299 + g * 587 + b * 114) / 1000
        assert 0 <= brighness <= 256
        if brighness > 128:
            return Colour("#000000")
        else:
            return Colour("#ffffff")

    @classmethod
    def complementary(cls, *colours):
        """Return a random colour that is a certain distance away
        from the colours in the 3d plain"""
        len_colours = len(colours)
        tolerance = 80
        while True:
            i = 0
            new = cls.random()
            for colour in colours:
                d = colour.ciede2000(new)
                if d > tolerance:
                    i += 1
            if i == len_colours:
                return new
            else:
                tolerance -= 0.01


BLACK = Colour(0, 0, 0)
WHITE = Colour(255, 255, 255)
DARK_GREY = Colour(40, 40, 40)
LIGHT_GREY = Colour(105, 105, 105)
RED = Colour(255, 0, 0)
GREEN = Colour(0, 255, 0)
BLUE = Colour(0, 0, 255)
YELLOW = Colour(255, 255, 0)
PINK = Colour(255, 0, 255)
CYAN = Colour(0, 255, 255)
LIGHT_BLUE = Colour(26, 99, 206)
DARK_RED = Colour(170, 0, 0)


def _test_complementary():
    import pygame, sys, time
    pygame.init()
    text_colours = [Colour.random() for _ in range(40)]
    screen = pygame.display.set_mode([250, 20 + 12 * len(text_colours)])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 12)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        t1 = time.time()
        comp_color = Colour.complementary(*text_colours)
        print(time.time() - t1)
        screen.fill(comp_color)
        y = 10
        for text_colour in text_colours:
            text = font.render(str(text_colour), 1, text_colour)
            screen.blit(text, [30, y])
            y += 12

        pygame.display.flip()
        clock.tick(0.6)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _test_complementary()