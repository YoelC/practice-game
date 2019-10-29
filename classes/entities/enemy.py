import pygame
from random import randint
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from classes.decoration.healthbar import HealthBar


ENEMY_SHIPS = [pygame.transform.scale(pygame.image.load('images/enemy_ship.png'), (280//3, 190//3))]


class Enemy:
    def __init__(self, spaceship_type, x=None, y=None):
        self.spaceship_type = spaceship_type
        self.img = ENEMY_SHIPS[spaceship_type]
        self.width, self.height = self.img.get_rect().width, self.img.get_rect().height
        self.x = randint(1, WINDOW_WIDTH//self.img.get_rect().width)*self.img.get_rect().width if x is None else x
        self.y = -self.height if y is None else y
        self.x_vel = 0
        self.y_vel = -2
        health = 1

        if spaceship_type == 0:
            self.reward = 10
            health = randint(1, 2)

        self.health_bar = HealthBar(self, health, extra_height=-25)

    def move(self):
        self.x += self.x_vel
        self.y -= self.y_vel

    def hit(self, damage):
        return self.health_bar.hit(damage)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        self.health_bar.draw(surface)

