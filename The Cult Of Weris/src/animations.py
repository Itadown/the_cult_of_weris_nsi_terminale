import pygame
from sound import Sound


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()

        self.name = name
        self.sprite_sheet = pygame.image.load(f"../sprites/{name}.png")
        self.menu_image = pygame.image.load("../menu/menu.png")
        self.menu__image_chiffre = pygame.image.load(
            "../menu/chiffres_before.png")  # pour les chiffres du volume des sons
        self.taillefenetre = pygame.display.Info()
        self.x_position = self.taillefenetre.current_w
        self.y_position = self.taillefenetre.current_h

        self.menu = self.get_image_355x756(0, 0)
        self.menu = pygame.transform.scale(self.menu, (self.x_position // 5.4, self.y_position // 1.4))
        self.menu.set_colorkey([75, 75, 75])
        self.menu.blit(self.menu, (0, 0), (0, 0, 355, 756))

        self.chiffre_musique = self.get_image_150x230(0, 0)
        self.chiffre_musique = pygame.transform.scale(self.chiffre_musique,
                                                      (self.x_position // 50, self.y_position // 25))
        self.chiffre_musique.set_colorkey([75, 75, 75])
        self.chiffre_musique.blit(self.chiffre_musique, (0, 0), (0, 0, 150, 230))

        self.chiffre_effet = self.get_image_150x230(0, 0)
        self.chiffre_effet = pygame.transform.scale(self.chiffre_effet, (self.x_position // 50, self.y_position // 25))
        self.chiffre_effet.set_colorkey([75, 75, 75])
        self.chiffre_effet.blit(self.chiffre_effet, (0, 0), (0, 0, 150, 230))

        self.mort_image = pygame.image.load("../map/mort.png")
        self.etrange_image = pygame.image.load("../map/etrange.png")
        self.barre_de_vie_image = pygame.image.load("../map/barre_de_vie.png")

        self.taillefenetre = pygame.display.Info()
        self.x_position = self.taillefenetre.current_w
        self.y_position = self.taillefenetre.current_h
        self.menu = self.get_image_355x756(0, 0)
        self.menu = pygame.transform.scale(self.menu, (self.x_position // 5.4, self.y_position // 1.4))
        self.menu.set_colorkey([75, 75, 75])
        self.menu.blit(self.menu, (0, 0), (0, 0, 355, 756))

        self.barre_de_vie = self.get_images_200x20(4000, 0)
        self.barre_de_vie = pygame.transform.scale(self.barre_de_vie, (self.x_position * 2, self.y_position * 2))
        self.barre_de_vie.set_colorkey([0, 0, 0])
        self.barre_de_vie.blit(self.barre_de_vie, (0, 0), (0, 0, 200, 20))

        self.mort_info = self.get_images_1920x1080_mort(0, 0)
        self.mort_info = pygame.transform.scale(self.mort_info, (self.x_position, self.y_position))
        self.mort_info.set_colorkey([0, 0, 0])
        self.mort_info.blit(self.mort_info, (0, 0), (0, 0, 1920, 1080))

        self.etrange = self.get_images_1920x1080_etrange(0, 0)
        self.etrange = pygame.transform.scale(self.etrange, (self.x_position, self.y_position))
        self.etrange.set_colorkey([0, 0, 0])
        self.etrange.blit(self.etrange, (0, 0), (0, 0, 1920, 1080))

        self.animation_index = 0
        self.clock = 0
        self.hit_clock = 0
        self.son = Sound()
        self.herbe = False
        self.first = False
        self.credit = False

        # variable qui stock tous les différents mouvements et leurs coordonnées en y sur l’image
        self.images = {
            'down': self.get_images(640, 'down'),
            'left': self.get_images(576, 'left'),
            'right': self.get_images(704, 'right'),
            'up': self.get_images(512, 'up'),

            'arret_down': self.get_images(896, 'arret_down'),
            'arret_left': self.get_images(832, 'arret_left'),
            'arret_right': self.get_images(960, 'arret_right'),
            'arret_up': self.get_images(768, 'arret_up'),

            'sword_hit_up': self.get_images(1344, 'sword_hit_up'),
            'sword_hit_down': self.get_images(1728, 'sword_hit_down'),
            'sword_hit_right': self.get_images(1920, 'sword_hit_right'),
            'sword_hit_left': self.get_images(1536, 'sword_hit_left'),

            'menu': self.get_images(0, 'menu'),
            'mort': self.get_images(0, 'mort'),
            'etrange': self.get_images(0, 'etrange'),
            'barre_de_vie': self.get_images(0, 'barre_de_vie'),

            'axe_hit_up': self.get_images(768, 'axe_hit_up'),
            'axe_hit_down': self.get_images(896, 'axe_hit_up'),
            'axe_hit_right': self.get_images(960, 'axe_hit_right'),
            'axe_hit_left': self.get_images(832, 'axe_hit_left'),

            'mort_player': self.get_images(1280, 'mort_player'),
            'menu_plus': self.get_images(0, "menu_plus"),
            'chiffres': self.get_images(0, "chiffres")
        }
        self.speed = 2

    def change_speed(self, speed):
        self.speed = speed

    def son_grass(self, var):
        if var:
            self.herbe = True
        else:
            self.herbe = False

    def son_grass_other(self, var):
        if var:
            self.herbe = True
        else:
            self.herbe = False

    def change_barre_de_vie(self, health):
        """
        Méthode pour actualiser la barre de vie en fonction des dégâts
        """
        i = health // 5
        if health <= 0:
            self.barre_de_vie = self.images['barre_de_vie'][0]
            self.barre_de_vie = pygame.transform.scale(self.barre_de_vie, (self.x_position * 2, self.y_position * 2))
            self.barre_de_vie.set_colorkey([0, 0, 0])
        self.barre_de_vie = self.images['barre_de_vie'][i]
        self.barre_de_vie = pygame.transform.scale(self.barre_de_vie, (self.x_position * 2, self.y_position * 2))
        self.barre_de_vie.set_colorkey([0, 0, 0])

    def change_animation(self, name):
        """
        Méthode pour les animations de marche ou de coup
        """
        touche = pygame.key.get_pressed()
        if self.animation_index >= len(self.images[name]) and "hit" not in name:
            self.animation_index = 0
        if self.herbe:
            self.son.grass_sound()

        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        if "hit" in name:
            if self.first:
                self.animation_index = 0
            if self.hit_clock >= 5:
                self.animation_index += 1  # passer à l’image suivante

                if self.animation_index >= len(self.images[name]):
                    self.animation_index = 0
                self.hit_clock = 0
            else:
                self.hit_clock += 1

        elif touche[pygame.K_LSHIFT] and "player" in self.name:

            if name == "up":
                self.image = pygame.transform.scale(self.image, (64, 60))
            if name == "down":
                self.image = pygame.transform.scale(self.image, (64, 60))
            if name == "left":
                self.image = pygame.transform.rotate(self.image, 5)
            if name == "right":
                self.image = pygame.transform.rotate(self.image, -5)
            self.clock += self.speed * 12
        else:
            self.speed = 2
            self.clock += self.speed * 8
        if self.clock >= 100:
            self.animation_index += 1  # passer à l’image suivante
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock = 0
        return False

    def change_animation_epee(self, name, compteur):
        """
        Méthode pour animer les coups d’épées
        """
        if compteur == 0:
            self.animation_index = 0
            self.clock = 0

        if self.animation_index >= len(self.images[name]):
            self.animation_index = 0

        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += 2 * 8

        if self.clock >= 60:
            self.animation_index += 1  # passer à l’image suivante
            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock = 0
        return False

    def credits_menu(self):
        """
        Méthode pour afficher les crédits
        """
        self.credit = True
        self.menu = self.images["menu_plus"][1]
        self.menu = pygame.transform.scale(self.menu, (self.x_position // 5.4, self.y_position // 1.4))
        self.menu.set_colorkey([75, 75, 75])

    def options_menu(self):
        """
        Méthode pour afficher les options
        """
        self.menu = self.images['menu_plus'][0]
        self.menu = pygame.transform.scale(self.menu, (self.x_position // 5.4, self.y_position // 1.4))
        self.menu.set_colorkey([75, 75, 75])

    def animation_menu(self, name, compteur):
        """
        Méthode pour animer le menu
        """
        if name == "up" and compteur == 0:
            self.animation_index = -1
        elif compteur == 0:
            self.animation_index = 0
        if self.animation_index >= len(self.images['menu']):
            return

        if name == 'down':
            self.menu = self.images['menu'][self.animation_index]
            self.menu = pygame.transform.scale(self.menu, (self.x_position // 5.4, self.y_position // 1.4))
            self.menu.set_colorkey([75, 75, 75])
            self.clock += 2 * 8

            if self.clock >= 40:

                self.animation_index += 1  # passer à l’image suivante
                if self.animation_index >= len(self.images['menu']):
                    self.animation_index = 0
                self.clock = 0
            return False

        if name == 'up':
            self.menu = self.images['menu'][self.animation_index]
            self.menu = pygame.transform.scale(self.menu, (self.x_position // 5.4, self.y_position // 1.4))
            self.menu.set_colorkey([75, 75, 75])
            self.clock += 2 * 8

            if self.clock >= 40:
                self.animation_index -= 1  # passer à l’image suivante
                if -self.animation_index >= len(self.images['menu']) + 1:
                    self.animation_index = 0
                self.clock = 0
            return False

    def image_mort(self, name, index):
        """
        Animation pour afficher le message de mort
        """
        self.animation_index = index
        if self.animation_index >= len(self.images['mort']):
            return

        if name == 'respawn':
            self.mort_info = self.images['mort'][self.animation_index]
            self.mort_info = pygame.transform.scale(self.mort_info, (self.x_position, self.y_position))
            self.mort_info.set_colorkey([0, 0, 0])

            self.animation_index -= 1  # passer à l’image suivante
            if self.animation_index >= len(self.images['mort']):
                self.animation_index = 0
            return False

        if name == 'mort':
            self.mort_info = self.images['mort'][self.animation_index]
            self.mort_info = pygame.transform.scale(self.mort_info, (self.x_position, self.y_position))
            self.mort_info.set_colorkey([0, 0, 0])

            self.animation_index += 1  # passer à l’image suivante
            if self.animation_index >= len(self.images['mort']):
                self.animation_index = 0
            if -self.animation_index >= len(self.images['mort']) + 1:
                self.animation_index = 0
            return False

    def image_respawn_etrange(self, name, index):
        """
        Méthode pour afficher une certaine image quand on prend un mauvais chemin dans la forêt
        """
        self.animation_index = index
        if self.animation_index >= len(self.images['etrange']):
            return

        if name == 'respawn':
            self.mort_info = self.images['etrange'][self.animation_index]
            self.mort_info = pygame.transform.scale(self.mort_info, (self.x_position, self.y_position))
            self.mort_info.set_colorkey([0, 0, 0])

            self.animation_index -= 1  # passer à l’image suivante
            if self.animation_index >= len(self.images['etrange']):
                self.animation_index = 0

            return False

        if name == 'etrange':
            self.mort_info = self.images['etrange'][self.animation_index]
            self.mort_info = pygame.transform.scale(self.mort_info, (self.x_position, self.y_position))
            self.mort_info.set_colorkey([0, 0, 0])

            self.animation_index += 1  # passer à l’image suivante
            if self.animation_index >= len(self.images['etrange']):
                self.animation_index = 0
            if -self.animation_index >= len(self.images['etrange']) + 1:
                self.animation_index = 0

            return False

    def animation_mort(self, compteur):
        """
        Méthode pour animer le joueur lorsqu’il meurt
        """
        if compteur == 0:
            self.animation_index = 0
            self.clock = 0

        if self.animation_index >= len(self.images['mort_player']):
            self.animation_index = 0

        self.image = self.images['mort_player'][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += 2 * 4

        if self.clock >= 60:
            self.animation_index += 1  # passer à l’image suivante
            if self.animation_index >= len(self.images['mort_player']):
                self.animation_index = 0
            self.clock = 0
        return False

    def animation_chiffres_musique(self, chiffre):
        self.chiffre_musique = self.images["chiffres"][chiffre]
        self.chiffre_musique = pygame.transform.scale(self.chiffre_musique,
                                                      (self.x_position // 50, self.y_position // 25))
        self.chiffre_musique.set_colorkey([75, 75, 75])

    def animation_chiffres_effet(self, chiffre):
        self.chiffre_effet = self.images["chiffres"][chiffre]
        self.chiffre_effet = pygame.transform.scale(self.chiffre_effet, (self.x_position // 50, self.y_position // 25))
        self.chiffre_effet.set_colorkey([75, 75, 75])

    # pour prendre une multitude d’images pour une animation

    def get_images(self, y, name):

        coord_sword_hit = [1344, 1728, 1920, 1536]  # coordonnées des animations de coup d’épées
        coord_mort = [1280]
        coord_walk = [512, 576, 640, 704]  # coordonnées des animations de marche
        coord_axedance = [768, 832, 896, 960]  # coordonnées des animations pour danser et hache
        coord_shield = [256, 320, 384, 448]

        images = []

        if y == 0 and name == "chiffres":
            for i in range(0, 11):
                x = i * 150
                image_chiffres = self.get_image_150x230(x, y)
                images.append(image_chiffres)

        if y == 0 and name == 'menu_plus':
            j = 9
            while j < 11:
                image_menu_plus = self.get_image_355x756(355 * j, 0)
                images.append(image_menu_plus)
                j += 1

        # boucle pour animer le menu
        if y == 0:
            if name == 'menu':
                for i in range(0, 9):
                    x = i * 355
                    image_menu = self.get_image_355x756(x, y)
                    images.append(image_menu)

            elif name == 'mort':
                for i in range(0, 5):
                    x = i * 1920
                    image = self.get_images_1920x1080_mort(x, y)
                    images.append(image)

            elif name == 'etrange':
                for i in range(0, 5):
                    x = i * 1920
                    image = self.get_images_1920x1080_etrange(x, y)
                    images.append(image)

            elif name == 'barre_de_vie':
                for i in range(0, 21):
                    x = i * 200
                    image = self.get_images_200x20(x, y)
                    images.append(image)

        # boucle pour animer la marche
        if y in coord_walk:
            for i in range(1, 8):
                x = i * 64
                image = self.get_image_64x64(x, y)
                images.append(image)

        # boucle pour animer l’arrêt
        if y in coord_axedance:
            for i in range(0, 7):
                if i == 6:
                    x = 4 * 64
                elif i == 7:
                    x = 3 * 64
                else:
                    x = i * 64
                image = self.get_image_64x64(x, y)
                images.append(image)

        if y in coord_sword_hit:
            for i in range(0, 5):
                x = i * 192
                image = self.get_image_192x192(x, y)
                images.append(image)

        if y in coord_mort:
            for i in range(0, 6):
                x = i * 64
                image = self.get_image_64x64(x, y)
                images.append(image)

        if y in coord_shield:
            for i in range(0, 7):
                x = i * 64
                image = self.get_image_64x64(x, y)
                images.append(image)

        return images

    # pour prendre une image fixe
    def get_image_64x64(self, x, y):
        image = pygame.Surface([64, 64])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 64, 64))
        return image

    def get_image_192x192(self, x, y):  # pour les coups d’épées
        image = pygame.Surface([192, 192])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 192, 192))
        return image

    def get_image_355x756(self, x, y):  # pour le menu
        image_menu = pygame.Surface([355, 756])
        image_menu.blit(self.menu_image, (0, 0), (x, y, 355, 756))
        return image_menu

    def get_images_1920x1080_mort(self, x, y):
        image = pygame.Surface([1920, 1080])
        image.blit(self.mort_image, (0, 0), (x, y, 1920, 1080))
        return image

    def get_images_1920x1080_etrange(self, x, y):
        image = pygame.Surface([1920, 1080])
        image.blit(self.etrange_image, (0, 0), (x, y, 1920, 1080))
        return image

    def get_images_200x20(self, x, y):
        image = pygame.Surface([1920, 1080])
        image.blit(self.barre_de_vie_image, (0, 0), (x, y, 1920, 1080))
        return image

    def get_image_150x230(self, x, y):  # pour les chiffres
        image_chiffres = pygame.Surface([150, 230])
        image_chiffres.blit(self.menu__image_chiffre, (0, 0), (x, y, 150, 230))
        return image_chiffres
