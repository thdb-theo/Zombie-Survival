# -*- coding: utf-8 -*-
"""options for the whole module."""

import argparse
import warnings
from random import uniform
import colorsys
import os
import locale


def get_resolution():
        """Get resoltution of the screen"""
        if os.name == 'posix':
            # For Linux, including macOS. Is not tested on Mac
            # HACK: saves resolution to a file, get results and deletes the file
            os.system("xrandr  | grep \* | cut -d' ' -f4 > resolution.txt")
            file = open('resolution.txt', 'r')
            # file looks like this: '1920x1080'
            try:
                return tuple(map(int, file.read().split('x')))
            except ValueError:
                warnings.warn("""\nThis is meant for testing cython on "Bash on Ubuntu on Windows"
                              where no screen is available and thus the xrandr returns an
                              empty string and the previous statement raises a ValueError.
                              If you didn\'t expect this message; either there is
                              something wrong with xrandr or it couldn't find a screen.""")
                return 1280, 720
            finally:
                file.close()
                os.remove('resolution.txt')  # delete the file

        elif os.name == 'nt':
            # For Windows
            import ctypes
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            # Various other OSes, not implemented
            # TODO: find a cross platform solution
            raise OSError('Cannot find screen resolution for this OS')


class Colours:
    """Defines a whole bunch of colours.
    Also has staticmethods related to colours; getting a random colour
    and a getting colour in hexadecimal or rgb

    NOTE: Colour is not callable! Think of it a namespace for everything releated to colours
    RAISES: TypeError: If it is called"""

    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    DARK_GREY = 40, 40, 40
    LIGHT_GREY = 105, 105, 105
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    BLUE = 0, 0, 255
    YELLOW = 255, 255, 0
    PINK = 255, 0, 255
    CYAN = 0, 255, 255
    LIGHT_BLUE = 26, 99, 206

    def __new__(cls, *args, **kwargs):
        raise TypeError('Colour is not callable')

    __call__ = __new__

    @staticmethod
    def random(h=(0, 1), s=(0, 1), l=(0, 1)):
        """Returns a random colour in rgb
        Params:
        ---------------------------------------------
        h: The uniform from which it gets a random hue
        s: The uniform from which it gets a random saturation
        l: The uniform from which it gets a random lightness

        :rtype: tuple"""
        hsl = uniform(*h), uniform(*s), uniform(*l)
        return tuple(int(256 * i) for i in colorsys.hls_to_rgb(*hsl))

    @classmethod
    def get_hex(cls, colour):
        """Get hex value of an rgb tuple or name of a colour
        if colour is a string: get hex of the class attr with that name
        if colour is a collection with three ints: get hex value
        >>> Colours.get_hex('RED')
        '#ff0000'
        >>> Colours.get_hex([0, 255, 0])
        '#00ff00'
        """
        if isinstance(colour, str):
            return '#{0:02x}{1:02x}{2:02x}'.format(*getattr(cls, colour.upper()))
        elif hasattr(colour, '__getitem__'):
            return '#{0:02x}{1:02x}{2:02x}'.format(*colour)
        else:
            raise ValueError

    @classmethod
    def get_rgb(cls, colour):
        """get rgb of hex or name of a colour
        examples:
        >>> Colours.get_rgb('#ffff00')
        (255, 255, 0)
        >>> Colours.get_rgb('LIGHT_GREY')
        (105, 105, 105)
        """
        if isinstance(colour, str) and colour.startswith('#'):
            colour = colour.lstrip('#')
            return tuple(int(colour[i: i + 2], 16) for i in (0, 2, 4))
        elif isinstance(colour, str):
            return getattr(cls, colour.upper())

    @classmethod
    def contrasting(cls, r, g, b):
        """return white (#ffffff) if the colour is dark and
        black (#000000) if the colour is light
        :returns: hex as a string"""
        if r + b + g < 255 * 1.5:
            return '#ffffff'
        else:
            return '#000000'


parser = argparse.ArgumentParser('Zombie Survival')
parser.add_argument('-f',  '--fps',         nargs='?', type=int,   default=60,                 help='The FPS cap')
parser.add_argument('-m',  '--map',         nargs='?',             default='Pac-Man',          help='The map, available maps are in the Maps-folder')
parser.add_argument('-v',  '--volume',      nargs='?', type=float, default=0.3,                help='Volume; a float between 0 and 1')
parser.add_argument('-tl', '--tile_length', nargs='?', type=int,   default=None,               help='Length of a tile in pixels. 24, 36 and 48 are the best')
parser.add_argument('-g',  '--gender',      nargs='?',             default='f',                help='Gender of the player; \'m\' for male, \'f\' for female')
parser.add_argument('-l',  '--language',    nargs='?',             default='norsk',            help='Language of all displayed text; \'norsk\' or \'english\'.')
parser.add_argument('-fc', '--fillcolour',  nargs='?', type=tuple, default=Colours.LIGHT_GREY, help='The colour of the open tiles')
parser.add_argument('-lc', '--loopcolour',  nargs='?', type=tuple, default=Colours.DARK_GREY,  help='the colour of the walls')

