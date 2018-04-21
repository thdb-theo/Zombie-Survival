# -*- coding: utf-8 -*-
"""options and constants for the whole module and a colour class"""

import argparse
import warnings
import sys
import os
import subprocess
from maths import isprime, Colour, LIGHT_GREY, DARK_GREY
try:
    from PIL import ImageGrab
except ImportError:  # Only available on Windows and Mac
    pass


def get_resolution():
    """Get resoltution of the screen"""
    if sys.platform in {"darwin", "win32", "cygwin"}:
        # Mac and Windows
        # This takes a screenshot and returns its size
        screenshot = ImageGrab.grab()
        s = screenshot.size
        return s
    # HACK: saves resolution to a file, get results and deletes the file
    subprocess.run("xrandr  | grep \* | cut -d\" \" -f4 > resolution.txt",
                   shell=True)
    file = open("resolution.txt", "r")
    # file looks like this: "1920x1080"
    try:
        return tuple(map(int, file.read().split("x")))
    except ValueError:
        warnings.warn("""\nThis is meant for testing cython on "Bash on Ubuntu on Windows"
                          where no screen is available and thus the xrandr returns an
                          empty string and the previous statement raises a ValueError.
                          If you didn't expect this message; either there is
                          something wrong with xrandr or it couldn't find a screen.""")
        return 1280, 720
    finally:
        file.close()
        os.remove("resolution.txt")  # delete the file


parser = argparse.ArgumentParser("Zombie Survival")
parser.add_argument("-f", "--fps", nargs="?", type=int, default=60,
                    help="The FPS cap")
parser.add_argument("-m", "--map", nargs="?", default="Pac-Man",
                    help="The map, available maps are in the Maps-folder")
parser.add_argument("-v", "--volume", nargs="?", type=float, default=0.3,
                    help="Volume; a float between 0 and 1")
parser.add_argument("-tl", "--tile_length", nargs="?", type=int, default=None,
                    help="Length of a tile in pixels. 24, 36 and 48 are the best")
parser.add_argument("-g", "--gender", nargs="?", default="f",
                    help="Gender of the player; \"m\" for male, \"f\" for female")
parser.add_argument("-l", "--language", nargs="?", default="norsk",
                    help="Language of all displayed text; \"norsk\" or \"english\".")
parser.add_argument("-fc", "--fillcolour", nargs="?", type=str,
                    default=LIGHT_GREY.hex,
                    help="The colour of the open tiles")
parser.add_argument("-lc", "--loopcolour", nargs="?", type=str,
                    default=DARK_GREY.hex, help="The colour of the walls")
parser.add_argument("-dl", "--night_darkness", nargs="?", type=int,
                    default=200,
                    help="How dark the night is; between 0 and 255, where 255 is completely dark")
parser.add_argument("-t", "--torch_darkness", nargs="?", type=int, default=128,
                    help="How dark the torch is; between 0 and 255, where 255 is completely dark")
parser.add_argument("-np", "--n_points", nargs="?", type=int, default=60,
                    help="The number of points to make up the polygon which finds the players view")
parser.add_argument("-li", "--line_incr", nargs="?", type=float, default=None,
                    help="How much to increment the sightline between checks. High number makes it go through corners. Low numbers is less efficient. Defaults to tile length / 5")

flags = parser.add_argument_group()
flags.add_argument("-M", "--mute", action="store_true",
                   help="Mute the game regardless of volume level")
flags.add_argument("-L", "--not_log", action="store_true",
                   help="Will not log regardless of optimasation mode")
flags.add_argument("-Z", "--no_zombies", action="store_true",
                   help="Spawn no zombies, Debug mode must be active")
flags.add_argument("-d", "--debug", action="store_true",
                   help="Set debug mode, no high scores can be set")
flags.add_argument("-s", "--opensettings", action="store_true",
                   help="Open settings automatically")
flags.add_argument("-n", "--night", action="store_true", help="Use night mode")
flags.add_argument("-p", "--pitch_black", action="store_true",
                   help="It is pitch black")
