from random import random,  uniform
from math import inf

from pygame import Color as PyGameColor
from colormath.color_objects import sRGBColor, LabColor, HSVColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


class Color(sRGBColor):
    def __init__(self, r, g=None, b=None, is_upscaled=False, upscale=False):
        if isinstance(r, sRGBColor):
            r, b, g = r.get_value_tuple()
        elif isinstance(r, (str, int)) and g is None or b is None:

            if isinstance(r, str):
                s = r
            else:
                s = "#" + format(hex(r)[2:], "0>6")
            r = int(s[1:3], 16)
            g = int(s[3:5], 16)
            b = int(s[5:7], 16)

        elif hasattr(r, "__getitem__"):
            r, g, b = r
        if upscale:
            r, g, b = int(r*256), int(g*256), int(b*256)
        super().__init__(r, g, b, is_upscaled=is_upscaled)
        self.r, self.g, self.b = r, g, b

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if isinstance(item, slice):
            return tuple(map(int, self.get_value_tuple()[item]))
        return int(self.get_value_tuple()[item])

    def norm(self):
        """From r, g, b values between 0-255 to 0.0-1.0"""
        return Color(self, is_upscaled=True)

    @classmethod
    def complementary(cls, *colors: "Color", decrement=0.01):
        """Return a random color that looks as different from the colors as possible
        The way it does this is creating a random color and checking the
        difference. If it is not different enough, check new color and decrement the
        required difference. This way it will not find the most different color,
        but something that is different enough for my use."""
        len_colors = len(colors)
        tolerance = 70
        lab_colours = [convert_color(color.norm(), LabColor) for color in colors]
        while True:
            new_hsv = HSVColor(uniform(0, 360), random(), random())
            new_lab = convert_color(new_hsv, LabColor)
            min_d = inf
            for color in lab_colours:
                d = delta_e_cie2000(new_lab, color)
                min_d = min(min_d, d)
                if d < tolerance:
                    tolerance -= decrement
                    break
            else:  # No break
                return Color(convert_color(new_lab, sRGBColor), upscale=True), min_d

    def contrasting(self):
        brightness = (self.r * 299 + self.g * 587 + self.b * 114) / 1000.
        return Color(0, 0, 0) if brightness > 128 else Color(255, 255, 255)

    def get_rgb_hex(self):
        return "#{0.r:02x}{0.g:02x}{0.b:02x}".format(self)


BLACK = Color(0)
WHITE = Color(0xffffff)
DARK_GREY = Color(0x1a1a1a)
LIGHT_GREY = Color(0x696969)
RED = Color(0xff0000)
GREEN = Color(0x00ff00)
BLUE = Color(0x0000ff)
YELLOW = Color(0xffff00)
PINK = Color(0xff00ff)
CYAN = Color(0x00ffff)
LIGHT_BLUE = Color(0x1a63ce)
DARK_RED = Color(0xaa0000)
TRANSPARENT = PyGameColor(0, 0, 0, 0)
