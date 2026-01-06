import pygame

class Button:

    """
    Button: Eunice - z125470
    A clickable graphical button for the user interface
    Displays text centered inside a colored rectangle and detects i the mouse clicks
    """

    def __init__(self, x, y, w, h, text, bg_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h) # Create a rectangle
        self.text = text # text displayed on the button
        self.bg_color = bg_color # color of the button
        self.text_color = text_color # color of the text
        self.font = pygame.font.SysFont("Comic Sans MS", 28) # font of the text

    # Function to draw the button
    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=25) # draw the button rectangle with rounded corners

        label = self.font.render(self.text, True, self.text_color) # render the text into a Surface
        label_rect = label.get_rect(center=self.rect.center) # get a rectangle for the text and center it inside the button
        screen.blit(label, label_rect) # display the text on the screen

    # function that return true if the event is the mouse press the button 
    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    
# class BoutonCouleur(Button):
#     def __init__(self, x, y, w, h, text, color):
#         super().__init__(x, y, w, h, text, color)
#         self.color = color
