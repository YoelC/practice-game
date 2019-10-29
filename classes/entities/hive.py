from classes.entities.enemy import Enemy
from random import randint


class Hive:
    def __init__(self):
        self.enemies = []
        self.spawn_rate = 100
        self.enemy_type = 0
        self.reward_ratio = 1

    def attempt_enemy_spawn(self, tick):
        if tick % self.spawn_rate == 0:
            self.enemies.append(Enemy(spaceship_type=self.enemy_type))
