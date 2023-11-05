

import pygame
import math

pygame.init()

SCREEN_WIDTH= 800
SCREEN_HEIGHT= 448

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie')

#framerate
clock=pygame.time.Clock()
FPS=60
GRAVITY= .75

bullet_img = pygame.image.load('assets/images/extra/bullet.png').convert_alpha()

BG = pygame.image.load("assets/images/forest2.png")
def draw_bg():
    screen.blit(BG, (0,0 ))
class Fighter(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        self.char_type = char_type
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed=speed
        self.shoot_cooldown = 0
        self.direction=1
        self.vel_y=0
        self.jump=False
        self.in_air= True
        self.flip= False
        self.animation_list=[]
        self.frame_index=0
        self.action=0
        self.health = 100
        self.max_health = self.health
        self.update_time = pygame.time.get_ticks()
        temp_list=[]
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
        for i in range(1):
            img = pygame.image.load(f'assets/images/{self.char_type}/jump/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'assets/images/{self.char_type}/death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image=self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown>0:
            self.shoot_cooldown -=1
    def move(self, moving_right, moving_left, moving_up, moving_down):
        dx=0
        dy=0

        if moving_right:
            dx= self.speed
            self.flip = False
            self.direction = 1
        if moving_left:
            dx= -self.speed
            self.flip= True
            self.direction= -1
        if moving_down:
            dy= self.speed
        if moving_up:
            dy= -self.speed

        #if self.jump == True and self.in_air==False:
            #self.vel_y = -11
            #self.jump = False
            #self.in_air=True
        #self.vel_y += GRAVITY
        #if self.vel_y > 10:
            #elf.vel_y


        #dy += self.vel_y
        #if self.rect.bottom + dy > 300:
            #dy = 300 - self.rect.bottom
            #self.in_air = False
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown== 0:
            self.shoot_cooldown = 40
            if event.type == pygame.MOUSEBUTTONDOWN:
                p_x, p_y = player.rect.center
                bx, by = pygame.mouse.get_pos()
                angle = math.atan2(by - p_y, bx - p_x)
                bvx = player.speed * math.cos(angle)
                bvy = player.speed * math.sin(angle)
                bullet = Bullet(self.rect.centerx + (.5 * self.rect.size[0] ), self.rect.centery, (bvx, bvy))
                bullet_group.add(bullet)

    def zombie_ai(self):
        #center of sprite is x and y
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
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = 7
            else:
                self.frame_index=0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time= pygame.time.get_ticks()

    def check_alive(self):
        if self.health<= 0:
            self.health=0
            self.speed=0
            self.alive=False
            self.update_action(3)
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image= bullet_img
        self.rect= self.image.get_rect()
        self.rect.center=(x,y)
        self.direction=direction





    def update(self):
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]

        # Check if the bullet is out of bounds and kill it
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()


        if pygame.sprite.spritecollide(player, zombie_group, False):
            if player.alive:
                player.health -= 50
                self.kill()
        for zombie in zombie_group:
            if pygame.sprite.spritecollide(zombie, bullet_group, False):
                if zombie.alive:
                    zombie.health-= 100
                    self.kill()



#creates a sprite group
zombie_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()


player = Fighter ('fighter',200, 200, 1.5, 3)
zombie= Fighter ('enemy',400, 200, 1.5, 1)
zombie2= Fighter ('enemy',400, 100, 1.5, 1)
zombie_group.add(zombie)
zombie_group.add(zombie2)





run = True
moving_right= False
moving_left= False
moving_up= False
moving_down= False
shoot= False
while run:

    clock.tick(FPS)

    draw_bg()

    player.draw()
    player.update()
    for zombie in zombie_group:
        zombie.draw()
        zombie.update()
        zombie.zombie_ai()
    bullet_group.update()
    bullet_group.draw(screen)


    if player.alive:
        if shoot:
            player.shoot()
        if moving_left or moving_right:
            player.update_action(1)
        #elif player.in_air:
            #player.update_action(2)
        else:
            player.update_action(0)

    player.move(moving_right, moving_left, moving_up, moving_down)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run= False
        #keyboard inputs
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            shoot = False
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_d:
                moving_right = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_w:
                moving_up=True
            if event.key == pygame.K_s:
                moving_down=True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump=False
        if event.type ==pygame.KEYUP:
            if event.key== pygame.K_d:
                moving_right=False
            if event.key == pygame.K_a:
                moving_left =False
            if event.key == pygame.K_w:
                moving_up=False
            if event.key == pygame.K_s:
                moving_down=False
            if event.key == pygame.K_SPACE:
                player.jump=False
    pygame.display.update()
pygame.quit()
