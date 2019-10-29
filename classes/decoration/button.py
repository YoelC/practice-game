from config import FONT
import pygame


class Button:
    def __init__(self, pos, text, cost=None, border=True):
        self.rect = pygame.Rect(pos)
        self.text = text
        self.cost = cost
        self.cost_text = self.cost if self.cost is not None else ''

        self.border = border

    def get_rect(self):
        return self.rect

    def update_cost(self, cost):
        self.cost = cost
        cost_str = self.cost
        digits = {
            'k': 0,
        }
        if self.cost / 1000 > 1:
            self.cost_text = f'${round(self.cost/1000, 2)}k'
        else:
            self.cost_text = self.cost

    def clicked(self):
        pos = pygame.mouse.get_pos()
        mouse_hitbox = pygame.Rect(pos[0], pos[1], 1, 1)
        if mouse_hitbox.colliderect(self.rect):
            return True
        return False

    def draw(self, surface):
        if self.border is True:
            pygame.draw.rect(surface, 0, self.rect)
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 4)

        font, font_pos = FONT.render(f'{self.text} {self.cost_text}', fgcolor=(255, 255, 255), size=30)
        surface.blit(font, (self.rect.x - font_pos.width/2 + self.rect.width/2, self.rect.y - font_pos.height/2 + self.rect.height/2))

