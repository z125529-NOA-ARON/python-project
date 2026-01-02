import pygame
from personalisation import snake_color
import personalisation
from snake_game import screen_width, screen_height
from button import Button, BoutonCouleur






def customisation_menu():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("Comic Sans MS", 50)

    buttons = [
        BoutonCouleur(230, 150, 150, 50, "Blue",   (58, 144, 255)),
        BoutonCouleur(230, 230, 150, 50, "Purple", (94, 0, 94)),
        BoutonCouleur(410, 150, 150, 50, "Pink",   (255, 171, 187)),
        BoutonCouleur(410, 230, 150, 50, "Green",  (0, 128, 0)),
    ]


    back_button = Button(screen_width // 2 - 150 // 2, screen_height - 60, 150, 50, "Retour", (191, 191, 191))

    background = pygame.image.load("C:/Users/eunic/OneDrive - IPSA/aero4/Japon/courses/applied_computer_prog/projet/tests/customise_background.png").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    while True:
        screen.blit(background, (0, 0))

        title = title_font.render("Customisation", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - 170, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            for b in buttons:
                if b.clicked(event):
                    personalisation.snake_color = b.color
                    return


            if back_button.clicked(event):
                return

        for b in buttons:
            b.draw(screen)

        back_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)
