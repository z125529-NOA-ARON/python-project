import pygame
from user_manager import UserManager
from score_manager import ScoreManager
from snake_game import SnakeGame

pygame.init()

class InputBox:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (200, 200, 200)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.font = pygame.font.SysFont("ADLaM Display", 26)
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
        pygame.draw.rect(screen, self.color, self.rect, 2)

        txt = self.text if self.text else self.placeholder
        txt_surface = self.font.render(txt, True, (255, 255, 255))
        screen.blit(txt_surface, (self.rect.x + 10, self.rect.y + 10))

        # Curseur clignotant
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + txt_surface.get_width() + 3
            cursor_y = self.rect.y + 10
            pygame.draw.rect(screen, (255, 255, 255), (cursor_x, cursor_y, 2, 25))


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.SysFont("Arial", 32)

    def draw(self, screen, color=(0, 150, 0)):
        pygame.draw.rect(screen, color, self.rect)
        label = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(label, (self.rect.x + 20, self.rect.y + 10))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def menu():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Snake Menu")

    username_box = InputBox(200, 120, 200, 40, "Utilisateur")
    password_box = InputBox(200, 180, 200, 40, "Mot de passe")
    play_button   = Button(230, 250, 140, 50, "JOUER")
    quit_button   = Button(230, 310, 140, 50, "QUITTER")

    user_manager = UserManager()

    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))

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

            if quit_button.clicked(event):
                pygame.quit()
                quit()

        # Mise à jour curseur clignotant
        username_box.update()
        password_box.update()

        # Affichage
        title = pygame.font.SysFont("Arial", 40).render("Connexion Snake", True, (255, 255, 0))
        screen.blit(title, (180, 40))

        username_box.draw(screen)
        password_box.draw(screen)
        play_button.draw(screen)
        quit_button.draw(screen, (200, 0, 0))

        pygame.display.flip()
        clock.tick(30)
