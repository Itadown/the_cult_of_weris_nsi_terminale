import pygame


class DialogBox:

    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position

        self.box = pygame.image.load("../dialogs/dialogbox.png")
        self.box = pygame.transform.scale(self.box, (self.x_position * 2, self.y_position * 2))  # Permet de modifier
        # la taille
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("../dialogs/Pixellari.ttf", self.x_position // 60)
        self.reading = False
        self.name = None

    def execute(self, name, dialog=None):
        """
        La méthode execute permet de passer les différents textes des pnjs
        """
        self.name = name
        if dialog is None:
            dialog = []
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render(self, screen):
        """
        La méthode render permet d’afficher le texte et le nom des pnjs sur l’écran de l’utilisateur
        """
        if not self.texts:
            self.reading = False
        elif self.reading:
            
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.x_position / 10, self.y_position / 1.33))
            name = self.font.render(self.name, False, (240, 240, 240))
            screen.blit(name,
                        (self.x_position / 5.4 + self.x_position // 30, self.y_position / 1.4 + self.y_position // 20))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))
            screen.blit(text,
                        (self.x_position / 10 + self.x_position // 30, self.y_position / 1.3 + self.y_position // 23))

    def next_text(self):
        """
        La méthode next_text permet de faire apparaitre les lettres petit à petit
        """
        self.text_index += 1
        self.letter_index = 0

        if self.text_index >= len(self.texts):
            self.reading = False
