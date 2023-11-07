
import pygame
import sys
import math


pygame.init()

SCREEN_WIDTH = 885
SCREEN_HEIGHT = 400
clock= pygame.time.Clock()
FPS=60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("green grass")

green=pygame.image.load("assets/images/forest2.png").convert()
green_width=green.get_width()
green_rect=green.get_rect()

scroll=0
tiles=math.ceil(SCREEN_WIDTH / green_width ) + 1

while True:
    clock.tick(FPS)
    for i in range(0, tiles):
        screen.blit(green, (i*green_width + scroll,0))
        green_rect.x=i *green_width+scroll
        pygame.draw.rect(screen, (255,0,0), green_rect, 1)
    scroll-=5
    if abs(scroll) > green_width:
        scroll=0


    #could use: if event.type==pygame.QUIT: or -->
    for event in pygame.event.get():
        if event.type==256:
            pygame.quit()
            sys.exit()
        print(event.type)
    pygame.display.update()
