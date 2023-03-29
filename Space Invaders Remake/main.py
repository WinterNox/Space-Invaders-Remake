import pygame, time, math, random, json
from player import Player
from background import Background_Tile
import block
from enemies import Enemy
from bullet2 import Bullet2
from particle import Particle
from floating_message import Message


class Game:
    def __init__(self):
        self.gaming = True
        self.highscore = 0
        self.camera_x, self.camera_y = 0, 0
        self.screen_shake = 0

        self.player_sprite = Player((224, 464), s_width)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.backgrond = pygame.sprite.Group()
        self.bullets_hit = 0

        self.transition_img = pygame.Surface((896, 512))
        self.transition_img.fill((8, 0, 16))
        self.transition_rect = self.transition_img.get_rect()
        self.transition_rect.topleft = (0, 0)

        self.backgrond.add(Background_Tile((-64, -64)))

        self.heart_img = pygame.image.load('./Graphics/Heart.png').convert_alpha()
        self.heart_img = pygame.transform.scale(self.heart_img, (self.heart_img.get_width() * 2, self.heart_img.get_height() * 2))

        self.dust_img = pygame.image.load('./Graphics/Pixel.png').convert()
        self.dust_img = pygame.transform.scale(self.dust_img, (self.dust_img.get_width() * 2, self.dust_img.get_height() * 2))

        self.shield_shape = block.shape
        self.shield_group = pygame.sprite.Group()
        self.init_shields()

        self.enemy_group = pygame.sprite.Group()
        self.enemy_dir = 28
        self.enemy_speed_mult = 1
        self.init_enemies_num = 35
        self.enmspeed = 1200
        self.round = 1
        m = Message(f'ROUND {self.round}', (224, 256), 2500, font32)
        self.init_enemies(5, 7)
        self.rows, self.cols = 5, 7
        self.t_of_last_move = 0

        self.shooting_group = pygame.sprite.Group()
        self.t_of_last_shot = 0
        self.enm_bullet_group = pygame.sprite.Group()

        self.explosion_group = pygame.sprite.Group()

        self.messages = pygame.sprite.Group()
        self.messages.add(m)

    def write(self, text, pos, rect = 'topleft'):
        if rect == 'center':
            for l_index, line in enumerate(str(text).split('\n')):
                image = font.render(line, True, (255, 255, 255)).convert_alpha()
                rect = image.get_rect(center=(pos[0], pos[1] + (l_index * 24)))
                screen.blit(image, rect)
        else:
            for l_index, line in enumerate(str(text).split('\n')):
                image = font.render(line, True, (255, 255, 255)).convert_alpha()
                rect = image.get_rect(topleft=(pos[0], pos[1] + (l_index * 24)))
                screen.blit(image, rect)

    def init_enemies(self, rows, cols):
        self.player.sprite.bullet_group.empty()
        self.init_enemies_num = 0
        if self.gaming:
            for r_index, row in enumerate(range(rows)):
                for c_index, col in enumerate(range(cols)):
                    x, y = c_index * 56 + 28, r_index * 48 + 28 - ((rows - 5) * 48)

                    if r_index < rows * 1/5:
                        alien = Enemy((x, y), 3)
                    elif r_index < rows * 3/5:
                        alien = Enemy((x, y), 2)
                    elif r_index < rows * 1:
                        alien = Enemy((x, y), 1)
                    
                    self.enemy_group.add(alien)
                    self.init_enemies_num += 1

    def enemy_collision(self, dt):
        for enemy in self.enemy_group.sprites():
            if round(enemy.x_pos) + 14 >= 448:
                self.enemy_dir = -28
                self.move_down()
                self.enemy_group.update(dt, self.enemy_dir, True, (self.camera_x, self.camera_y))
                break
            elif round(enemy.x_pos) - 14 <= 0:
                self.enemy_dir = 28
                self.move_down()
                self.enemy_group.update(dt, self.enemy_dir, True, (self.camera_x, self.camera_y))
                break

    def enemy_death(self, ticks):
        if (round(ticks % 900, -1) < 60) and (ticks - self.t_of_last_shot > 1000):
            self.shooting_group.empty()
            self.t_of_last_shot = ticks
            for enemy in self.enemy_group.sprites():
                if abs(enemy.rect.centerx - self.player_sprite.rect.centerx) < 64:
                    self.shooting_group.add(enemy)

            if bool(self.shooting_group.sprites()):
                shooter_num = random.randint(0, len(self.shooting_group.sprites()) - 1)
                shooter = self.shooting_group.sprites()[shooter_num]
                bullet2 = Bullet2(shooter.rect.center, 360, math.atan2(self.player_sprite.rect.centery - shooter.rect.centery, self.player_sprite.rect.centerx - shooter.rect.centerx))
                self.enm_bullet_group.add(bullet2)

        for enemy in self.enemy_group.sprites():
            for bullet in self.player.sprite.bullet_group.sprites():
                if enemy.rect.colliderect(bullet.rect):
                    enemy.kill()
                    bullet.kill()
                    self.bullets_hit += 1
                    self.screen_shake = 20
                    for particle in range(random.randint(3, 9)):
                        self.explosion_group.add(Particle((enemy.x_pos, enemy.y_pos), random.randint(0, 360), random.randint(300, 600), random.randint(200, 300)))

                    if enemy.type == 1:
                        self.player_sprite.score += 10
                    elif enemy.type == 2:
                        self.player_sprite.score += 20
                    elif enemy.type == 3:
                        self.player_sprite.score += 30

    def move_down(self):
        if self.enemy_group:
            for enemy in self.enemy_group.sprites():
                enemy.y_pos += 14

    def make_shield(self, pos):
        for r_indx, row in enumerate(self.shield_shape):
            for c_indx, col in enumerate(row):
                if col == '1':
                    x, y = c_indx * 2 + pos[0], r_indx * 2 + pos[1]
                    g = block.Block(2, (x, y))
                    self.shield_group.add(g)

    def init_shields(self):
        for x in range(4):
            self.make_shield((x * 112 + 32, 400))

    def shield_destruct(self):
        for bullet in self.player.sprite.bullet_group.sprites() + self.enm_bullet_group.sprites():
            kill = False
            for block in self.shield_group.sprites():
                if bullet.rect.colliderect(block.rect):
                    block.kill()
                    kill = True
                    self.explosion_group.add(Particle(block.rect.center, random.randint(0, 360), random.randint(0, 700), random.randint(100, 300)))
            if kill:
                bullet.kill()  



    def player_health(self):
        for bullet2 in self.enm_bullet_group.sprites():
            if bullet2.rect.colliderect(self.player_sprite.rect):
                bullet2.kill()
                for x in range(random.randint(15, 30)):
                    self.explosion_group.add(Particle((self.player_sprite.x_pos, self.player_sprite.y_pos), random.randint(0, 360), random.randint(200, 800), random.randint(750, 1250)))
                self.player_sprite.health -= 1
                self.screen_shake = 60
                if self.player_sprite.health <= 0:
                    self.screen_shake = 120
                    for x in range(random.randint(25, 50)):
                        self.explosion_group.add(Particle((self.player_sprite.x_pos, self.player_sprite.y_pos), random.randint(0, 360), random.randint(500, 1600), random.randint(1500, 6000)))
                    self.enemy_group.empty()
                    self.player.sprite.bullet_group.empty()
                    self.gaming = False
                    

        if self.player_sprite.health > 0:
            for heart_num, heart in enumerate(range(self.player_sprite.health)):
                screen.blit(self.heart_img, (8 - (self.camera_x / 2), 8 + (heart_num * 24) - (self.camera_y / 2)))
        else:
            write('YOU LOST', (224, 256), 'center', 32)

    def run(self, dt, cam_shake):
        ticks = pygame.time.get_ticks()
        if self.screen_shake > 0 and cam_shake:
            self.screen_shake -= 60 * dt
            self.camera_x = random.uniform(-4 * self.screen_shake, 4 * self.screen_shake) / 40
            self.camera_y = random.uniform(-4 * self.screen_shake, 4 * self.screen_shake) / 40

        if self.gaming:
            self.player.update(dt, (self.camera_x, self.camera_y))
        self.backgrond.update(dt, 0, 60, (self.camera_x / 2, self.camera_y / 2))

        self.enemy_speed_mult = math.sqrt(len(self.enemy_group.sprites()) / self.init_enemies_num)
        if ticks - self.t_of_last_move > self.enmspeed * self.enemy_speed_mult:
            self.t_of_last_move = ticks
            self.enemy_group.update(dt, self.enemy_dir, True, (self.camera_x, self.camera_y), self.enemy_speed_mult)
            self.enemy_collision(dt)
        else:
            self.enemy_group.update(dt, self.enemy_dir, False, (self.camera_x, self.camera_y), self.enemy_speed_mult)
        self.enemy_death(ticks)
        self.enm_bullet_group.update(dt, (self.camera_x, self.camera_y))
        self.shield_destruct()
        self.explosion_group.update(dt, ticks, self.camera_x, self.camera_y)
        self.messages.update(ticks, dt)

        self.backgrond.draw(screen)
        self.messages.draw(screen)
        self.explosion_group.draw(screen)
        self.enemy_group.draw(screen)
        self.player.sprite.bullet_group.draw(screen)
        self.enm_bullet_group.draw(screen)
        if self.gaming:
            self.player.draw(screen)
        self.shield_group.draw(screen)
        self.write(f'SCORE:\n{self.player_sprite.score}', (32 - (self.camera_x / 2), 8 - (self.camera_y / 2)))

        if not bool(self.enemy_group.sprites()) and self.gaming:
            self.init_enemies(self.rows + 1, self.cols)
            self.init_enemies_num = (self.rows + 1) * self.cols
            self.enmspeed -= 50
            self.rows += 1
            self.round += 1
            m = Message(f'ROUND {self.round}', (224, 256), 2500, font32)
            self.messages.add(m)

        self.player_health()

        if self.player_sprite.score > self.highscore:
            self.highscore = self.player_sprite.score

        if self.transition_rect.left <= 448:
            screen.blit(self.transition_img, self.transition_rect)
            self.transition_rect.x += 3600 * dt


