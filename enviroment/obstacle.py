import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, side):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()