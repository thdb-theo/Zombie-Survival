"""various functions that don't fit in any other file"""

import math
import sys
import os
import locale
from functools import partial, reduce
import logging
import json

import pygame

import init as _
from options import Options, Colours
from maths import Vector
from tile import Tile

if __name__ == '__main__':
    misc_screen = pygame.display.set_mode((Options.width, Options.height))

stats = {'Zombies Killed': 0,
         'Bullets Fired': 0,
         'Bullets Hit': 0}

clock = pygame.time.Clock()

data = json.load(open('src/screen_text.json'))

def get_text(area, name):
    return data[area][name][Options.language]


def make_partialable(func):
    def wrapper(a, b, c=None):
        try:
            return func(a, b, c)
        except TypeError:
            return func(a, b)
    return wrapper


rotate = make_partialable(pygame.transform.rotate)
flip = make_partialable(pygame.transform.flip)
# So flip and rotate accept keywords to be used by partial

new_dir_func = {math.pi / 2: partial(rotate, b=270),
                math.pi * 3 / 2: partial(rotate, b=90),
                math.pi: lambda x: x,
                0: partial(flip, b=True, c=False)}
# transform image from angle in radians
# Because the zombie image is facing east the rotation angle is π rad less.
# rotating upwards would be π/2 - π = -π/2 which when is equivalent of rotating by 3π/2
# because pygame doesn't allow negative angles


def rotated(img, new_dir):
    """Rotates img new_dir radians"""
    return new_dir_func[new_dir](img)


def further_than(tile_idx, survivor, min_dist):
    """Return True if a tile is further than min_dist away from survivor, else False"""
    tile = Tile.instances[tile_idx].pos
    dist = (survivor.pos - tile).magnitude()
    return dist > min_dist


def scale(img, size=Tile.size):
    if isinstance(size[0], float):
        return pygame.transform.scale(img, size.as_ints())
    else:
        return pygame.transform.scale(img, size)