def write(text, pos, rect = 'topleft', size = 24):
        if rect == 'center':
            for l_index, line in enumerate(str(text).split('\n')):
                if size == 24:
                    image = font.render(line, True, (255, 255, 255)).convert_alpha()
                elif size == 32:
                    image = font32.render(line, True, (255, 255, 255)).convert_alpha()
                elif size == 16:
                    image = font16.render(line, True, (255, 255, 255)).convert_alpha()
                rect = image.get_rect(center=(pos[0], pos[1] + (l_index * 24)))
                screen.blit(image, rect)
        elif rect == 'topleft':
            for l_index, line in enumerate(str(text).split('\n')):
                if size == 24:
                    image = font.render(line, True, (255, 255, 255)).convert_alpha()
                elif size == 32:
                    image = font32.render(line, True, (255, 255, 255)).convert_alpha()
                elif size == 16:
                    image = font16.render(line, True, (255, 255, 255)).convert_alpha()
                rect = image.get_rect(topleft=(pos[0], pos[1] + (l_index * 24)))
                screen.blit(image, rect)
        elif rect == 'left':
            for l_index, line in enumerate(str(text).split('\n')):
                if size == 24:
                    image = font.render(line, True, (255, 255, 255)).convert_alpha()
                elif size == 32:
                    image = font32.render(line, True, (255, 255, 255)).convert_alpha()
                elif size == 16:
                    image = font16.render(line, True, (255, 255, 255)).convert_alpha()
                rect = image.get_rect(midleft=(pos[0], pos[1] + (l_index * 24)))
                screen.blit(image, rect)


