"""
Marie Zhu z525082
"""

import pygame
import os
from snake_game import screen_height, screen_width

podium_positions = {
    1: {"x": screen_width // 2 - 65   , "y_name": 145, "y_score": 145 + 80},
    2: {"x": screen_width // 2 - 215  , "y_name": 190, "y_score": 190 + 80},
    3: {"x": screen_width // 2 + 75   , "y_name": 228, "y_score": 230 + 80},
    4: {"x": screen_width // 2 + 220  , "y_name": 270, "y_score": 270 + 80},
}

#First, the function displays a timed “GAME OVER” message on the screen. 
#Then, it shows the player’s score and a podium with the four players who have the best scores. 
#Finally, it waits for user input to go back to the main screen.

def game_over_screen(screen, score, top4):
    pygame.font.init() #font module for rendering text
    clock = pygame.time.Clock() #clock used for the frame rate

    big_font = pygame.font.SysFont("Comic Sans MS", 100, bold=True) #font for game over
    font = pygame.font.SysFont("Comic Sans MS", 20) #font for names and small text
    font_score = pygame.font.SysFont("Comic Sans MS", 30) #font for score title

    start_time = pygame.time.get_ticks()  #start of the game over screen
    show_score = False #flag for knowning when the score and podium should be shown

    #loop until the player chooses to start over
    waiting = True
    while waiting:
        elapsed = pygame.time.get_ticks() - start_time #time since the game over display

        #handling multiple events
        for event in pygame.event.get():
            
            # when window closed, quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # keyboad input accepted only after the score is shown
            if show_score and event.type == pygame.KEYDOWN:
                #SPACE: restart the game
                if event.key == pygame.K_SPACE:
                    waiting = False
                #ESC: quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # -------- PHASE 1 : YOU LOSE (10 secondes) --------
        if elapsed < 2000:
            #load and display background image
            base_dir = os.path.dirname(os.path.abspath(__file__))
            background = pygame.image.load(os.path.join(base_dir, "snake_game_over.png")).convert()
            background = pygame.transform.scale(background, (screen_width, screen_height))
            screen.blit(background, (0, 0))
            
            #display 'GAME OVER' text
            lose_text = big_font.render("GAME OVER", True, (170, 0, 0))
            rect = lose_text.get_rect(center = (screen_width // 2, screen_height // 3))
            screen.blit(lose_text, rect)

        # -------- PHASE 2 : SCORE + TOP 4 --------
        else:
            #enable keyboard input
            show_score = True
            
            #load and display the podium image
            background = pygame.image.load(os.path.join(base_dir, "podium.png")).convert()
            background = pygame.transform.scale(background, (screen_width, screen_height))
            screen.blit(background, (0, 0))

            #display the player's score
            title = font_score.render(f"Your score : {score}", True, (255, 255 , 255))
            screen.blit(title, (screen_width // 2 - 100, 10))

            #display the top 4 players
            for rank, (username, data) in enumerate(top4, start=1):
                if rank > 4:
                    break

                #get the screen position for the current rank
                pos = podium_positions[rank]

                #display the player's username
                name_text = font.render(username, True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(pos["x"], pos["y_name"]))
                screen.blit(name_text, name_rect)

                #display the player's score under its name 
                score_text = font.render(str(data["best_score"]), True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(pos["x"], pos["y_score"]))
                screen.blit(score_text, score_rect)

            #display the instructions to start over
            restart = font.render("SPACE to play again - ESC to quit", True, (255, 255, 255))
            screen.blit(restart, (screen_width // 2 - 175, screen_height - 30))

        pygame.display.flip() #update the display with everything drawn this frame
        clock.tick(30) #limit the loop to 30 ticks

