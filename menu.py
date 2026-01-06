import pygame
import os
from user_manager import UserManager, EmptyFieldError, InvalidCredentialsError
from score_manager import ScoreManager
from snake_game import SnakeGame, screen_height, screen_width
from customisation import customisation_menu
from button import Button


pygame.init()

# Constants for button and input box sizes
button_width = 140
button_height = 50
box_width = 200
box_height = 50


# -------------------
# InputBox class for text input
# -------------------
class InputBox:
    """
    InputBox: Timo - Z125560
    A text input box for user input in the menu.
    Handles clicking, typing, backspace and displays a blinking cursor.
    Can show a placeholder when empty.
    """
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h) # Rectangle that defines the box position and size
        self.color = (200, 200, 200) # Border color of the box
        self.text = "" # Text currently typed in the box
        self.placeholder = placeholder # Placeholder text when empty
        self.active = False # Whether the box is currently active (clicked)
        self.font = pygame.font.SysFont("Comic Sans MS", 20) # Font used for the text
        # Cursor visibility and timer for blinking
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        """
        Handle events related to the input box:
        - Mouse click to activate the box
        - Keyboard input to type or delete text
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activate box if clicked
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                # Remove last character on backspace
                self.text = self.text[:-1]
            elif len(self.text) < 16:
                # Add new character if under limit
                self.text += event.unicode

    def update(self):
        """
        Update the blinking cursor.
        Toggles visibility every 30 frames.
        """
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

    def draw(self, screen):
        """
        Draw the input box, text, placeholder, and blinking cursor on the screen
        """
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius = 30) # Draw the rectangle border

        # Determine which text to show
        if self.text != "":
            # Show typed text
            txt_surface = self.font.render(self.text, True, (255, 255, 255))
        elif not self.active:
            # Show placeholder if not active and empty
            txt_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        else:
            # Show empty if active but no text
            txt_surface = self.font.render("", True, (255, 255, 255))

        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10)) # Draw the text

        # Draw blinking cursor if active
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + txt_surface.get_width() + 3
            cursor_y = self.rect.y + 10
            pygame.draw.rect(screen, (255, 255, 255), (cursor_x, cursor_y, 2, 25))


def menu():
    """
    Main menu of the Snake Game:
    - Displays background and overlay
    - Handles user login via InputBox
    - Provides Play, Quit and Customization buttons
    - Launches game when Play is clicked and credentials are valid
    """
    width = screen_width
    height = screen_height
    # button_width = 140
    # button_height = 50
    # box_width = 200
    # box_height = 50


    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Menu")

    # Load background image using relative path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    background_path = os.path.join(base_dir, "snake_menu.png")
    background = pygame.image.load(background_path).convert()
    background = pygame.transform.scale(background, (width, height))

    # Dark overlay to improve readability of text and buttons
    dark_overlay = pygame.Surface((width, height))
    dark_overlay.set_alpha(120)  # Transparency level (0=transparent, 255=opaque)
    dark_overlay.fill((0, 0, 0))
    
    # Create input boxes for username and password
    username_box = InputBox((width // 2) - (box_width // 2) , (height // 2 ) - 10 - box_height , box_width, box_height, "User")
    password_box = InputBox((width // 2) - (box_width // 2) , (height // 2 ) + 10 , box_width, box_height, "Password")

    # Create buttons
    play_button = Button(width // 5 , height - 100, button_width, button_height, "Play", (46,139,87))
    quit_button = Button(width - (width // 5) - 140 , height - 100, button_width, button_height, "Quit",(170,0,0))
    custom_button = Button(width // 2 - (button_height + 30), height - 100, button_width + 20, button_height, "Custom",(70,130,180))

    # User manager to handle authentification
    user_manager = UserManager()
    clock = pygame.time.Clock()
    font_title = pygame.font.SysFont("Comix Sans MS", 50)

    running = True
    while running:
        # Draw background and overlay
        screen.blit(background, (0, 0))
        screen.blit(dark_overlay, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Let input boxes handle typing/clicks
            username_box.handle_event(event)
            password_box.handle_event(event)

            # ----- Play Button -----
            if play_button.clicked(event):
                username = username_box.text.strip()
                password = password_box.text.strip()

                if username and password:
                    try:
                        authentificated = user_manager.authenticate(username, password)
                        if authentificated:
                            #Launch the game if authentification succeeded
                            score_manager = ScoreManager(user_manager)
                            SnakeGame(username, score_manager).start()
                    except EmptyFieldError as e:
                        print(f"[WARNING] {e}")
                    except InvalidCredentialsError as e:
                        print(f"[ERROR] {e}")            

            # ----- Customisation Button -----
            if custom_button.clicked(event):
                customisation_menu()

            # ----- Quit Button -----
            if quit_button.clicked(event):
                pygame.quit()
                quit()

        # Update cursor blinking for input boxes
        username_box.update()
        password_box.update()

        # Draw the title and input boxes
        screen.blit(font_title.render("Log in", True, (255, 255, 255)), (screen_width // 2 - 70, 30))
        username_box.draw(screen)
        password_box.draw(screen)

        # Draw buttons
        play_button.draw(screen)
        quit_button.draw(screen)
        custom_button.draw(screen)

        # Refresh the display
        pygame.display.flip()
        clock.tick(30)
