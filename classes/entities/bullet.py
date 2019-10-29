import pygame
from config import rotate_center, WINDOW_WIDTH
from math import radians, sin, cos, atan2, degrees

LASER1_IMG = pygame.transform.scale(pygame.image.load('images/laser1.png'), (5, 100)).convert_alpha()
LASER2_IMG = pygame.transform.scale(pygame.image.load('images/laser2.png'), (5, 100)).convert_alpha()
LASER3_IMG = pygame.transform.scale(pygame.image.load('images/laser3.png'), (5, 100)).convert_alpha()
LASER4_IMG = pygame.transform.scale(pygame.image.load('images/laser4.png'), (5, 100)).convert_alpha()


class Bullet:
    def __init__(self, pos, angle, bullet_type, damage, critical_shot, target_x=None, target_y=None):
        self.chase = False
        if bullet_type == 0:
            self.img = LASER1_IMG
            self.vel = 50
            self.angle = angle

        if bullet_type == 1:
            self.img = LASER2_IMG
            self.vel = 40
            self.angle = angle

        if bullet_type == 2:
            self.img = LASER3_IMG
            self.chase = True
            self.vel = 25
            self.angle = angle

        if bullet_type == 3:
            self.img = LASER4_IMG
            self.chase = True
            self.vel = 50
            self.angle = angle

        self.crit = critical_shot
        self.damage = damage
        self.x, self.y = pos
        self.width, self.height = (self.img.get_rect().width, self.img.get_rect().height)
        self.target_x = target_x
        self.target_y = target_y

    def move(self):
        if self.chase and self.target_x is not None:
            angle_to_pos = ((degrees(
                atan2(self.target_x - self.x, self.target_y - self.y))) + 270) % 360

            self.angle = angle_to_pos - 90

        self.x += self.vel*cos(radians(self.angle+90))
        self.y -= self.vel*sin(radians(self.angle+90))

    def set_target(self, x=None, y=None):
        self.target_x = x
        self.target_y = y

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        to_draw, new_rect = rotate_center(self.img, self.angle, (self.x, self.y))
        surface.blit(to_draw, new_rect)
