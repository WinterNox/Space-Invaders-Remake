import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, s_width):
        super().__init__()
        self.x_pos, self.y_pos = pos
        self.image = pygame.image.load('./Graphics/Ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 300
        self.s_width = s_width
        self.dt = 0
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 450
        self.bullet_group = pygame.sprite.Group()
        self.health = 5
        self.score = 0
        self.bullets_shot = 0

    def get_input(self, dt):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < self.s_width:
            self.x_pos += self.speed * dt
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > 0:
            self.x_pos -= self.speed * dt

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.ready:
            self.shoot()
            self.bullets_shot += 1
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_t = pygame.time.get_ticks()
            if current_t - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def constraint(self):
        if self.x_pos + 16 > self.s_width:
            self.x_pos = self.s_width - 16
        elif self.x_pos - 16 < 0:
            self.x_pos = 16

    def shoot(self):
        self.bullet_group.add(Bullet((self.x_pos, self.y_pos), 480))

    def update(self, dt, camera):
        self.get_input(dt)
        self.recharge()
        self.constraint()
        self.bullet_group.update(dt, (camera[0], camera[1]))

        self.rect.center = (round(self.x_pos - camera[0]), round(self.y_pos - camera[1]))