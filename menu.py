import pygame
from user_manager import UserManager
from score_manager import ScoreManager
from snake_game import SnakeGame
from snake_game import screen_height, screen_width
from customisation import customisation_menu
from button import Button


pygame.init()


button_width = 140
button_height = 50
box_width = 200
box_height = 50


class InputBox:
    """
    Class that creates the User input box on the Menu
    """
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200, 200, 200)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.font = pygame.font.SysFont("Comic Sans MS", 20)
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 16:
                    self.text += event.unicode

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius = 30)

        if self.text != "":
            txt_surface = self.font.render(self.text, True, (255, 255, 255))
        elif not self.active:
            txt_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        else:
            txt_surface = self.font.render("", True, (255, 255, 255))

        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

        # Curseur clignotant
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + txt_surface.get_width() + 3
            cursor_y = self.rect.y + 10
            pygame.draw.rect(screen, (255, 255, 255), (cursor_x, cursor_y, 2, 25))


# class Button:
#     def __init__(self, x, y, w, h, text):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.text = text
#         self.font = pygame.font.SysFont("Comic Sans MS", 32)

#     # def draw(self, screen, color=(0, 150, 0)):
#     #     pygame.draw.rect(screen, color, self.rect, border_radius =  30)
#     #     label = self.font.render(self.text, True, (255, 255, 255))
#     #     screen.blit(label, (self.rect.x , self.rect.y))

#     def draw(self, screen, color = (0,150,0)):
#         pygame.draw.rect(screen, color, self.rect, border_radius =  30)
#         label = self.font.render(self.text, True, (255, 255, 255))
#         label_rect = label.get_rect(center=self.rect.center)
#         screen.blit(label, label_rect)

#     def clicked(self, event):
#         return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)



def menu():
    width = screen_width
    height = screen_height
    # button_width = 140
    # button_height = 50
    # box_width = 200
    # box_height = 50


    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Menu")

    background = pygame.image.load("C:/Users/eunic/OneDrive - IPSA/aero4/Japon/courses/applied_computer_prog/projet/tests/snake_menu.png").convert()
    background = pygame.transform.scale(background, (width, height))

    dark_overlay = pygame.Surface((width, height))
    dark_overlay.set_alpha(120)  # 0 = transparent, 255 = noir total
    dark_overlay.fill((0, 0, 0))
    

    username_box = InputBox((width // 2) - (box_width // 2) , (height // 2 ) - 10 - box_height , box_width, box_height, "User")
    password_box = InputBox((width // 2) - (box_width // 2) , (height // 2 ) + 10 , box_width, box_height, "Password")
    
    play_button = Button(width // 5                 , height - 100, button_width, button_height, "Play", (46,139,87))
    quit_button = Button(width - (width // 5) - 140 , height - 100, button_width, button_height, "Quit",(170,0,0))

    custom_button = Button(width // 2 - (button_height + 30), height - 100, button_width + 20, button_height, "Custom",(70,130,180))

    user_manager = UserManager()

    clock = pygame.time.Clock()

    while True:
        
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            username_box.handle_event(event)
            password_box.handle_event(event)

            if play_button.clicked(event):
                username = username_box.text
                password = password_box.text

                if username and password:
                    if user_manager.authenticate(username, password):
                        score_manager = ScoreManager(user_manager)
                        SnakeGame(username, score_manager).start()
            
            if custom_button.clicked(event):
                customisation_menu()

            if quit_button.clicked(event):
                pygame.quit()
                quit()

        # Mise à jour curseur clignotant
        username_box.update()
        password_box.update()

        # Affichage
        title = pygame.font.SysFont("Comic Sans MS", 50).render("Log in", True, (255, 255, 255))
        screen.blit(title, (screen_width // 2 - 70, 30))

        username_box.draw(screen)
        password_box.draw(screen)
        play_button.draw(screen)
        quit_button.draw(screen)
        custom_button.draw(screen)


        pygame.display.flip()
        clock.tick(30)

