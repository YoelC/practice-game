import pygame
from random import randint
from config import WINDOW_WIDTH, WINDOW_HEIGHT, rotate_center


ASTEROID_IMG = pygame.image.load('images/asteroid.png')


class Background:
    def __init__(self, amount_stars):
        self.elements = []
        for i in range(amount_stars):
            self.generate_star()
        self.x_accel = 0
        self.y_accel = 0

        for i in range(amount_stars//20):
            self.generate_asteroid()

    def move(self):
        for i, element in enumerate(self.elements):
            element.y_vel += self.y_accel
            element.x_vel += self.x_accel
            element.move()

            if isinstance(element, Star):
                if element.x > WINDOW_WIDTH:
                    self.generate_star(x=0 - element.width)
                    self.elements.pop(i)

                if element.x + element.width < 0:
                    self.generate_star(x=WINDOW_WIDTH)
                    self.elements.pop(i)

                if element.y > WINDOW_HEIGHT:
                    self.generate_star(y=0 - element.height)
                    self.elements.pop(i)

                if element.y + element.height < 0:
                    self.generate_star(y=WINDOW_HEIGHT)
                    self.elements.pop(i)

            elif isinstance(element, Asteroid):
                if element.x > WINDOW_WIDTH:
                    self.generate_asteroid(x=0 - element.width)
                    self.elements.pop(i)

                if element.x + element.width < 0:
                    self.generate_asteroid(x=WINDOW_WIDTH)
                    self.elements.pop(i)

                if element.y > WINDOW_HEIGHT:
                    self.generate_asteroid(y=0 - element.height)
                    self.elements.pop(i)

                if element.y + element.height < 0:
                    self.generate_asteroid(y=WINDOW_HEIGHT)
                    self.elements.pop(i)

    def generate_star(self, x=None, y=None):
        if x is None:
            x = randint(1, WINDOW_WIDTH)

        if y is None:
            y = randint(1, WINDOW_HEIGHT)

        color = randint(64, 255)
        size = color / 32
        y_vel = -size / 4
        x_vel = 0
        self.elements.append(Star(pos=(x, y, size, size), color=(color, color, color), vel=(x_vel, y_vel)))

    def generate_asteroid(self, x=None, y=None):
        if x is None:
            x = randint(1, WINDOW_WIDTH)

        if y is None:
            y = randint(1, WINDOW_HEIGHT)

        size = randint(6, 48)
        y_vel = -size / 32
        x_vel = 0
        rotation_vel = randint(1, 1000) / 1000
        self.elements.append(Asteroid(pos=(x, y), vel=(x_vel, y_vel), rotation_vel=rotation_vel, size=size))

    def draw(self, surface):
        for star in self.elements:
            star.draw(surface)


class Star:
    def __init__(self, pos, color, vel):
        self.x, self.y, self.width, self.height = pos
        self.x_vel, self.y_vel = vel
        self.color = color

    def move(self):
        self.x += self.x_vel
        self.y -= self.y_vel

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))


class Asteroid:
    def __init__(self, pos, vel, rotation_vel, size):
        self.x, self.y = pos
        self.img = pygame.transform.scale(ASTEROID_IMG, (size, size))
        self.width, self.height = self.img.get_rect().width, self.img.get_rect().height
        self.x_vel, self.y_vel = vel
        self.rotation_vel = rotation_vel
        self.angle = 0

    def move(self):
        self.x += self.x_vel
        self.y -= self.y_vel
        self.angle += self.rotation_vel

    def draw(self, surface):
        to_draw, new_rect = rotate_center(self.img, self.angle, (self.x, self.y))
        surface.blit(to_draw, new_rect)

