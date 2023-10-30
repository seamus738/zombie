import pygame

pygame.init()

SCREEN_WIDTH= 800
SCREEN_HEIGHT= 448

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie')

#framerate
clock=pygame.time.Clock()
FPS=60

BG = pygame.image.load("assets/images/forest2.png")
def draw_bg():
    screen.blit(BG, (0,0 ))
class Fighter(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        self.char_type = char_type
        pygame.sprite.Sprite.__init__(self)
        self.speed=speed
        self.direction=1
        self.flip= False
        self.animation_list=[]
        self.frame_index=0
        self.action=0
        self.update_time = pygame.time.get_ticks()
        temp_list=[]
        for i in range(5):
            img = pygame.image.load(f'assets/images/{self.char_type}/idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'assets/images/{self.char_type}/run/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image=self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

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

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index=0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time= pygame.time.get_ticks()
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Fighter ('fighter',200, 200, 1.5, 3)
zombie= Fighter ('enemy',400, 200, 1.5, 3)





run = True
moving_right= False
moving_left= False
moving_up= False
moving_down= False
while run:

    clock.tick(FPS)

    draw_bg()

    player.draw()
    zombie.draw()
    player.update_animation()

    if moving_left or moving_right:
        player.update_action(1)
    else:
        player.update_action(0)

    player.move(moving_right, moving_left, moving_up, moving_down)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run= False
        #keyboard inputs
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_UP:
                moving_up=False
            if event.key == pygame.K_DOWN:
                moving_down=False
        if event.type ==pygame.KEYUP:
            if event.key== pygame.K_RIGHT:
                moving_right=False
            if event.key == pygame.K_LEFT:
                moving_left =False
            if event.key == pygame.K_UP:
                moving_up=False
            if event.key == pygame.K_DOWN:
                moving_down=False
    pygame.display.update()
pygame.quit()
