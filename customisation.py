import pygame
import os
from personalisation import snake_color
import personalisation
from snake_game import screen_width, screen_height
# from menu import menu


class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont("Comic Sans MS", 28)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=25)

        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)

        screen.blit(label, label_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def customisation_menu():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("Comic Sans MS", 50)

    buttons = [
        Button(150+80, 150, 150, 50, "Blue",   (58, 144, 255)),
        Button(150+80, 230, 150, 50, "Purple", (94, 0, 94)),
        Button(330+80, 230, 150, 50, "Green",  (0, 128, 0)),
        Button(330+80, 150, 150, 50, "Pink",   (255, 171, 187)),
    ]

    back_button = Button(screen_width // 2 - 150 // 2, screen_height - 60, 150, 50, "Back", (191, 191, 191))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    background = pygame.image.load(os.path.join(base_dir, "customise_background.png")).convert()
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

