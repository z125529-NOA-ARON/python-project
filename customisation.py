import pygame
import os
from personalisation import snake_color
import personalisation
from snake_game import screen_width, screen_height
from button import Button


"""
Marie Zhu z525082
"""


def customisation_menu():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height)) #create a game window
    clock = pygame.time.Clock() #clock for controling frame rate

    title_font = pygame.font.SysFont("Comic Sans MS", 50) #font for the title

    #buttons for customizing the snake color
    buttons = [
        Button(150+80, 150, 150, 50, "Blue",   (58, 144, 255)),
        Button(150+80, 230, 150, 50, "Purple", (94, 0, 94)),
        Button(330+80, 230, 150, 50, "Green",  (0, 128, 0)),
        Button(330+80, 150, 150, 50, "Pink",   (255, 171, 187)),
    ]

    #button for returning to the previous menu
    back_button = Button(screen_width // 2 - 150 // 2, screen_height - 60, 150, 50, "Back", (191, 191, 191))

    #load and scale the background image
    base_dir = os.path.dirname(os.path.abspath(__file__))
    background = pygame.image.load(os.path.join(base_dir, "customise_background.png")).convert()
    background = pygame.transform.scale(background, (screen_width, screen_height))

    #loop of the customisation menu
    while True:
        screen.blit(background, (0, 0)) #draw background

        #display title text
        title = title_font.render("Customisation", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - 170, 10))

        #handling events
        for event in pygame.event.get():
            #if window closed, close the game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #update the snake color based on the selected button
            for b in buttons:
                if b.clicked(event):
                    personalisation.snake_color = b.color   
                    return

            if back_button.clicked(event): #return to previous menu if back button was clicked
                return

        #draw all the color buttons
        for b in buttons:
            b.draw(screen)

        #draw the back button
        back_button.draw(screen)

        pygame.display.flip() #update the display
        clock.tick(30) #limit the frame rate to 30 FPS