flags = parser.add_argument_group()
flags.add_argument('-M',    '--mute',         action='store_true', help='Mute the game regardless of volume level')
flags.add_argument('-L',    '--not_log',      action='store_true', help='Will log regardless of optimasation mode')
flags.add_argument('-Z',    '--no_zombies',   action='store_true', help='Spawn no zombies, Debug mode must be active')
flags.add_argument('-d',    '--debug',        action='store_true', help='Set debug mode, no high scores can be set')
flags.add_argument('-s',    '--opensettings', action='store_true', help='open settings automatically')
flags.add_argument('-tk',   '--tk',           action='store_true', help='Use tkinter even though pyqt is available')
flags.add_argument('-stfu', '--stfu',         action='store_true', help='disable stdout')

_args, unknown = parser.parse_known_args()


class _Options:
    monitor_w, monitor_h = get_resolution()

    def __init__(self):
        self.setmapname(_args.map + '.txt')
        self.settilelength(_args.tile_length)
        self.setfps(_args.fps)
        self.update_speeds()
        self.update_size()
        self.volume = _args.volume
        self.setmute(_args.mute)
        self.gender = _args.gender
        self.no_zombies = _args.no_zombies
        self.debug = _args.debug
        self.not_log = _args.not_log
        self.set_language(_args.language)
        self.fillcolour = _args.fillcolour
        self.loopcolour = _args.loopcolour
        self.opensettings = _args.opensettings
        self.tk = _args.tk
        self.stfu = _args.stfu
        self.assertions()
        try:
            self.warnings()
        except AssertionError as e:
            warnings.warn(str(e))

    def getmute(self):
        return self._mute

    def setmute(self, new):
        self._mute = new
        self.volume *= (not new)

    mute = property(getmute, setmute)

    def getmapname(self):
        return self._mapname

    def setmapname(self, new):
        self._mapname = new
        self.mappath = 'assets/Maps/{}'.format(self.mapname)
        with open(self.mappath) as file:
            file_str = file.read()
            self.tiles_x = file_str.find('\n')
            if self.tiles_x == -1:
                # If the file is one line
                self.tiles_x = len(file_str)
            self.tiles_y = file_str.count('\n') + 1  # +1 because there is no '\n' on the last line
        if hasattr(self, '_tilelength'):
            self.update_size()

    mapname = property(getmapname, setmapname)

    def gettilelength(self):
        return self._tilelength

    def settilelength(self, new):
        if new is None:
            tile_length_width = _Options.monitor_w // self.tiles_x
            tile_length_width -= tile_length_width % 12
            tile_length_height = _Options.monitor_h // self.tiles_y
            tile_length_height -= tile_length_height % 12
            self._tilelength = min(tile_length_width, tile_length_height)
        else:
            self._tilelength = new
        if hasattr(self, '_fps'):
            self.update_speeds()
        self.update_size()

    tile_length = property(gettilelength, settilelength)

    def getfps(self):
        return self._fps

    def setfps(self, new):
        self._fps = new
        self.update_speeds()

    fps = property(getfps, setfps)

    def get_language(self):
        return self._language

    def set_language(self, lang):
        self._language = lang
        if lang == 'norsk':
            locale.setlocale(locale.LC_ALL, 'NOR')
        elif lang == 'english':
            locale.setlocale(locale.LC_NUMERIC, 'GBR')
        else:
            raise ValueError(lang)

    language = property(get_language, set_language)

    def update_speeds(self):
        _divs_of_tl = [self.tile_length // x for x in range(1, self.tile_length)
                       if self.tile_length / x % 1 == 0]
        self.speed = min(_divs_of_tl, key=lambda x: abs(x - 240 / self.fps))
        self.bullet_vel = min(max(400 / self.fps, 1), self.tile_length)

    def update_size(self):
        self.width = self.tiles_x * self.tile_length
        self.height = self.tiles_y * self.tile_length
        self.screen_size = self.width, self.height

    def assertions(self):
        assert os.path.isfile(self.mappath), self.mappath + ' finnes ikke..'
        assert 10 < self.fps < 180, 'FPS må være mellom 10 og 180.'
        assert 0 <= self.volume <= 1, 'Volumet må være mellom 0 or 1, inkludert 0 og 1.'
        assert 11 < self.tile_length, 'Flislengden må være mellom 11 og 100.'
        assert any(self.tile_length % i == 0 for i in range(2, self.tile_length)), \
            'Flislengden kan ikke være et primtall.'
        assert self.gender in {'f', 'm'}, 'Kjønnet må være \'m\' eller \'f\'.'
        assert (self.no_zombies and self.debug) or not self.no_zombies, \
            'Feilsøkingsmodus må være aktiv for å ha ingen zombier.'

    def warnings(self):
        assert self.tile_length % 12 == 0, 'Flislengde bør være delelig med 12.'
        assert 20 < self.fps < 69, \
            'FPS bør være mellom 20 og 69 for at zombienes fart er optimal.'
        assert self.tiles_x * self.tile_length < _Options.monitor_w, \
            'Vinduet er bredere enn sjermen.'
        assert self.tiles_y * self.tile_length < _Options.monitor_h, \
            'Vinduet er høyere enn sjermen.'


Options = _Options()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    print(Colours.get_hex('red'))
    print(Colours.get_hex([255, 0, 0]))
