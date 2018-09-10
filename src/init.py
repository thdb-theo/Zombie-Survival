"""Initiate pygame, logging and other things"""

import pygame
import os
import logging

from options import Options


pygame.mixer.pre_init(44100, -16, 1, 512)  # Makes all gun sounds play
# Without this, only some play because they are so close together

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Zombie Survival")

if not Options.not_log:
    logging.basicConfig(filename="src/logging.log", level=logging.NOTSET,
                        filemode="w",
                        format="%(asctime)s:%(msecs)03d %(filename)s "
                        "%(levelname)s %(funcName)s -> %(message)s",
                        datefmt="%d.%m.%Y %H:%M:%S")
else:
    logging.basicConfig(filename="src/logging.log",
                        filemode="w", level=logging.DEBUG)
    logging.info("Optimisation mode set. Logging was disabled")
    logging.disable(50)
os.environ["SDL_VIDEO_WINDOW_POS"] = "1, 1"
