import pygame

enemy1_img = pygame.image.load('./Graphics/Enemy1.png')
enemy2_img = pygame.image.load('./Graphics/Enemy2.png')
enemy3_img = pygame.image.load('./Graphics/Enemy3.png')
enemy1_img = pygame.transform.scale(enemy1_img, (enemy1_img.get_width() * 2, enemy1_img.get_height() * 2))
enemy2_img = pygame.transform.scale(enemy2_img, (enemy2_img.get_width() * 2, enemy2_img.get_height() * 2))
enemy3_img = pygame.transform.scale(enemy3_img, (enemy3_img.get_width() * 2, enemy3_img.get_height() * 2))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.x_pos, self.y_pos = pos
        self.ix, self.iy = pos
        self.type = type
        if type == 1:
            self.image = enemy1_img.convert_alpha()
        elif type == 2:
            self.image = enemy2_img.convert_alpha()
        elif type == 3:
            self.image = enemy3_img.convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def interpolate(self, dt, speed_div):
        self.ix += (((self.x_pos - self.ix) * 3) * dt) / speed_div
        self.iy += (((self.y_pos - self.iy) * 3) * dt) / speed_div

    def update(self, dt, direction, actual_movement, camera, speed_div = 1):
        if actual_movement:
            self.x_pos += direction
        else:
            self.interpolate(dt, speed_div)

        self.rect.center = (round(self.ix - camera[0]), round(self.iy - camera[1]))