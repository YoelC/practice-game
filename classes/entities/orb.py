from random import randint, choice
from config import rotate_center
from math import cos, sin, radians, degrees, atan2
import pygame


MONEY1_IMG = pygame.transform.scale(pygame.image.load('images/money1.png'), (32, 32))
MONEY2_IMG = pygame.transform.scale(pygame.image.load('images/money2.png'), (48, 48))
MONEY3_IMG = pygame.transform.scale(pygame.image.load('images/money3.png'), (64, 64))


class Orb:
    def __init__(self, pos, objective, reward, deviation=0, reward_ratio=1):
        self.x, self.y = pos
        self.x += randint(1, 25)*choice((-1, 1))
        self.y += randint(1, 25)*choice((-1, 1))

        self.x_vel = 0
        self.y_vel = 0
        self.angle = 0
        self.objective = objective

        if deviation != 0:
            self.reward = round((reward + randint(0, deviation))*reward_ratio)
        else:
            self.reward = round(reward*reward_ratio)


        if self.reward > 0:
            self.img = MONEY1_IMG

        if self.reward > 50:
            self.img = MONEY2_IMG

        if self.reward > 200:
            self.img = MONEY3_IMG

        self.width, self.height = self.img.get_rect().width, self.img.get_rect().height

    def move(self):
        x = self.objective.x + self.objective.width/2
        y = self.objective.y + self.objective.height/2

        self.angle = ((degrees(atan2(x - self.x, y - self.y))) + 270) % 360

        self.x += cos(radians(self.angle))*10
        self.y -= sin(radians(self.angle))*10

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        to_draw, new_rect = rotate_center(self.img, self.angle, (self.x, self.y))
        surface.blit(to_draw, new_rect)
