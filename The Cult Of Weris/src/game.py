import os
import pygame

from dialog import DialogBox
from map import MapManager
from player import Player
from save import Sauvegarde
from sound import Sound


class Game:
    def __init__(self):
        # créer la fenêtre du jeu
        self.running = True

        self.event = None
        self.rect = None
        self.mouse = None
        self.taillefenetre = pygame.display.Info()
        self.sprite_sheet_player = pygame.image.load("../sprites/player.png")

        x = self.taillefenetre.current_w // 10
        y = self.taillefenetre.current_h // 10
        os.environ['SDL_VIDEO_WINDOW_POS'] = " %d, %d " % (x, y)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.fullscreen = True
        pygame.display.set_caption("The cult of Weris")

        # générer un joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.depart = 0

        self.dialog_box = DialogBox(self.taillefenetre.current_w, self.taillefenetre.current_h)
        self.sauvegarde = Sauvegarde()
        self.son = Sound()

        self.volume_general = 2
        self.volume_musique = 3
        self.volume_effet = 1

        # savoir le cote et le temps d’arrêt
        self.cote = self.sauvegarde.restoration_cote()
        self.temps = 0
        self.epee = False

        # pour bloquer les animations
        self.mouvement_en_cours = None
        self.compteur = 0
        self.compteur_mort = 0
        self.index = 0

        self.change_vie = self.player.health
        self.cooldown_regen = 0
        self.restor_image = self.sauvegarde.restoration_image()

        # menu échap
        self.menu_on = False
        self.menu_en_cours = None

        self.x_position = self.taillefenetre.current_w
        self.y_position = self.taillefenetre.current_h

        self.menu_options_on = False
        self.menu_options = pygame.image.load("../menu/menu_options.png")
        self.menu_credits = pygame.image.load("../menu/credits.png")
        self.menu_options.set_colorkey([75, 75, 75])

        self.menu_click_close = pygame.Rect((self.taillefenetre.current_w // 6.04, 0),
                                            (self.taillefenetre.current_w // 40, self.taillefenetre.current_h // 21))
        self.menu_click_open = pygame.Rect((self.taillefenetre.current_w // 6.04, self.taillefenetre.current_h // 1.52),
                                           (self.taillefenetre.current_w // 40, self.taillefenetre.current_h // 20))

        self.passage_mino = False
        self.passage_boss1 = False
        self.passage_boss2 = False
        self.passage_boss3 = False
        self.detect1 = False
        self.detect2 = False

        self.bouton_options_rect = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 81),
                                                (self.taillefenetre.current_h // (self.taillefenetre.current_h / 173))),
                                               (187, 93))

        self.bouton_credits_rect = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 81),
                                                (self.taillefenetre.current_h // (self.taillefenetre.current_h / 338))),
                                               (187, 93))

        self.bouton_quitter_rect = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 83),
                                                (self.taillefenetre.current_h // (self.taillefenetre.current_h / 501))),
                                               (187, 93))

        """
        self.unmute_generale = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 231),
                                            (self.taillefenetre.current_h // (self.taillefenetre.current_h / 121))),
                                           (21, 14))
        self.mute_generale = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 231),
                                          (self.taillefenetre.current_h // (self.taillefenetre.current_h / 138))),
                                         (21, 14))

        self.fleche_up_musique = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 210),
                                              (self.taillefenetre.current_h // (self.taillefenetre.current_h / 152))),
                                             (21, 14))
        self.fleche_down_musique = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 210),
                                                (self.taillefenetre.current_h // (self.taillefenetre.current_h / 169))),
                                               (21, 14))

        self.fleche_up_effet = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 205),
                                            (self.taillefenetre.current_h // (self.taillefenetre.current_h / 187))),
                                           (21, 14))
        self.fleche_down_effet = pygame.Rect((self.taillefenetre.current_w // (self.taillefenetre.current_w / 205),
                                              (self.taillefenetre.current_h // (self.taillefenetre.current_h / 204))),
                                             (21, 14))
        """

    def handle_input(self):
        """
        La méthode handle_input permet de récupérer les touches sur lesquelles appuie l’utilisateur
        """
        pressed = pygame.key.get_pressed()

        souris = pygame.mouse.get_pressed()

        if self.map_manager.current_map != "weris_debut":
            self.player.start = True
        if self.depart < 600:
            self.depart += 1

        if not self.menu_on:
            if pressed[pygame.K_LALT]:
                self.mouse = True
                pygame.mouse.set_visible(True)  # rendre le pointeur de la souris visible avec alt

            else:
                self.mouse = False
                pygame.mouse.set_visible(False)  # rendre le pointeur de la souris invisible
        """
        if self.menu_on is True and souris[0] == 1 and self.bouton_options_rect.collidepoint(self.event.pos):
            self.player.options_menu()
            self.menu_options_on = True
            self.player.animation_chiffres_musique(self.volume_musique)
            self.player.animation_chiffres_effet(self.volume_effet)
        """

        if self.menu_on is True and souris[0] == 1 and self.bouton_credits_rect.collidepoint(self.event.pos):
            self.player.credits_menu()

        if self.menu_on is True and souris[0] == 1 and self.bouton_quitter_rect.collidepoint(self.event.pos) \
                and not self.player.credit:
            self.running = False

        """
        if self.menu_options_on is True and souris[0] == 1 and self.fleche_up_musique.collidepoint(self.event.pos):
            if self.volume_musique >= 10:
                self.volume_musique = 10
            else:
                self.son.volume(self.volume_musique, "up", "musique", True)
                self.volume_musique += 1
                self.player.animation_chiffres_musique(self.volume_musique)

        if self.menu_options_on is True and souris[0] == 1 and self.fleche_down_musique.collidepoint(self.event.pos):
            if self.volume_musique <= 0:
                self.volume_musique = 0
            else:
                self.son.volume(self.volume_musique, "down", "musique", True)
                self.volume_musique -= 1
                self.player.animation_chiffres_musique(self.volume_musique)

        if self.menu_options_on is True and souris[0] == 1 and self.fleche_up_effet.collidepoint(self.event.pos):
            if self.volume_effet >= 10:
                self.volume_effet = 10
            else:
                self.son.volume(self.volume_effet, "up", "effet", True)
                self.volume_effet += 1
                self.player.animation_chiffres_effet(self.volume_effet)
        if self.menu_options_on is True and souris[0] == 1 and self.fleche_down_effet.collidepoint(self.event.pos):
            if self.volume_effet <= 0:
                self.volume_effet = 0
            else:
                self.son.volume(self.volume_effet, "down", "effet", True)
                self.volume_effet -= 1
                self.player.animation_chiffres_effet(self.volume_effet)

        if self.menu_options_on is True and souris[0] == 1 and self.mute_generale.collidepoint(self.event.pos):
            self.son.volume(0, None, "generale", False)
            self.volume_general = False
        if self.menu_options_on is True and souris[0] == 1 and self.unmute_generale.collidepoint(self.event.pos):
            self.son.volume(0, None, "generale", True)
            self.volume_general = True
        """
        # Pour restaurer les images

        if self.restor_image != self.player.name:
            if self.depart < 100:
                self.player.name = self.restor_image
                self.player.sprite_sheet = self.sprite_sheet_player
            else:
                self.restor_image = self.player.name
                self.player.sprite_sheet = self.sprite_sheet_player
                self.sauvegarde.sauvegarde_image(self.player.name)

            self.player.images['down'] = self.player.get_images(640, 'down')
            self.player.images['left'] = self.player.get_images(576, 'left')
            self.player.images['right'] = self.player.get_images(704, 'right')
            self.player.images['up'] = self.player.get_images(512, 'up')

            self.player.images['arret_down'] = self.player.get_images(896, 'arret_down')
            self.player.images['arret_left'] = self.player.get_images(832, 'arret_left')
            self.player.images['arret_right'] = self.player.get_images(960, 'arret_right')
            self.player.images['arret_up'] = self.player.get_images(768, 'arret_up')

            self.player.images['sword_hit_up'] = self.player.get_images(1344, 'sword_hit_up')
            self.player.images['sword_hit_down'] = self.player.get_images(1728, 'sword_hit_down')
            self.player.images['sword_hit_right'] = self.player.get_images(1920, 'sword_hit_right')
            self.player.images['sword_hit_left'] = self.player.get_images(1536, 'sword_hit_left')

            self.player.images['mort_player'] = self.player.get_images(1280, 'mort_player')

            self.mouvement_en_cours = "chargement"
            self.temps = 0

        if self.mouvement_en_cours == "chargement":
            self.temps += 1
            if self.temps >= 90:
                self.mouvement_en_cours = None

        if self.player.health < self.change_vie:
            self.temps = 0
            self.cooldown_regen = 300
        else:
            if self.cooldown_regen == 0 and self.player.health != 100:
                if self.player.health + 5 > 100:
                    self.player.health = 100
                    self.player.change_barre_de_vie(self.player.health)
                else:
                    self.player.health += 5
                    self.player.change_barre_de_vie(self.player.health)
                    self.cooldown_regen += 60
            if self.cooldown_regen != 0:
                self.cooldown_regen -= 1

        self.change_vie = self.player.health

        if self.player.mort >= 1:
            if self.player.mort == 3 and self.compteur_mort >= 12000:
                self.player.mort = 4
                self.compteur_mort = 0
                self.map_manager.teleport_player("respawn")
            if self.player.mort == 4 and self.compteur_mort >= 240:
                self.compteur_mort = 0
                if not self.player.respawn_etrange:
                    self.player.image_mort("respawn", self.index)
                else:
                    self.player.image_respawn_etrange("respawn", self.index)
                    self.player.respawn_etrange = False
                self.index -= 1
                if self.index < -5:
                    self.index = 0
                    self.player.mort = 0
                    self.player.health = 100
                    self.player.change_barre_de_vie(self.player.health)

            if self.player.mort == 2 and self.compteur_mort >= 240:
                self.compteur_mort = 0
                if not self.player.respawn_etrange:
                    self.player.image_mort("mort", self.index)
                else:
                    self.player.image_respawn_etrange("etrange", self.index)
                self.index += 1
                if self.index > 5:
                    self.index = -1
                    self.player.mort = 3
            self.compteur_mort += 60
            return

        if pressed[pygame.K_ESCAPE] or (
                pressed[pygame.K_LALT] and souris[0] == 1 and self.menu_click_close.collidepoint(
            self.event.pos) and self.menu_on is False) or (
                self.menu_on is True and souris[0] == 1 and self.menu_click_open.collidepoint(
            self.event.pos)) or self.menu_en_cours is not None:

            self.player.credit = False

            if self.compteur == 0:
                if self.menu_on:
                    self.menu_on = False
                    self.menu_en_cours = 'up'
                else:
                    self.menu_on = True
                    self.menu_en_cours = 'down'

            if self.compteur >= 400:
                self.player.animation_index = 0
                self.menu_en_cours = None
                self.compteur = 0

            if self.menu_on and self.menu_en_cours == 'down':
                self.player.animation_menu('down', self.compteur)
                self.compteur += 16

            elif self.menu_en_cours == 'up':
                self.player.animation_menu('up', self.compteur)
                self.compteur += 16
                self.temps = 16

        # si un dialogue est lancé, ça met en pause le joueur met on peut ouvrir le menu
        elif self.dialog_box.reading is True:
            return

        # pour mettre un coup d’épée
        elif (souris[0] == 1 or self.mouvement_en_cours is not None) and not self.menu_on and not pressed[
            pygame.K_LALT] and self.player.name == "player" and self.mouvement_en_cours != "chargement":

            self.son.epee_sound()

            if souris[0] == 1 and self.compteur == 0 and self.epee is False:
                self.player.position[0] -= 64
                self.player.position[1] -= 64
                self.player.old_position = self.player.position
                self.epee = True

            if self.compteur >= 496 and souris[0] == 1:
                return

            elif self.compteur >= 496:
                self.mouvement_en_cours = None
                self.player.old_position = self.player.position
                self.compteur = 0

            elif self.cote == "up" or self.mouvement_en_cours == "sword_hit_up":
                self.mouvement_en_cours = "sword_hit_up"
                self.temps = 0
                self.player.change_animation_epee('sword_hit_up', self.compteur)
                self.player.attacking = True
                self.compteur += 2 * 8

            elif self.cote == "down" or self.mouvement_en_cours == "sword_hit_down":
                self.mouvement_en_cours = "sword_hit_down"
                self.temps = 0
                self.player.change_animation_epee('sword_hit_down', self.compteur)
                self.player.attacking = True
                self.compteur += 2 * 8

            elif self.cote == "right" or self.mouvement_en_cours == "sword_hit_right":
                self.mouvement_en_cours = "sword_hit_right"
                self.temps = 0
                self.player.change_animation_epee('sword_hit_right', self.compteur)
                self.player.attacking = True
                self.compteur += 2 * 8

            elif self.cote == "left" or self.mouvement_en_cours == "sword_hit_left":
                self.mouvement_en_cours = "sword_hit_left"
                self.temps = 0
                self.player.change_animation_epee('sword_hit_left', self.compteur)
                self.player.attacking = True
                self.compteur += 2 * 8

        # pour avancer

        elif pressed[pygame.K_z] and pressed[pygame.K_d] and self.mouvement_en_cours is None and not self.menu_on \
                and self.epee is False:
            self.temps = 0
            self.cote = "right"
            self.player.move_up_right()

        elif pressed[pygame.K_z] and pressed[pygame.K_q] and self.mouvement_en_cours is None and not self.menu_on \
                and self.epee is False:
            self.temps = 0
            self.cote = "left"
            self.player.move_up_left()

        elif pressed[pygame.K_s] and pressed[pygame.K_q] and self.mouvement_en_cours is None and not self.menu_on \
                and self.epee is False:
            self.temps = 0
            self.cote = "left"
            self.player.move_down_left()

        elif pressed[pygame.K_s] and pressed[pygame.K_d] and self.mouvement_en_cours is None and not self.menu_on and \
                self.epee is False:
            self.temps = 0
            self.cote = "right"
            self.player.move_down_right()

        elif pressed[pygame.K_z] and self.mouvement_en_cours is None and not self.menu_on and self.epee is False:
            self.temps = 0
            self.cote = "up"
            self.player.move_up()

        elif pressed[pygame.K_s] and self.mouvement_en_cours is None and not self.menu_on and self.epee is False:
            self.temps = 0
            self.cote = "down"
            self.player.move_down()

        elif pressed[pygame.K_d] and self.mouvement_en_cours is None and not self.menu_on and self.epee is False:
            self.temps = 0
            self.cote = "right"
            self.player.move_right()

        elif pressed[pygame.K_q] and self.mouvement_en_cours is None and not self.menu_on and self.epee is False:
            self.temps = 0
            self.cote = "left"
            self.player.move_left()

        elif pressed[pygame.K_p]:
            self.sauvegarde.restoration_coord()
        else:

            if self.temps >= 600 and not self.menu_on:
                self.player.change_animation('arret_' + self.cote)

            elif self.mouvement_en_cours is None:
                if self.epee is True:
                    self.player.position[0] += 64
                    self.player.position[1] += 64
                    self.epee = False
                self.player.arret(self.cote)
                self.temps += 1
                self.compteur = 0

    def barre_de_vie_blit(self):
        """
        La méthode barre_de_vie_blit permet d’afficher la barre de vie
        """
        if self.fullscreen:
            self.screen.blit(self.player.barre_de_vie, [self.player.x_position - (self.player.x_position // 4.8), 0])
        else:
            self.screen.blit(self.player.barre_de_vie, [self.player.x_position - (self.player.x_position // 4.8), 0])

    def update(self):
        self.map_manager.update()

    def dialogue(self):
        self.dialog_box.execute("Inconnu", ["Un Orc nous attaque !!!"])
        self.player.start = True

    def dialogue_mino(self):
        self.dialog_box.execute("???", ["$*$*$*$ (je me suis perdu dans cette foutue forêt !)"])
        self.passage_mino = True

    def dialogue_boss1(self):
        self.dialog_box.execute("???", ["Tu m'as rattrapé..."])
        self.passage_boss1 = True

    def dialogue_boss2(self):
        self.dialog_box.execute("Arlong", ["Je suis Arlong, enchanté."])
        self.passage_boss2 = True

    def dialogue_boss3(self):
        self.dialog_box.execute("Arlong", ["Je vais te tuer puis exterminer ce village."])
        self.passage_boss3 = True

    def run(self):
        """
        La méthode run permet d’actualiser et de vérifier à chaque tick les différents événements
        """
        # permet de fixer les fps
        clock = pygame.time.Clock()

        # boucle du jeu
        running = True

        while running is True:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.screen.blit(self.player.menu, [0, 0])
            self.screen.blit(self.player.chiffre_musique, [317, 156])
            self.screen.blit(self.player.chiffre_effet, [317, 193])
            self.screen.blit(self.player.menu, [0, 0])
            self.barre_de_vie_blit()
            self.screen.blit(self.player.mort_info, [0, 0])
            self.screen.blit(self.player.etrange, [0, 0])
            if self.player.dialog_en_cours and not self.player.start:
                self.dialogue()
            if self.player.dialog_en_cours and self.player.start and self.map_manager.passage_mino \
                    and not self.passage_mino:
                self.dialogue_mino()
            if self.player.dialog_en_cours and self.player.start and self.map_manager.passage_boss \
                    and not self.passage_boss1:
                self.dialogue_boss1()
            if not self.player.dialog_en_cours and self.player.start and self.map_manager.passage_boss \
                    and self.passage_boss1 and not self.passage_boss2:
                self.player.dialog_en_cours = True
                self.dialogue_boss2()
            if not self.player.dialog_en_cours and self.player.start and self.map_manager.passage_boss \
                    and self.passage_boss1 and self.passage_boss2 and not self.passage_boss3:
                self.player.dialog_en_cours = True
                self.dialogue_boss3()

            pygame.display.flip()

            if self.epee:
                self.map_manager.oui = True
                self.rect = (self.player.position[0] + 96, self.player.position[1] + 96, 192, 192)
                self.map_manager.get_group().center(self.rect)

            if self.menu_on is True or self.mouse is True:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)

            # permet de fermer le jeu
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT or not self.running:
                    running = False
                elif self.event.type == pygame.KEYDOWN:
                    if self.event.key == pygame.K_SPACE:
                        if self.player.dialog_en_cours:
                            self.dialog_box.execute("", [])
                            self.player.dialog_en_cours = False
                        check = self.map_manager.check_npc_collisions_dialog(self.dialog_box)
                        if check is not None:
                            self.map_manager.changement_direction_npc(check, self.cote)
                    if self.event.key == pygame.K_LSHIFT:
                        self.player.sprint()

                    # Adaptation de la taille de la fenêtre et des différents éléments graphiques
                    if self.event.key == pygame.K_F11 and self.player.mort == 0:
                        if self.fullscreen is True:
                            self.screen = pygame.display.set_mode(
                                (self.taillefenetre.current_w // 1.5, self.taillefenetre.current_h // 1.5))
                            self.dialog_box.font = pygame.font.Font("../dialogs/Pixellari.ttf",
                                                                    self.dialog_box.x_position // 90)
                            self.dialog_box.x_position = self.taillefenetre.current_w // 1.5
                            self.dialog_box.y_position = self.taillefenetre.current_h // 1.5
                            self.dialog_box.box = pygame.transform.scale(self.dialog_box.box, (
                                self.dialog_box.x_position * 2, self.dialog_box.y_position * 2))
                            self.player.x_position = self.taillefenetre.current_w // 1.5
                            self.player.y_position = self.taillefenetre.current_h // 1.5

                            self.player.menu = pygame.transform.scale(self.player.menu, (
                                self.player.x_position // 5.4, self.player.y_position // 1.4))
                            self.player.menu.set_colorkey([75, 75, 75])
                            self.player.menu.blit(self.player.menu, (0, 0), (0, 0, 355, 756))

                            self.player.barre_de_vie = pygame.transform.scale(self.player.barre_de_vie, (
                                self.player.x_position * 2, self.player.y_position * 2))
                            self.player.barre_de_vie.set_colorkey([0, 0, 0])
                            self.player.barre_de_vie.blit(self.player.barre_de_vie, (0, 0), (0, 0, 200, 20))

                            self.player.mort_info = pygame.transform.scale(self.player.mort_info, (
                                self.player.x_position, self.player.y_position))
                            self.player.mort_info.set_colorkey([0, 0, 0])
                            self.player.mort_info.blit(self.player.mort_info, (0, 0), (0, 0, 1920, 1080))

                            self.player.etrange = pygame.transform.scale(self.player.etrange, (
                                self.player.x_position, self.player.y_position))
                            self.player.etrange.set_colorkey([0, 0, 0])
                            self.player.etrange.blit(self.player.etrange, (0, 0), (0, 0, 1920, 1080))

                            self.menu_click_close = pygame.Rect((self.player.x_position // 6.04, 0),
                                                                (self.player.x_position // 40,
                                                                 self.player.y_position // 21))
                            self.menu_click_open = pygame.Rect(
                                (self.player.x_position // 6.04, self.player.y_position // 1.52),
                                (self.player.x_position // 40, self.player.y_position // 20))

                            self.bouton_options_rect = pygame.Rect(
                                (self.taillefenetre.current_w // (self.taillefenetre.current_w / 81),
                                 (self.taillefenetre.current_h // (self.taillefenetre.current_h / 173))),
                                (187, 93))

                            self.bouton_credits_rect = pygame.Rect(
                                (self.taillefenetre.current_w // (self.taillefenetre.current_w / 81),
                                 (self.taillefenetre.current_h // (self.taillefenetre.current_h / 338))),
                                (187, 93))

                            self.bouton_quitter_rect = pygame.Rect(
                                (self.taillefenetre.current_w // (self.taillefenetre.current_w / 83),
                                 (self.taillefenetre.current_h // (self.taillefenetre.current_h / 501))),
                                (187, 93))

                            self.fullscreen = False

                        elif self.fullscreen is False:
                            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                            self.dialog_box.x_position = self.taillefenetre.current_w
                            self.dialog_box.y_position = self.taillefenetre.current_h
                            self.dialog_box.font = pygame.font.Font("../dialogs/Pixellari.ttf",
                                                                    self.dialog_box.x_position // 60)
                            self.dialog_box.box = pygame.transform.scale(self.dialog_box.box, (
                                self.dialog_box.x_position * 2, self.dialog_box.y_position * 2))
                            self.player.x_position = self.taillefenetre.current_w
                            self.player.y_position = self.taillefenetre.current_h

                            self.player.menu = pygame.transform.scale(self.player.menu, (
                                self.player.x_position // 5.4, self.player.y_position // 1.4))
                            self.player.menu.set_colorkey([75, 75, 75])
                            self.player.menu.blit(self.player.menu, (0, 0), (0, 0, 355, 756))

                            self.player.barre_de_vie = pygame.transform.scale(self.player.barre_de_vie, (
                                self.player.x_position * 2, self.player.y_position * 2))
                            self.player.barre_de_vie.set_colorkey([0, 0, 0])
                            self.player.barre_de_vie.blit(self.player.barre_de_vie, (0, 0), (0, 0, 200, 20))

                            self.player.mort_info = pygame.transform.scale(self.player.mort_info, (
                                self.player.x_position, self.player.y_position))
                            self.player.mort_info.set_colorkey([0, 0, 0])
                            self.player.mort_info.blit(self.player.mort_info, (0, 0), (0, 0, 1920, 1080))

                            self.player.etrange = pygame.transform.scale(self.player.etrange, (
                                self.player.x_position, self.player.y_position))
                            self.player.etrange.set_colorkey([0, 0, 0])
                            self.player.etrange.blit(self.player.etrange, (0, 0), (0, 0, 1920, 1080))

                            self.menu_click_close = pygame.Rect((self.taillefenetre.current_w // 6.04, 0),
                                                                (self.taillefenetre.current_w // 40,
                                                                 self.taillefenetre.current_h // 21))
                            self.menu_click_open = pygame.Rect(
                                (self.taillefenetre.current_w // 6.04, self.taillefenetre.current_h // 1.52),
                                (self.taillefenetre.current_w // 40, self.taillefenetre.current_h // 20))

                            self.bouton_options_rect = pygame.Rect(
                                (self.taillefenetre.current_w // (self.taillefenetre.current_w / 81),
                                 (self.taillefenetre.current_h // (self.taillefenetre.current_h / 173))),
                                (187, 93))

                            self.bouton_credits_rect = pygame.Rect(
                                (self.taillefenetre.current_w // (self.taillefenetre.current_w / 81),
                                 (self.taillefenetre.current_h // (self.taillefenetre.current_h / 338))),
                                (187, 93))

                            self.bouton_quitter_rect = pygame.Rect(
                                (self.taillefenetre.current_w // (self.taillefenetre.current_w / 83),
                                 (self.taillefenetre.current_h // (self.taillefenetre.current_h / 501))),
                                (187, 93))

                            self.fullscreen = True
            # permet de fixer les fps
            clock.tick(60)

        pygame.quit()
