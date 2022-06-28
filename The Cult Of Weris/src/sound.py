import pygame


class Sound:

    def __init__(self):
        self.volume = 0
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)

        self.grass_cooldown = 0
        self.grass = pygame.mixer.Sound("../sound/sfx_step_grass_l.mp3")
        self.grass_volume = 0.1  # volume par défaut des effets

        self.fond = pygame.mixer.Sound("../sound/NieRHis Dream extended.mp3")
        self.fond_volume = 0.1  # volume par défaut

        self.coupepeecooldown = 0
        self.coupepee = pygame.mixer.Sound("../sound/coupepee.mp3")
        self.coupepee_volume = 0.1

    def ambiance_musique(self):
        """
        Méthode pour jouer la musique de fond
        """
        self.fond.play(-1)
        self.fond.set_volume(self.fond_volume)
        return

    def epee_sound(self):
        """
        Méthode pour jouer le son de l'épée
        """
        if self.coupepeecooldown < 20:
            self.coupepeecooldown += 1
        if self.coupepeecooldown >= 20:
            self.coupepee.play()
            self.coupepee.set_volume(self.coupepee_volume)
            self.coupepeecooldown = 0

    def grass_sound(self):
        """
        Méthode pour jouer le son de l’herbe
        """
        if self.grass_cooldown < 20:
            self.grass_cooldown += 1
        if self.grass_cooldown >= 20:
            self.grass.play()
            self.grass.set_volume(self.grass_volume)
            self.grass_cooldown = 0

    def volume(self, chiffre, updown, name, general):

        if name == "generale":
            if general is False:
                self.grass.set_volume(0)
                self.fond.set_volume(0)
            else:
                self.grass.set_volume(0.1)
                self.fond.set_volume(0.1)

        if updown == 'down':
            chiffre -= 1
        elif updown == 'up':
            chiffre += 1

        self.volume = chiffre / 10  # pour mettre l’indice chiffre au même niveau que le volume pygame

        if name == "effet":
            self.grass_volume = self.volume
            # le faire pour le coup d’épée

        if name == "musique":
            self.fond_volume = self.volume
