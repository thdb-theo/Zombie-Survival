"""This file initiate the game"""
import logging
from time import time

import pygame

from init import main; main()
from options import Options
from init_screen import main; main()
from miscellaneous import text, game_over
from zombie import Zombie
from survivor import Survivor
from bullet import Bullet
from pickup import PickUp
from interaction import interaction
from tile import Tile
from drop import Drop

pygame.mixer.music.load('assets/Audio/theme.mp3')
pygame.mixer.music.set_volume(Options.volume)

display = pygame.display.set_mode(Options.screen_size, pygame.NOFRAME)


def main():
    Tile.create()
    survivor = Survivor(*Tile.random_open_tile())
    clock = pygame.time.Clock()
    logging.debug('options: %s', Options.__dict__)
    main_loop(survivor, clock)


def main_loop(survivor, clock):
    total_frames = 0
    pygame.mixer.music.play(loops=-1)
    while survivor.health > 0:
        interaction(display, survivor)
        Zombie.spawn(total_frames, survivor)
        survivor.movement()
        Tile.draw_all(display)
        text(display, survivor.health, Zombie.left_round + len(Zombie.instances),
             clock.get_fps(), Zombie.level, survivor.ammo, Survivor.power_ups)
        Bullet.update(display)
        survivor.draw(display)
        Zombie.update(display, survivor)
        PickUp.update(display, survivor, total_frames)
        Drop.update(display, survivor)
        clock.tick(Options.fps)
        pygame.display.flip()
        total_frames += 1
    game_over(display, Zombie.level)


if __name__ == '__main__':
    main()
