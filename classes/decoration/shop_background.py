from config import WINDOW_WIDTH, WINDOW_HEIGHT
import pygame

class ShopBackground:
    def __init__(self):
        self.imgs = []
        for i in range(60):
            self.imgs.append(pygame.transform.scale(pygame.image.load(f'images/background-gif/frame_{i}_delay-0.12s.png'), (WINDOW_WIDTH, WINDOW_HEIGHT)))
        self.current_img = 0

    def draw(self, surface):
        surface.blit(self.imgs[self.current_img//8], (0, 0))
        self.current_img += 1
        self.current_img %= 480
