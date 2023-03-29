import pygame


class Message(pygame.sprite.Sprite):
    def __init__(self, text, pos, time, font):
        super().__init__()
        self.init_time = pygame.time.get_ticks()
        self.time = time
        self.image = font.render(text, False, (255, 255, 255))
        self.x_pos, self.y_pos = pos
        self.rect = self.image.get_rect()

    def update(self, ticks, dt):
        self.y_pos += 0 * dt

        opacity = 255 - (((ticks - self.init_time) / self.time) * 255)
        if opacity > 0:
            self.image.set_alpha(opacity)
        else:
            self.kill()
        self.rect.center = (self.x_pos, self.y_pos)