def mainmenu():
    running = True
    mouse_down = False
    options = ['START', 'CLOSE', 'OPTIONS']
    chosen_option = 0
    title_img = pygame.image.load('./Graphics/Title.png').convert_alpha()
    title_img = pygame.transform.scale(title_img, (title_img.get_width() * 3, title_img.get_height() * 3))
    title_rect = title_img.get_rect(center=(224, 100))
    fps, cam_shake = 60, True

    transitioning = False

    transition_img = pygame.Surface((896, 512))
    transition_img.fill((8, 0, 16))
    t_rect = transition_img.get_rect()
    t_rect.topleft = (-896, 0)

    while running:
        mouse_down = False
        for event in pygame.event.get():
            mx, my = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    chosen_option += 1
                if event.key == pygame.K_UP:
                    chosen_option -= 1

                if event.key == pygame.K_RETURN:
                    if chosen_option == 0:
                        transitioning = True
                    if chosen_option == 1:
                        running = False
                    if chosen_option == 2:
                        fps, cam_shake = options_menu()

        if chosen_option < 0:
            chosen_option = len(options) - 1
        elif chosen_option > len(options) - 1:
            chosen_option = 0

        screen.fill((8, 0, 16))

        screen.blit(title_img, title_rect)

        for num, option in enumerate(options):
            if option == options[chosen_option]:
                write(f'<{option}>', (224, 240 + num * 28), 'center', 32)
            else:
                write(option, (224, 240 + num * 28), 'center', 24)

        write('Press Up and Down arrow keys to navigate.\nPress Enter Key to select.', (224, 435 + math.sin(pygame.time.get_ticks() / 250) * 2.5), 'center', 16)

        if transitioning:
            screen.blit(transition_img, t_rect)
            t_rect.x += 60
            if t_rect.x >= 0:
                game(fps, cam_shake)
                running = False

        pygame.display.flip()
        clock.tick(60)


