import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)


shape = [
    '0011111111111111100',
    '0111111111111111110',
    '1111111111111111111',
    '1111111111111111111',
    '1111111111111111111',
    '1111111111111111111',
    '1111111111111111111',
    '1100000000000000011'
]