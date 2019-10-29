import pygame
from random import randint, choice
from config import FONT, convert_to_prefix

pygame.init()
pygame.font.init()


def rotate_center(surface, angle, pos):
    to_draw = pygame.transform.rotate(surface, angle)
    new_rect = to_draw.get_rect(center=surface.get_rect(topleft=(pos[0], pos[1])).center)
    return to_draw, new_rect


class HitMarker:
    def __init__(self, pos, indicator, color, crit=False, crit_color=None, spread=0, extra='', delay=50, size=40, angle_variation=25, decimal=True, angle_spread=25, y_vel=1, x_spread=0, y_spread=0):
        self.x, self.y = pos[0] + randint(0, x_spread), pos[1] + randint(0, y_spread)
        if spread > 0:
            self.x += randint(1, spread)*choice((-1, 1))
            self.y += randint(1, spread)*choice((-1, 1))

        self.x_vel = 0
        self.y_vel = y_vel
        self.indicator = indicator

        self.crit = crit
        self.color = color
        self.crit_color = crit_color

        self.font = FONT
        self.delay = delay

        self.angle = angle_variation
        if angle_variation != 0 and angle_spread != 0:
            negative = choice((-1, 1))
            self.angle = randint(0, angle_spread) * negative

        self.extra = extra

        self.size = size

        self.decimal = decimal

    def move(self):
        self.x += self.x_vel
        self.y -= self.y_vel

    def draw(self, surface):
        symbol = '+' if self.indicator > 0 else '-'
        symbol = '' if self.indicator == 0 else symbol

        font1, font1_pos = self.font.render(f'{symbol}{self.extra}{convert_to_prefix(abs(self.indicator), decimal=self.decimal) if symbol != "" else ""}', fgcolor=self.color, size=self.size)

        if self.crit:
            font1, font1_pos = self.font.render(f'CRIT! {symbol}{self.extra}{convert_to_prefix(abs(self.indicator), decimal=self.decimal) if symbol != "" else ""}', fgcolor=self.crit_color, size=self.size)

        to_draw1, new_rect1 = rotate_center(font1, self.angle, (self.x - font1_pos.width/2, self.y - font1_pos.height))
        surface.blit(to_draw1, new_rect1)

        self.delay -= 1
