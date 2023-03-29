import pygame, math

particleimg = pygame.image.load('./Graphics/Pixel.png')
particleimg = pygame.transform.scale(particleimg, (particleimg.get_width() * 2, particleimg.get_height() * 2))

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, time, color = (255, 255, 255)):
        super().__init__()
        self.init_time = pygame.time.get_ticks()
        self.x_pos, self.y_pos= pos
        self.direction = direction
        self.x_velocity, self.y_velocity = math.sin(math.radians(direction)) * speed, math.cos(math.radians(direction)) * speed
        self.time = time
        
        self.og_image = pygame.transform.rotate(particleimg.convert(), math.radians(direction))
        self.image = pygame.Surface((2, 2))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, dt, cticks, camera_x, camera_y):
        self.x_velocity -= 6 * self.x_velocity * dt
        self.y_velocity += 240 * dt
        self.y_velocity -= 6 * self.y_velocity * dt
        self.x_pos += self.x_velocity * dt
        self.y_pos += self.y_velocity * dt

        alpha = 255 - (((cticks - self.init_time) / self.time) * 255)
        if cticks - self.init_time < self.time:
            self.image.set_alpha(alpha)
        else:
            self.kill()
        self.rect.center = (round(self.x_pos - camera_y), round(self.y_pos - camera_y))
