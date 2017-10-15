"""The intro screen"""
import sys

import pygame
import xml.etree.ElementTree as ET

from init import main; main()
from options import Options, Colours
import settings


text_tree = ET.parse('src/screen_text.xml')
root = text_tree.getroot()


def middle_of_screen(text):
    return Options.width // 2 - text.get_rect().width // 2


def main():
    screen = pygame.display.set_mode(Options.screen_size)
    clock = pygame.time.Clock()
    intro_img = pygame.image.load('assets/Images/intro.jpg')
    scaled_intro_img = pygame.transform.scale(intro_img, (Options.width, Options.height))
    move_text = root.find('./init/move').get(Options.language)
    shoot_text = root.find('./init/shoot').get(Options.language)
    weapon_text = root.find('./init/weapon').get(Options.language)
    settings_text = root.find('./init/settings_').get(Options.language)
    begin_text = root.find('./init/begin').get(Options.language)
    ctrl_font_size = 100
    ctrl_font = pygame.font.SysFont('Courier', ctrl_font_size)
    if 'halo3' in pygame.font.get_fonts():
        title_font = pygame.font.SysFont('Halo3', 55)
    else:
        title_font = pygame.font.SysFont('Courier', 55)
    title_font_size = 100

    ctrl_start_y = Options.height // 4
    y_interval = Options.height // 6
    title_y = Options.height // 15
    while ctrl_font_size > 0:
        ctrl_font = pygame.font.SysFont('Courier', ctrl_font_size)
        move = ctrl_font.render(move_text, 1, Colours.WHITE)
        shoot = ctrl_font.render(shoot_text, 1, Colours.WHITE)
        weapon = ctrl_font.render(weapon_text, 1, Colours.WHITE)
        set_text = ctrl_font.render(settings_text, 1, Colours.WHITE)
        begin = ctrl_font.render(begin_text, 1, Colours.WHITE)
        ctrl_font_size -= 1
        if begin.get_rect().width < Options.width:
            break
    else:  # No break
        pygame.quit()
        raise OverflowError('Couldn\'t fit ctrltext on screen')
    while title_font_size > 0:
        if 'halo3' in pygame.font.get_fonts():
            title_font = pygame.font.SysFont('Halo3', title_font_size)
        else:
            title_font = pygame.font.SysFont('Courier', title_font_size)
        title = title_font.render(' Zombie Survival ', 1, Colours.WHITE)
        title_font_size -= 1
        if title.get_rect().width < Options.width:
            break
    else:
        pygame.quit()
        raise OverflowError('Couldn\'t fit titletext on screen')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings.main()
                elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()
                elif event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

        screen.blit(scaled_intro_img, (0, 0))
        screen.blit(title, (middle_of_screen(title), title_y))
        screen.blit(move, (middle_of_screen(move), ctrl_start_y))
        screen.blit(shoot, (middle_of_screen(shoot), ctrl_start_y + y_interval))
        screen.blit(weapon, (middle_of_screen(weapon), ctrl_start_y + y_interval * 2))
        screen.blit(set_text, (middle_of_screen(set_text), ctrl_start_y + y_interval * 3))
        screen.blit(begin, (middle_of_screen(begin), ctrl_start_y + y_interval * 4))
        pygame.display.flip()
        clock.tick(10)


if __name__ == '__main__':
    main()
