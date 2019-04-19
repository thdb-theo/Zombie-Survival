import pygame
import sys
import os
from math import inf, sqrt
import randomcolor
from colormath.color_diff import delta_e_cie2000
from colormath.color_conversions import convert_color
from colormath.color_objects import sRGBColor, LabColor

sys.path.insert(0, os.getcwd().replace("\\assets\\Tools", "") + "/src/")

from maths import Color
pygame.init()


def euclidean_distance(c1, c2):
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

def test_complementary(n=10, font_size=12, fps=1):
    rand_gen = randomcolor.RandomColor()
    hex_text_colors = rand_gen.generate(count=n)
    text_colors = [Color(h) for h in hex_text_colors]
    screen = pygame.display.set_mode([font_size * 40, 20 + font_size * (len(text_colors) + 4)])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", font_size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    hex_text_colors = rand_gen.generate(count=n)
                    text_colors = [Color(h) for h in hex_text_colors]
        bg, diff = Color.complementary(*text_colors)
        least_diff_ciede = inf
        for color in text_colors:
            lab_color = convert_color(color, LabColor)
            lab_bg = convert_color(bg, LabColor)

            diff_ciede = delta_e_cie2000(lab_color, lab_bg)
            if least_diff_ciede > diff_ciede:
                least_diff_ciede = diff_ciede
                diff_euclid = euclidean_distance(color, bg)
                least_diff = color
        screen.fill(bg)
        y = 10
        for text_color in text_colors:
            font.set_underline(text_color == least_diff)
            font.set_bold(text_color == least_diff)
            text = font.render(str(text_color), 1, text_color)
            screen.blit(text, [font_size, y])
            y += font_size
        font.set_underline(False)
        font.set_bold(False)
        text_color, diff = color.complementary(bg)
        bg_text = font.render("bg: " + str(bg), 1, text_color)
        ciede_text = font.render("ciede: " + str(least_diff_ciede), 1, text_color)
        euclid_text = font.render("euclid: " + str(diff_euclid), 1, text_color)
        screen.blit(bg_text, [font_size, y + font_size])
        screen.blit(ciede_text, [font_size, y + font_size * 2])
        screen.blit(euclid_text, [font_size, y + font_size * 3])

        pygame.display.flip()
        clock.tick(fps)
if __name__ == "__main__":
    args = map(int, sys.argv[1:])
    test_complementary(*args)