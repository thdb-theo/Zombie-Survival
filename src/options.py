# -*- coding: utf-8 -*-
"""options for the whole module."""

import argparse
import warnings
from random import uniform
from colorsys import hls_to_rgb
import os


def get_resolution():
        """Get resoltution of the screen"""
        if os.name == 'posix':
            # For Linux, including macOS. Is not tested on Mac
            # HACK: saves resolution to a file, get results and deletes the file
            os.system("xrandr  | grep \* | cut -d' ' -f4 > resolution.txt")
            file = open('resolution.txt', 'r') 
            try:
                return tuple(map(int, file.read().split('x')))
            except ValueError:
                return 1280, 720
            finally:
                file.close()
                os.remove('resolution.txt')

        elif os.name == 'nt':
            # For Windows
            import ctypes
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            # Various other OSes, not implemented, just guess
            # TODO: find a cross platform solution
            raise OSError('Invalid OS')


parser = argparse.ArgumentParser('Zombie Survival')
parser.add_argument('-f',  '--fps',         nargs='?', type=int,   default=60,        help='The FPS cap')
parser.add_argument('-m',  '--map',         nargs='?',             default='Pac-Man', help='The map, available maps are in the Maps-folder')
parser.add_argument('-v',  '--volume',      nargs='?', type=float, default=0.3,       help='Volume; a float between 0 and 1')
parser.add_argument('-tl', '--tile_length', nargs='?', type=int,   default=None,      help='Length of a tile in pixels. 24, 36 and 48 are the best')
parser.add_argument('-g',  '--gender',      nargs='?',             default='f',       help='Gender of the player; \'m\' for male, \'f\' for female')
parser.add_argument('-l',  '--language',    nargs='?',             default='norsk',   help='Language of all displayed text; \'norsk\' or \'english\'.')

flags = parser.add_argument_group()
flags.add_argument('-M', '--mute',           action='store_true', help='Mute the game regardless of volume level')
flags.add_argument('-L', '--not_log',        action='store_true', help='Will log regardless of optimasation mode')
flags.add_argument('-Z', '--no_zombies',     action='store_true', help='Spawn no zombies, Debug mode must be active')
flags.add_argument('-d', '--debug',          action='store_true', help='Set debug mode, no high scores can be set')

_args, unknown = parser.parse_known_args()


class _Options:
    monitor_w, monitor_h = monitor_size = get_resolution()

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
        self.language = _args.language
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
            self.line_length = file_str.find('\n')
            if self.line_length == -1:
                # If the file is one line
                self.line_length = len(file_str)
            self.amnt_lines = file_str.count('\n') + 1  # +1 because there is no '\n' on the last line
        if hasattr(self, '_tilelength'):
            self.update_size()

    mapname = property(getmapname, setmapname)

    def gettilelength(self):
        return self._tilelength

    def settilelength(self, new):
        if new is None:
            tile_length_width = _Options.monitor_w // self.line_length
            tile_length_width -= tile_length_width % 12
            tile_length_height = _Options.monitor_h // self.amnt_lines
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

    def update_speeds(self):
        _divs_of_tl = [self.tile_length // x for x in range(1, self.tile_length)
                       if self.tile_length / x % 1 == 0]
        self.speed = min(_divs_of_tl, key=lambda x: abs(x - 240 / self.fps))
        self.bullet_vel = min(max(400 / self.fps, 1), self.tile_length)

    def update_size(self):
        self.width = self.line_length * self.tile_length
        self.height = self.amnt_lines * self.tile_length
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
        assert self.line_length * self.tile_length < _Options.monitor_w, \
            'Vinduet er bredere enn sjermen.'
        assert self.amnt_lines * self.tile_length < _Options.monitor_h, \
            'Vinduet er høyere enn sjermen.'


Options = _Options()


class Colours:
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
        return tuple(int(256 * i) for i in hls_to_rgb(*hsl))

    @classmethod
    def get_hex(cls, colour):
        """Get hex value of an rgb tuple or name of a colour
        if colour is a string: get hex of the class attr with that name
        if colour is a collection with three ints: get hex value"""
        if isinstance(colour, str):
            return '#{0:02x}{1:02x}{2:02x}'.format(*getattr(cls, colour.upper()))
        elif hasattr(colour, '__getitem__'):
            return '#{0:02x}{1:02x}{2:02x}'.format(*colour)
        else:
            raise ValueError


if __name__ == '__main__':
    print(Colours.get_hex('red'))
    print(Colours.get_hex([255, 0, 0]))