_args, unknown = parser.parse_known_args()


# noinspection PyAttributeOutsideInit
class _Options:
    monitor_w, monitor_h = get_resolution()

    def __init__(self):
        self.setmapname(_args.map + ".txt")
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
        self.night = _args.night
        self.setpitchblack(_args.pitch_black)
        self.n_points = _args.n_points
        if _args.line_incr is None:
            self.line_increment = self._tilelength / 5
        else:
            self.line_increment = _args.line_incr
        self.set_language(_args.language)
        self.fillcolour = Colour(_args.fillcolour)
        self.loopcolour = Colour(_args.loopcolour)
        self.opensettings = _args.opensettings
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

    def getpitchblack(self):
        return self._pitch_black

    def setpitchblack(self, new):
        self._pitch_black = new
        if new:
            self.night_darkness = 255
            self.torch_darkness = 128
        else:
            self.night_darkness = _args.night_darkness
            self.torch_darkness = _args.torch_darkness

    pitch_black = property(getpitchblack, setpitchblack)

    def getmapname(self):
        return self._mapname

    def setmapname(self, new):
        self._mapname = new
        self.mappath = "assets/Maps/{}".format(self.mapname)
        with open(self.mappath) as file:
            file_str = file.read()
            if file_str.endswith("\n"):
                file_str.rstrip("\n")
            self.tiles_x = file_str.find("\n")
            if self.tiles_x == -1:
                # If the file is one line
                self.tiles_x = len(file_str)
            self.tiles_y = file_str.count(
                "\n") + 1  # +1 because there is no "\n" on the last line
        if hasattr(self, "_tilelength"):
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
        if hasattr(self, "_fps"):
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

    language = property(get_language, set_language)

    def update_speeds(self):
        _divs_of_tl = [self.tile_length // x for x in
                       range(1, self.tile_length)
                       if self.tile_length / x % 1 == 0]
        self.speed = min(_divs_of_tl, key=lambda x: abs(x - 240 / self.fps))
        self.bullet_vel = min(max(400 / self.fps, 1), self.tile_length)

    def update_size(self):
        self.width = self.tiles_x * self.tile_length
        self.height = self.tiles_y * self.tile_length
        self.screen_size = self.width, self.height

    def assertions(self):
        # TODO: Translate to English
        assert os.path.isfile(self.mappath), self.mappath + " finnes ikke.."
        assert 10 < self.fps < 180, "FPS må være mellom 10 og 180."
        assert 0 <= self.volume <= 1, "Volumet må være mellom 0 or 1, inkludert 0 og 1."
        assert 11 < self.tile_length < 100, "Flislengden må være mellom 11 og 100."
        assert not isprime(
            self.tile_length), "Flislengden kan ikke være et primtall."
        assert self.gender in {"f", "m"}, "Kjønnet må være \"m\" eller \"f\"."
        assert (self.no_zombies and self.debug) or not self.no_zombies, \
            "Feilsøkingsmodus må være aktiv for å ha ingen zombier."
        assert self.line_increment > 0, "-li må være et positivt tall"
        assert 0 <= self.torch_darkness <= 255, "-dl må være mellom 0 og 255"
        assert 0 <= self.night_darkness <= 255, "-tl må være mellom 0 og 255"

    def warnings(self):
        # TODO: Translate to English
        assert self.tile_length % 12 == 0, "Flislengde bør være delelig med 12."
        assert 20 < self.fps < 69, \
            "FPS bør være mellom 20 og 69 for at zombienes fart er optimal."
        assert self.tiles_x * self.tile_length < _Options.monitor_w, \
            "Vinduet er bredere enn sjermen."
        assert self.tiles_y * self.tile_length < _Options.monitor_h, \
            "Vinduet er høyere enn sjermen."
        assert self.night or not self.pitch_black, \
            "Bekmørkt har ingen effekt om natt ikke er på"


Options = _Options()

if __name__ == "__main__":
    import doctest

    doctest.testmod()

