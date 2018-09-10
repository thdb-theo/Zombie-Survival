import pygame
import sys
import os
from math import inf
sys.path.insert(0, os.getcwd().replace("\\assets\\Tools", "") + "/src/")

from maths import Colour
pygame.init()


def test_complementary(n=10, font_size=12, fps=1):
    text_colours = [Colour.random() for _ in range(n)]
    screen = pygame.display.set_mode([font_size * 20, 20 + font_size * (len(text_colours) + 4)])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", font_size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    text_colours = [Colour.random() for _ in range(n)]
        bg = Colour.complementary(*text_colours)
        least_diff_ciede = inf
        for colour in text_colours:
            diff_ciede = colour.ciede2000(bg)
            if least_diff_ciede > diff_ciede:
                least_diff_ciede = diff_ciede
                diff_euclid = colour.euclidean_distance(bg)

                least_diff = colour
        screen.fill(bg)
        y = 10
        for text_colour in text_colours:
            font.set_underline(text_colour == least_diff)
            font.set_bold(text_colour == least_diff)
            text = font.render(str(text_colour), 1, text_colour)
            screen.blit(text, [font_size, y])
            y += font_size
        font.set_underline(False)
        font.set_bold(False)
        text_colour = Colour.complementary(bg)
        bg_text = font.render("bg: " + str(bg), 1, text_colour)
        ciede_text = font.render("ciede: " + str(least_diff_ciede), 1, text_colour)
        euclid_text = font.render("euclid: " + str(diff_euclid), 1, text_colour)
        screen.blit(bg_text, [font_size, y + font_size])
        screen.blit(ciede_text, [font_size, y + font_size * 2])
        screen.blit(euclid_text, [font_size, y + font_size * 3])

        pygame.display.flip()
        clock.tick(fps)
if __name__ == "__main__":
    args = map(int, sys.argv[1:])
    test_complementary(*args)