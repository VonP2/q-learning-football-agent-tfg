import pygame

class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, size, groups, side):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()