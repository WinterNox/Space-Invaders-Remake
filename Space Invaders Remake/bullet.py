import pygame
bullet_img = pygame.image.load('./Graphics/Bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (bullet_img.get_width() * 2, bullet_img.get_height() * 2))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.x_pos, self.y_pos = pos
        self.image = bullet_img.convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self, dt, camera):
        self.y_pos -= self.speed * dt

        if self.y_pos < -600:
            self.kill()

        self.rect.center = (round(self.x_pos - camera[0]), round(self.y_pos - camera[1]))
