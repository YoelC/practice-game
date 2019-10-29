import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from random import randint, choice
from config import rotate_center
from classes.entities.bullet import Bullet
from classes.decoration.healthbar import HealthBar

pygame.init()

SHIP_IMGS = [pygame.transform.scale(pygame.image.load('images/ship1.png'), (96, 96)),
             pygame.transform.scale(pygame.image.load('images/ship2.png'), (128, 128)).convert_alpha(),
             pygame.transform.scale(pygame.image.load('images/ship3.png'), (154, 154)).convert_alpha(),
             pygame.transform.scale(pygame.image.load('images/ship4.png'), (154, 154)).convert_alpha()]


class Player:
    def __init__(self, pos):
        self.x, self.y = pos
        self.repair = False
        self.damage = 1
        self.x_vel, self.y_vel = (0, 0)
        self.angle = 0

        self.ship_level = 1
        self.current_ship_level = 1
        self.img = SHIP_IMGS[self.ship_level - 1]
        self.width, self.height = (self.img.get_rect().width, self.img.get_rect().height)

        self.center_x = self.x + self.width/2
        self.center_y = self.y + self.height/2

        self.moving_left = False
        self.moving_right = False

        self.bullets = []

        self.bullet_type = 0

        self.crit_chance = 4
        self.crit_damage = 2
        self.health = 5

        self.health_bar = HealthBar(self, self.health, extra_height=self.img.get_rect().height)

        self.delay1 = 0
        self.delay1_delay = 40

        self.money = float(0)

        self.max_vel = 6
        self.accel = 0.25

        self.repair_cost = 50

    def left(self):
        self.moving_left = True

    def right(self):
        self.moving_right = True

    def move(self):
        if self.moving_right:
            self.x_vel += self.accel

        if self.moving_left:
            self.x_vel -= self.accel

        if self.x_vel < -0 and self.moving_right:
            self.x_vel += self.accel

        if self.x_vel > 0 and self.moving_left:
            self.x_vel -= self.accel

        if self.x < 0:
            self.x = 0
            self.x_vel = 0

        if self.x > WINDOW_WIDTH-self.width:
            self.x = WINDOW_WIDTH-self.width
            self.x_vel = 0

        if self.x_vel > self.max_vel:
            self.x_vel = self.max_vel
        if self.x_vel < -self.max_vel:
            self.x_vel = -self.max_vel

        if not (self.moving_right or self.moving_left) and self.x_vel != 0:
            self.x_vel = self.x_vel * 0.95

        self.angle = -self.x_vel*2
        self.x += self.x_vel
        self.y -= self.y_vel
        self.moving_right = False
        self.moving_left = False
        self.center_x = self.x + self.width/2
        self.center_y = self.y + self.height/2

        for i, bullet in enumerate(self.bullets):
            bullet.move()

            if bullet.y < -bullet.height or bullet.x < -bullet.width or bullet.y > WINDOW_HEIGHT or bullet.x > WINDOW_WIDTH:
                self.bullets.pop(i)

    def upgrade(self):
        self.current_ship_level = self.ship_level

        if self.ship_level == 2:
            self.health = 12
            self.bullet_type = 1
            self.img = SHIP_IMGS[self.ship_level - 1]
            self.repair_cost *= 2
            self.y = WINDOW_HEIGHT - 150

        if self.ship_level == 3:
            self.health = 18
            self.bullet_type = 2
            self.img = SHIP_IMGS[self.ship_level - 1]
            self.repair_cost *= 2
            self.y = WINDOW_HEIGHT - 175

        if self.ship_level == 4:
            self.health = 30
            self.bullet_type = 3
            self.img = SHIP_IMGS[self.ship_level - 1]
            self.repair_cost *= 2
            self.y = WINDOW_HEIGHT - 175

        self.width, self.height = (self.img.get_rect().width, self.img.get_rect().height)
        self.center_x = self.x + self.width/2
        self.center_y = self.y + self.height/2

        self.health_bar = HealthBar(self, self.health, extra_height=self.img.get_rect().height)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def shoot(self):
        damage = self.damage
        self.center_x = self.x + self.width/2
        self.center_y = self.y + self.height/2
        critical_shot = randint(1, 100) <= self.crit_chance
        if critical_shot:
            damage *= self.crit_damage

        if self.ship_level == 1:
            self.bullets.append(Bullet((self.center_x-2.5, self.y), self.angle, self.bullet_type, damage, critical_shot))

        elif self.ship_level == 2:
            deviation1 = randint(1, 5)*choice((1, -1))
            deviation2 = randint(1, 5)*choice((1, -1))
            self.bullets.append(Bullet((self.center_x - 2.5, self.y), self.angle+deviation1, self.bullet_type, damage/2, critical_shot))
            self.bullets.append(Bullet((self.center_x - 2.5, self.y), self.angle+deviation2, self.bullet_type, damage/2, critical_shot))
            self.bullets.append(Bullet((self.center_x - 2.5, self.y), self.angle, self.bullet_type, damage/2, critical_shot))

        elif self.ship_level == 3:
            self.bullets.append(Bullet((self.center_x - 2.5, self.y), self.angle, self.bullet_type, damage, critical_shot))

        elif self.ship_level == 4:
            deviation1 = randint(1, 40)*choice((1, -1))
            deviation2 = randint(1, 40)*choice((1, -1))
            deviation3 = randint(1, 40)*choice((1, -1))
            deviation4 = randint(1, 40)*choice((1, -1))
            self.bullets.append(Bullet((self.center_x - 2.5 + deviation1, self.y+ deviation1), self.angle, self.bullet_type, round(damage/2, 1), critical_shot))
            self.bullets.append(Bullet((self.center_x - 2.5 + deviation2, self.y + deviation2), self.angle, self.bullet_type, round(damage/2, 1), critical_shot))
            self.bullets.append(Bullet((self.center_x - 2.5 + deviation3, self.y + deviation3), self.angle, self.bullet_type, round(damage/2, 1), critical_shot))
            self.bullets.append(Bullet((self.center_x - 2.5 + deviation4, self.y + deviation4), self.angle, self.bullet_type, round(damage/2, 1), critical_shot))
            self.bullets.append(Bullet((self.center_x - 2.5, self.y), self.angle, self.bullet_type, round(damage/2, 1), critical_shot))



    def hit(self, damage):
        self.health_bar.hit(damage)
        return self.health_bar.health <= 0

    def draw(self, surface):
        if self.ship_level != self.current_ship_level:
            self.upgrade()

        to_draw, new_rect = rotate_center(self.img, self.angle, (self.x, self.y))
        surface.blit(to_draw, new_rect)

        # pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

        for bullet in self.bullets:
            bullet.draw(surface)

        self.health_bar.draw(surface)
