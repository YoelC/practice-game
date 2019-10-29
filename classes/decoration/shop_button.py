import pygame
from config import FONT, convert_to_prefix


class ShopButton:
    def __init__(self, pos, text, class_instance, attribute_attached, attribute_ratio, attribute_type, upgrade_cost, upgrade_ratio, upgrade_type, attribute_extra='', gap=15, max_upgrades=0):
        self.x, self.y = pos

        self.text = text

        self.class_instance = class_instance

        self.attribute_attached = attribute_attached
        self.attribute_ratio = attribute_ratio
        self.attribute_type = attribute_type

        self.upgrade_cost = float(upgrade_cost)
        self.upgrade_cost_text = convert_to_prefix(self.upgrade_cost)
        self.upgrade_ratio = float(upgrade_ratio)
        self.upgrade_type = upgrade_type

        self.attribute_extra = attribute_extra
        self.gap = gap

        self.upgrades = 0
        self.max_upgrades = max_upgrades

        _, text1_pos = FONT.render(f'{self.text}: {getattr(self.class_instance, self.attribute_attached)}{self.attribute_extra}', (255, 255, 255), size=30)
        _, text2_pos = FONT.render(f'UPGRADE COST: ${self.upgrade_cost_text}', (255, 255, 255), size=30)
        self.rect = pygame.Rect(self.x + text1_pos.width+self.gap, self.y, text2_pos.width+self.gap*2, 50)

    def get_rect(self):
        return self.rect

    def clicked(self):
        pos = pygame.mouse.get_pos()
        mouse_hitbox = pygame.Rect(pos[0], pos[1], 1, 1)
        if mouse_hitbox.colliderect(self.get_rect()):
            return True

        return False

    def upgrade(self, money):
        if self.upgrades >= self.max_upgrades and self.max_upgrades != 0:
            return False

        if money >= self.upgrade_cost:
            money -= self.upgrade_cost
            attribute = getattr(self.class_instance, self.attribute_attached)
            if self.attribute_type == '+':
                attribute += self.attribute_ratio
            elif self.attribute_type == '*':
                attribute *= self.attribute_ratio
            elif self.attribute_type == '-':
                attribute -= self.attribute_ratio

            if self.upgrade_type == '+':
                self.upgrade_cost += self.upgrade_ratio

            elif self.upgrade_type == '*':
                self.upgrade_cost = round(self.upgrade_cost * self.upgrade_ratio)

            setattr(self.class_instance, self.attribute_attached, attribute)
            self.upgrade_cost_text = convert_to_prefix(self.upgrade_cost)

            self.upgrades += 1

        return money

    def reset(self, cost, attribute):
        self.upgrade_cost = cost
        self.upgrade_cost_text = convert_to_prefix(self.upgrade_cost)

        setattr(self.class_instance, self.attribute_attached, attribute)

        self.upgrades = 0

    def draw(self, surface, player_money):
        if self.upgrades >= self.max_upgrades and self.max_upgrades != 0:
            text1, text1_pos = FONT.render(f'{self.text}: {convert_to_prefix(round(getattr(self.class_instance, self.attribute_attached), 4))}{self.attribute_extra} |', (255, 255, 255), size=30)
            text2, text2_pos = FONT.render(f' UPGRADE COST: MAX LVL', (255, 0, 0), size=30)

        else:
            text1, text1_pos = FONT.render(f'{self.text}: {convert_to_prefix(round(getattr(self.class_instance, self.attribute_attached)), 4)}{self.attribute_extra} |', (255, 255, 255), size=30)
            text2, text2_pos = FONT.render(f' UPGRADE COST: ${self.upgrade_cost_text}', (0, 255, 0) if player_money >= self.upgrade_cost else (255, 0, 0), size=30)

        self.rect = pygame.Rect(self.x, self.y, text2_pos.width+self.gap*2 + text1_pos.width+self.gap + 10, 50)
        pygame.draw.rect(surface, (0, 0, 0), self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 4)
        surface.blit(text1, (self.x + self.gap*2, self.y+self.rect.height/2-text1_pos.height/2))
        surface.blit(text2, (self.x + text1_pos.width+self.gap*2, self.y+self.rect.height/2-text2_pos.height/2))
