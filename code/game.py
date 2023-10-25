import pygame

pygame.init()

SCREEN_WIDTH= 800
SCREEN_HEIGHT= 448

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie')

#framerate
clock=pygame.time.Clock()
FPS=60

BG = pygame.image.load("forest2.png")
def draw_bg():
    screen.blit(BG, (0,0 ))
class Fighter(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        self.char_type = char_type
        pygame.sprite.Sprite.__init__(self)
        self.speed=speed
        self.direction=1
        self.flip= False
        img = pygame.image.load(f'{self.char_type}.png')
        self.image = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
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


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)



player = Fighter ('fighter',200, 200, 1.5, 3)
zombie= Fighter ('zombie',400, 200, .06, 3)





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
                moving_up=True
            if event.key == pygame.K_DOWN:
                moving_down=True
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
