import pygame, math

bg_tile_img = pygame.image.load('./Graphics/Background Tile.png')

class Background_Tile(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x_pos, self.y_pos = pos
        self.bg_speed = 0
        # (448 + 128, 512 + 128)
        self.image = pygame.Surface((576, 640))

        for r_index, row in enumerate(range(9)):
            for c_index, col in enumerate(range(10)):
                x = r_index * 64
                y = c_index * 64
                self.image.blit(bg_tile_img, (x, y))

        self.image = self.image.convert()

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, dt, x_speed, y_speed, camera):
        self.bg_speed = 20
        self.x_pos += x_speed * dt
        self.y_pos += y_speed * dt

        if self.x_pos >= 0:
            self.x_pos = -64
        elif self.x_pos < -64:
            self.x_pos = 0
        
        if self.y_pos >= 0:
            self.y_pos = -64
        elif self.y_pos < -64:
            self.y_pos = 0

        self.rect.topleft = (round(self.x_pos - camera[0]), round(self.y_pos - camera[1]))