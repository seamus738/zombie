import pygame
import math
from bullet import Bullet
from settings import *

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
        if self.rect.left < 255:
            self.rect.left = 255
        if self.rect.right > WORLD_WIDTH - 250:
            self.rect.right = WORLD_WIDTH - 250

    def shoot(self, bx, by, bullet_group):
        if self.shoot_cooldown== 0:
            self.shoot_cooldown = 20
            p_x, p_y = self.rect.center
            angle = math.atan2(by - p_y, bx - p_x)
            bvx = self.speed * math.cos(angle)
            bvy = self.speed * math.sin(angle)
            bullet = Bullet(self.rect.centerx + (self.direction * .5 * self.rect.size[0]),
                            self.rect.centery,(bvx, bvy))
            bullet_group.add(bullet)
        print(bx,by)


    def zombie_ai(self, player):
        # center of sprite is x and y
        xx = self.rect.centerx
        yy = self.rect.centery
        xxx = player.rect.centerx
        yyy = player.rect.centery

        # Calculate the direction vector
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
                self.frame_index = 7
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
