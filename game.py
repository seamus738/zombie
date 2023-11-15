import pygame
import math
from settings import *
from fighter import *

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie')

clock = pygame.time.Clock()
FPS = 60


BG = pygame.image.load("assets/images/background.png").convert()
WORLD_WIDTH = BG.get_width()
WORLD_HEIGHT = BG.get_height()

world_surface = BG.copy()

def draw_bg():
    world_surface.blit(BG, (0, 0))


def collide():
    if pygame.sprite.spritecollide(player, zombie_group, False):
        if player.alive:
            player.health -= 100

    for zombie in zombie_group:
        if pygame.sprite.spritecollide(zombie, bullet_group, True):
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






#creates a sprite group
zombie_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()

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

run = True
moving_right = False
moving_left = False
moving_up = False
moving_down = False
while run :

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
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.shoot(pygame.mouse.get_pos()[0]+camera_offset.x,
                         pygame.mouse.get_pos()[1]+ camera_offset.y, bullet_group)
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

    clipping_rect = player.rect.copy()
    clipping_rect.width = SCREEN_WIDTH
    clipping_rect.height = SCREEN_HEIGHT
    clipping_rect.center = player.rect.center

    screen.blit(world_surface, (0, 0), clipping_rect)
    pygame.display.update()



pygame.quit()


