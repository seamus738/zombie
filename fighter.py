import pygame
import math
from settings import *
from bullet import *
import random

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie')

clock = pygame.time.Clock()
FPS = 60
game_font=pygame.font.Font('assets/fonts/Black_Crayon.ttf', 30)

BG = pygame.image.load("assets/images/version1map.png").convert()
WORLD_WIDTH = BG.get_width()
WORLD_HEIGHT = BG.get_height()

world_surface = BG.copy()

current_level = 1
max_zombies_per_level = 1000
def game_screen():
    global first_screen
    global Second_Screen

    class Fighter(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y, scale, speed):
            self.char_type = char_type
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.speed = speed
            self.shoot_cooldown = 0
            self.direction = 1
            self.vel_y = 0
            self.in_air = True
            self.flip = False
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.health = 100
            self.max_health = self.health
            self.update_time = pygame.time.get_ticks()
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f'assets/images/{self.char_type}/idle/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            for i in range(6):
                img = pygame.image.load(f'assets/images/{self.char_type}/run/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'assets/images/{self.char_type}/death/{i}.png')
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            self.update_animation()
            self.check_alive()
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

        def move(self, moving_right, moving_left, moving_up, moving_down):
            dx = 0
            dy = 0

            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_down:
                dy = self.speed
            if moving_up:
                dy = -self.speed

            self.rect.x += dx
            self.rect.y += dy
            # check if position is valid
            if self.rect.left < 290:
                self.rect.left = 290
            if self.rect.right > WORLD_WIDTH - 1767:
                self.rect.right = WORLD_WIDTH - 1767
            if self.rect.bottom > WORLD_HEIGHT - 1880:
                self.rect.bottom = WORLD_HEIGHT - 1880
            if self.rect.top < 170:
                self.rect.top = 170

        def shoot(self, bx, by, bullet_group):
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = 20
                p_x, p_y = self.rect.center
                angle = math.atan2(by - p_y, bx - p_x)
                bvx = self.speed * math.cos(angle)
                bvy = self.speed * math.sin(angle)
                bullet = Bullet(self.rect.centerx + (self.direction * .5 * self.rect.size[0]),
                                self.rect.centery, (bvx, bvy))
                bullet_group.add(bullet)
            print(bx, by)

        def zombie_ai(self, player):
            xx = self.rect.centerx
            yy = self.rect.centery
            xxx = player.rect.centerx
            yyy = player.rect.centery
            dxx = xxx - xx
            dyy = yyy - yy

            # Calculate the angle to the player
            angle = math.atan2(dyy, dxx)

            # Calculate the change in x and y using speed
            xvx = self.speed * math.cos(angle)
            yvy = self.speed * math.sin(angle)

            # Update the zombie's position
            self.rect.centerx += xvx
            self.rect.centery += yvy

        def update_animation(self):
            ANIMATION_COOLDOWN = 200
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:
                    zombie_group.remove(zombie)
                    # self.frame_index = 7
                else:
                    self.frame_index = 0

        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(2)

        def draw(self, screen):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def draw_bg():
        world_surface.blit(BG, (0, 0))

    sound_file = pygame.mixer.Sound('assets/images/Mitch.wav')
    emma_file = pygame.mixer.Sound('assets/images/emma (1).wav')

    def collide():
        if pygame.sprite.spritecollide(player, zombie_group, False):
            if player.alive:
                player.health -= 100

        for zombie in zombie_group:
            if pygame.sprite.spritecollide(zombie, bullet_group, True):
                sound_file.play()
                if zombie.alive:
                    zombie.health -= 100

    camera_offset = pygame.Vector2(0, 0)

    def camera():
        # Calculate the camera offset to center the player
        camera_offset.x = -SCREEN_WIDTH // 2 + player.rect.centerx
        camera_offset.y = -SCREEN_HEIGHT // 2 + player.rect.centery

        # Clear the screen
        screen.fill((0, 0, 0))

        # Calculate the position to draw the background with the camera offset
        bg_x = 0 - 2 * camera_offset.x
        bg_y = 0 - 2 * camera_offset.y

        # Draw the background at the calculated position
        world_surface.blit(BG, (bg_x, bg_y))
        player.draw(world_surface)

    zombie_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    player = Fighter('fighter', 400, 224, 1.5, 2)
    zombie = Fighter('enemy', 200, 200, 1.5, 1)
    zombie2 = Fighter('enemy', 600, 100, 1.5, 1)
    zombie3 = Fighter('enemy', 400, 0, 1.5, 1)
    zombie4 = Fighter('enemy', 500, 600, 1.5, 1)
    zombie5 = Fighter('enemy', 50, 200, 1.5, 1)
    zombie6 = Fighter('enemy', 0, 800, 1.5, 1)
    zombie_group.add(zombie)
    zombie_group.add(zombie2)
    zombie_group.add(zombie3)
    zombie_group.add(zombie4)
    zombie_group.add(zombie5)
    zombie_group.add(zombie6)

    def generate_zombies(num_zombies):
        for _ in range(num_zombies):
            zombie_x = random.randint(100, 1270)
            zombie_y = random.randint(100, 1190)

            # Ensure zombies don't spawn where the player is
            while abs(zombie_x - player.rect.centerx) < 200 and abs(zombie_y - player.rect.centery) < 200:
                zombie_x = random.randint(100, 1270)
                zombie_y = random.randint(100, 1190)

            zombie = Fighter('enemy', zombie_x, zombie_y, 1.5, 1)
            zombie_group.add(zombie)

    def next_level():
        global current_level
        current_level += 1
        num_zombies = min(current_level * 10, max_zombies_per_level)
        generate_zombies(num_zombies)

    run = True

    moving_right = False
    moving_left = False
    moving_up = False
    moving_down = False
    while run:
        clock.tick(FPS)

        # draw_bg()
        camera()
        # player.draw()
        player.update()

        for zombie in zombie_group:
            zombie.update()
            zombie.zombie_ai(player)
            zombie.draw(world_surface)
        collide()
        bullet_group.draw(world_surface)
        bullet_group.update()

        if player.alive:
            if moving_left or moving_right:
                player.update_action(1)
            else:
                player.update_action(0)

        player.move(moving_right, moving_left, moving_up, moving_down)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                first_screen = False
                Second_Screen = False
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shoot(pygame.mouse.get_pos()[0] + camera_offset.x,
                             pygame.mouse.get_pos()[1] + camera_offset.y, bullet_group)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False
            if len(zombie_group) == 0:
                emma_file.play()
                next_level()
        clipping_rect = player.rect.copy()
        clipping_rect.width = SCREEN_WIDTH
        clipping_rect.height = SCREEN_HEIGHT
        clipping_rect.center = player.rect.center

        screen.blit(world_surface, (0, 0), clipping_rect)
        text = game_font.render(str(current_level), True, (255, 69, 0))
        screen.blit(text,
                    (SCREEN_WIDTH -20, 0))
        pygame.display.flip()
        pygame.display.update()

