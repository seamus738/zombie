
from fighter import *
import sys

pygame.init()



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Zombie')
game_font=pygame.font.Font('assets/fonts/Black_Crayon.ttf', 128)
second_game_font=pygame.font.Font('assets/fonts/Black_Crayon.ttf', 40)
instructions_game_font=pygame.font.Font('assets/fonts/Black_Crayon.ttf', 30)




Menu_Screen = True
end_screen=True
while Menu_Screen:
    screen.fill((52, 78, 91))
    text = game_font.render("Zombies!", True, (255, 69, 0))
    subtext = second_game_font.render("Press space to continue", True, (0, 0, 0))
    instructions=instructions_game_font.render('Use W A S D to move and mouse button click to shoot', True, (0,0,0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(subtext, (SCREEN_WIDTH // 2 - .9*text.get_width() // 2, SCREEN_HEIGHT // 2 + 1.3 * text.get_height() // 2))
    screen.blit(instructions,(SCREEN_WIDTH // 2 - 1.3 * text.get_width() // 2, SCREEN_HEIGHT // 2 + 2 * text.get_height() // 2))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Menu_Screen = False

        if event.type == pygame.QUIT:
            Menu_screen = False
            sys.exit()

game_screen()


pygame.quit()



