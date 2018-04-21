"""This file initiate the game"""
import logging

import pygame

import init as _
from options import Options
from init_screen import main; main()  # This must run before tile.py is run

from miscellaneous import text, game_over
from zombie import Zombie
from survivor import Survivor
from bullet import Bullet
from pickup import PickUp
from interaction import interaction
from tile import Tile
from drop import Drop

pygame.mixer.music.load("assets/Audio/Other/theme.mp3")
pygame.mixer.music.set_volume(Options.volume)

display = pygame.display.set_mode(Options.screen_size)


def main():
    """initiate tiles, survival, clock and start music and run main loop"""
    Tile.create()
    survivor = Survivor(*Tile.random_open_tile())
    clock = pygame.time.Clock()
    logging.debug("options: %s", Options.__dict__)
    logging.debug("monitor: w=%s, h=%s", Options.monitor_w, Options.monitor_h)
    pygame.mixer.music.play(loops=-1)
    main_loop(survivor, clock)
    game_over(display, Zombie.level)


def main_loop(survivor, clock):
    total_frames = 0
    while survivor.health > 0:
        Tile.draw_all(display)
        interaction(display, survivor)
        Bullet.update(display)
        Zombie.update(display, survivor)
        PickUp.update(display, survivor, total_frames)
        Drop.update(display, survivor)
        survivor.update(display)
        Zombie.spawn(display, total_frames, survivor)
        text(display, survivor.health, Zombie.left_round + len(Zombie.instances),
             clock.get_fps(), Zombie.level, survivor.ammo, Drop.actives)
        clock.tick(Options.fps)
        pygame.display.flip()
        total_frames += 1


if __name__ == "__main__":
    main()
