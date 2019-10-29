from pygame.freetype import Font
import pygame
from math import sqrt

pygame.freetype.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 800
FPS = 60
FONT = Font('fonts/slkscr.ttf')


def rotate_center(surface, angle, pos):
    to_draw = pygame.transform.rotate(surface, angle)
    new_rect = to_draw.get_rect(center=surface.get_rect(topleft=(pos[0], pos[1])).center)
    return to_draw, new_rect


def convert_to_prefix(number, decimal=True):
    if number >= 1e9:
        return f'{round(number/1e9, 2)}B'

    elif number >= 1e6:
        return f'{round(number/1e6, 2)}M'

    elif number >= 1e3:
        return f'{round(number/1e3, 2)}k'

    return float(number) if decimal else number


def distance_two_points(x1, y1, x2, y2):
    dist = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist
