"""Initiate pygame, logging and other things"""

import pygame
import os
import logging

from options import Options

initiated = False


def main():
    global initiated
    if not initiated:
        pygame.init()
        pygame.display.set_caption('Zombie Survival')
        if not Options.not_log:
            logging.basicConfig(filename='src/logging.log', level=logging.NOTSET, filemode='w',
                                format='%(asctime)s:%(msecs)03d %(filename)s %(levelname)s'
                                ' %(funcName)s -> %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
        else:
            logging.basicConfig(filename='src/logging.log', filemode='w', level=logging.DEBUG)
            logging.info('Optimisation mode set. Logging was disabled')
            logging.disable(50)
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1, 1'
        initiated = True


if __name__ == '__main__':
    main()