def options_menu():
    running = True
    settings = ['MAX FPS', 'CAMERA SHAKE']
    chosen_setting = 0
    framerates = [30, 60, 90, 120]
    chosen_fps = 1
    camera_shake = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_DOWN:
                    chosen_setting += 1
                elif event.key == pygame.K_UP:
                    chosen_setting -= 1

                if event.key == pygame.K_RIGHT:
                    if chosen_setting == 0:
                        chosen_fps += 1
                    elif chosen_setting == 1:
                        if camera_shake:
                            camera_shake = False
                        else:
                            camera_shake = True
                elif event.key == pygame.K_LEFT:
                    if chosen_setting == 0:
                        chosen_fps -= 1
                    elif chosen_setting == 1:
                        if camera_shake:
                            camera_shake = False
                        else:
                            camera_shake = True

        if chosen_setting > len(settings) - 1:
            chosen_setting = 0
        elif chosen_setting < 0:
            chosen_setting = len(settings) - 1

        if chosen_fps > len(framerates) - 1:
            chosen_fps = 0
        elif chosen_fps < 0:
            chosen_fps = len(framerates) - 1

        screen.fill((8, 0, 16))

        write('OPTIONS', (244, 32), 'center', 32)

        for num, setting in enumerate(settings):
            if num == chosen_setting:
                write(f'{setting}:', (32, 128 + num * 32), 'left', 32)
            else:
                write(f'{setting}:', (32, 128 + num * 32), 'left', 24)

        write(framerates[chosen_fps], (380, 128), 'left', 32 if chosen_setting == 0 else 24)
        write('ON' if camera_shake else 'OFF', (380, 160), 'left', 32 if chosen_setting == 1 else 24)

        write('Press Up and Down arrow keys to navigate.\nPress Left and Right arrow keys to change selected setting.\nPress Esc key to return to main menu.', (224, 405 + math.sin(pygame.time.get_ticks() / 250) * 2.5), 'center', 16)

        pygame.display.flip()
        clock.tick(60)
    return framerates[chosen_fps], camera_shake


def game(fps, cam_shake):
    running = True
    game = Game()
    last_time = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta = time.time() - last_time
        last_time = time.time()

        screen.fill((8, 0, 16))

        game.run(delta, cam_shake)

        print(clock.get_fps())
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    pygame.init()
    s_width, s_height = 448, 512
    logo = pygame.image.load('./Graphics/Logo.png')
    screen = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Space Invaders Remake')
    font = pygame.font.Font('./Picopixel.ttf', 24)
    font32 = pygame.font.Font('./Picopixel.ttf', 32)
    font16 = pygame.font.Font('./Picopixel.ttf', 16)
    clock = pygame.time.Clock()
          
    last_time = time.time()

    mainmenu()
    pygame.quit()
