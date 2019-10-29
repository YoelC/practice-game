import pygame


class HealthBar:
    def __init__(self, attached, health, extra_height=0):
        self.extra_height = extra_height
        self.width, self.height = 25*health, 12.5
        self.gap_x = (attached.width - self.width) / 2
        self.gap_y = extra_height
        self.thickness = 4

        self.attached = attached

        self.max_health = health
        self.health = health

        self.color = [0, 255, 0]

    def hit(self, damage):
        self.health -= damage
        return self.health <= 0

    def draw(self, surface):
        # Changes color based on damage
        color = self.color.copy()
        danger = self.health*25
        max_danger = self.max_health*25
        ratio = danger/max_danger
        color[0] = int(round(255 - 255*ratio))
        color[1] = int(round(255*ratio))

        # Only exception being one damage

        self.width = 25*self.health
        width_temp = 25*self.max_health
        gap_x = (self.attached.width - self.width) / 2

        # Max
        pygame.draw.rect(surface, (255, 255, 255), (self.attached.x + self.gap_x - 5, self.attached.y + self.extra_height, width_temp + 10, self.height), 2)

        # Decreasing
        try:
            pygame.draw.rect(surface, color, (self.attached.x + gap_x, self.attached.y + 5 + self.extra_height, self.width, self.height - 10))

        except TypeError:
            pygame.draw.rect(surface, (255, 255, 255), (self.attached.x + gap_x, self.attached.y + 5 + self.extra_height, self.width, self.height - 10))

