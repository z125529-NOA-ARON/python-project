import pygame

class Button:
    def __init__(self, x, y, w, h, text, bg_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Comic Sans MS", 28)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=25)

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    



class BoutonCouleur(Button):
    def __init__(self, x, y, w, h, text, color):
        super().__init__(x, y, w, h, text, color)
        self.color = color

