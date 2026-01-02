import pygame
import random

class SnakeGame:
    def __init__(self, username, score_manager):
        self.username = username                         # store the player's username
        self.score_manager = score_manager               # store the score manager object

        # Window + block size
        self.width = 600
        self.height = 400
        self.block = 20

        # download images --> change the path
        self.grass = pygame.image.load("C:/Users/eunic/OneDrive - IPSA/aero4/Japon/courses/applied_computer_prog/projet/tests/grass.png")
        self.grass = pygame.transform.scale(self.grass, (self.width, self.height))

        self.apple_img = pygame.image.load("C:/Users/eunic/OneDrive - IPSA/aero4/Japon/courses/applied_computer_prog/projet/tests/appel.png")
        self.apple_img = pygame.transform.scale(self.apple_img, (20, 20))

        # Reset
        self.reset_game()

    # fonction of the reset
    def reset_game(self):
        self.snake = [(self.width/2, self.height/2)]          # initialise the snake at the position (100,100); the size is 1 segment 
        self.direction = (self.block, 0)                      # initialise the direction of the snake to the right
        self.score = 0                                        # reset the score to 0
        self.food = self.spawn_food()                         # generate the first food position
        self.is_running = True                                # the game running varable is True

    # function to make food appear
    def spawn_food(self):
        return (random.randint(0, (self.width - self.block) // self.block) * self.block, random.randint(0, (self.height - self.block) // self.block) * self.block) # random position (x, y)

    # 
    def move_snake(self):
        x, y = self.snake[0]               # get the position of the snake
        dx, dy = self.direction            # get the movement direction
        new_head = (x + dx, y + dy)        # calculate the position of the new head
        self.snake.insert(0, new_head)     # add the new head at the beginning of the snake list 

        # check if the snake ate an appel
        if new_head == self.food:      
            self.score += 1                # increase the score of 1
            self.food = self.spawn_food()  # respawn an apple 
        else:
            self.snake.pop()               # remove the last segment of the snake to have the good number of segment


    # Check if the snake touch itself or the wall
    def check_collisions(self):
        x, y = self.snake[0]               # get the position of the head of the snake

        # if the snake touch the wall 
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True

        # if the snake touch itself
        if self.snake[0] in self.snake[1:]:
            return True

        return False                        # no collision

    # fonction to initialise the start
    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))    # create the game window
        clock = pygame.time.Clock()                                    # creation of the clock to control the FPS

        from game_over import game_over_screen                         # import game over screen fonction
        from menu import menu                                          # import menu fonction

        font = pygame.font.SysFont("Arial", 24)                        # creation of the font for the score display

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                elif event.type == pygame.KEYDOWN:
                    # press "z" to go up
                    if event.key == pygame.K_z:
                        self.direction = (0, -self.block)

                    # press "s" to go down
                    elif event.key == pygame.K_s:
                        self.direction = (0, self.block)

                    # press "q" to go left
                    elif event.key == pygame.K_q:
                        self.direction = (-self.block, 0)

                    # press "d" to go right
                    elif event.key == pygame.K_d:
                        self.direction = (self.block, 0)

                    # press escape to go up
                    elif event.key == pygame.K_ESCAPE:
                        # Retour menu principal
                        return                           #return to the main menu

            self.move_snake()                            # move the snake

            if self.check_collisions():                                     # chek the collision
                self.score_manager.update_score(self.username, self.score)  # save the score
                top4 = self.score_manager.get_top_4()                       # have the top 4
                game_over_screen(screen, self.score, top4)                  # display the game over screen
                return

            # Display
            screen.blit(self.grass, (0, 0))                                 # display the background 

            # diplay the snake segments
            for block in self.snake:
                pygame.draw.rect(screen, (0, 128, 0), (*block, self.block, self.block))

            # diplay the apple
            screen.blit(self.apple_img, self.food)

            # Diplay the score
            score_text = font.render(f"Score : {self.score}", True, (255, 255, 255))
            screen.blit(score_text, (self.width - 100, 10))

            pygame.display.flip()                                           #update the display
            clock.tick(10)                                                  # 10 FPS 