font = pygame.font.Font('assets/Fonts/ModifiedDeadFontWalking.otf', Options.width // 30)

text_render = partial(lambda x, y, z: font.render(x, y, z), y=1, z=Colours.WHITE)
*_, text_width, text_height = text_render('T').get_rect()

lifes_text = get_text('info', 'lifes')
zombies_left_text = get_text('info', 'zombies_left')
round_text = get_text('info', 'round')
ammo_text = get_text('info', 'ammo')
fps_text = get_text('info', 'fps')
power_up_text = get_text('info', 'power_up')
logging.debug('font size: %s, text_height: %s, text_width: %s',
              Options.width // 30, text_height, text_width)


def text(screen, health, len_zombies, fps, level, ammo, power_ups):
    """Writes all the text during the standard game loop"""
    lifes_text_f = lifes_text.format(math.ceil(health))
    screen.blit(text_render(lifes_text_f), (0, 0))
    zombies_left_text_f = zombies_left_text.format(len_zombies)
    screen.blit(text_render(zombies_left_text_f), (text_width * len(lifes_text_f) + Options.width // 25, 0))
    round_text_f = round_text.format(level)
    screen.blit(text_render(round_text_f), (Options.width - text_width * len(round_text_f), 0))
    ammo_text_f = ammo_text.format(ammo)
    screen.blit(text_render(ammo_text_f), (Options.width - text_width * len(ammo_text_f), Options.height - text_height))
    fps_text_f = fps_text.format(locale.format('%0.1f', fps))
    screen.blit(text_render(fps_text_f), (0, Options.height - text_height))
    power_up_text_f = power_up_text.format(list(power_ups))
    screen.blit(text_render(power_up_text_f), (0, Options.height - text_height * 2))


def pause(screen, level):
    """Pauses the game until p is pressed
    red cross quit the game
    escape show results"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return
                if event.key == pygame.K_ESCAPE:
                    game_over(screen, level)
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()
        clock.tick(5)


def game_over(screen, level):
    """The screen after the game is over
    Display stats and all time high score"""

    font_size = 100
    killed_text = get_text('game_over', 'killed')
    fired_text = get_text('game_over', 'fired')
    accuracy_text = get_text('game_over', 'accuracy')
    level_text = get_text('game_over', 'level')
    high_score_text = get_text('game_over', 'high_score')
    killed_text_f = killed_text.format(stats['Zombies Killed'])
    fired_text_f = fired_text.format(stats['Bullets Fired'])
    try:
        accuracy_num = stats['Bullets Hit'] / stats['Bullets Fired'] * 100
    except ZeroDivisionError:
        accuracy_num = 0.0
    accuracy_text_f = accuracy_text.format(accuracy_num)

    level_text_f = level_text.format(level)
    try:
        with open('src/high_score.json', 'r') as file_read_m:
            file_txt = json.loads(file_read_m.read())  # Read the file
            current_high = file_txt[Options.mapname]  # The the high_score of the map that was played
    except Exception as e:
        high_score = 0 if Options.debug else level
        if isinstance(e, FileNotFoundError):
            with open('src/high_score.json', 'w') as file_write_m:
                json.dump({Options.mapname: high_score}, file_write_m)
        elif isinstance(e, KeyError):
            with open('src/high_score.json', 'rb+') as f:
                f.seek(-1, 2)  # HACK: Places the cursor on the last line and before the '}'
                string = ', "{0}": {1}}}'.format(Options.mapname, high_score)
                f.write(bytes(string, 'utf-8'))
        else:
            raise e
    else:
        if level > current_high and not Options.debug:
            file_txt[Options.mapname] = level
            with open('src/high_score.json', 'w') as write_file:  # Open file again in write mo
                json.dump(file_txt, write_file)
            high_score = level
        else:
            high_score = current_high

    high_score_text_f = high_score_text.format(high_score)

    while font_size > 0:
        font = pygame.font.SysFont('Courier', font_size)
        killed = font.render(killed_text_f, 1, Colours.WHITE)
        fired = font.render(fired_text_f, 1, Colours.WHITE)
        accuracy = font.render(accuracy_text_f, 1, Colours.WHITE)
        level = font.render(level_text_f, 1, Colours.WHITE)
        high_score = font.render(high_score_text_f, 1, Colours.WHITE)
        font_size -= 1
        if accuracy.get_rect().width < Options.width // 2:
            break
    else:  # No break
        pygame.quit()
        raise OverflowError('Couldn\'t fit the text on the screen. text_width: {},'
                            'width / 2: {}'.format(accuracy.get_rect().width, Options.width / 2))
    game_over_img = pygame.image.load('assets/Images/Other/game_over2.png')
    scaled_img = scale(game_over_img, (Options.width, Options.height // 2))
    y_interval = Options.height // 6
    level_pos = Options.width // 15, Options.height // 4
    high_score_pos = Options.width // 2, Options.height // 4
    killed_pos = Options.width // 15, Options.height // 4 + y_interval
    fired_pos = Options.width // 15, Options.height // 4 + y_interval * 2
    accuracy_pos = Options.width // 15, Options.height // 4 + y_interval * 3

    while True:
        screen.fill(Colours.BLACK)
        screen.blit(scaled_img, (0, 0))
        screen.blit(level, level_pos)
        screen.blit(high_score, high_score_pos)
        screen.blit(killed, killed_pos)
        screen.blit(fired, fired_pos)
        screen.blit(accuracy, accuracy_pos)
        pygame.display.flip()
        pygame.time.wait(500)
        pygame.event.wait()
        pygame.quit()
        sys.exit()


class NextRoundCountdown:
    """A countdown between rounds
    params:
    time: the time of the pause between rounds in frames"""
    text_x, text_y = None, None

    def __init__(self, time):
        self.finished = time
        self.time_passed = 0
        self.colour = Colours.LIGHT_BLUE

    def update(self, screen):
        self.time_passed += 1
        start_angle = math.pi / 2
        proportion = self.time_passed / self.finished
        end_angle = -math.pi * (4 * proportion - 5) / 2
        diameter = Options.width // 5
        x = Options.width // 2 - diameter // 2
        y = Options.height // 2 - diameter // 2
        rect = x, y, diameter, diameter
        pygame.draw.arc(screen, self.colour, rect, start_angle, end_angle,
                        diameter // 5)
        time_left = (self.finished - self.time_passed) / Options.fps
        formatted = locale.format('%0.1f', time_left)
        text_ = get_text('info', 'next_round').format(formatted)
        rendered = text_render(text_)
        if NextRoundCountdown.text_x is None:
            NextRoundCountdown.text_x = Options.width // 2 - rendered.get_rect().width // 2
            NextRoundCountdown.text_y = Options.height // 2 - rendered.get_rect().height // 2
        screen.blit(rendered, (NextRoundCountdown.text_x, NextRoundCountdown.text_y))


if __name__ == '__main__':
    game_over(misc_screen, 1)
    import doctest
    doctest.testmod()
