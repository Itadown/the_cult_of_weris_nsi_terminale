import pygame
from animations import AnimateSprite
from save import Sauvegarde
from sound import Sound


class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)

        self.health = 100
        self.sauvegarde = Sauvegarde()
        self.cote = None
        self.image = self.get_image_64x64(0, 640)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
        self.old_position = self.position.copy()
        self.attaque = 0

    def save_location(self):
        """
        La méthode save_location permet de sauvegarder la position - 1 du joueur
        """
        self.old_position = self.position.copy()

    """
    Les méthodes move_* permettent de déplacer le joueur en l'animant
    """
    def move_right(self):
        self.change_animation('right')
        self.position[0] += self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("right")

    def move_left(self):
        self.change_animation('left')
        self.position[0] -= self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("left")

    def move_up(self):
        self.change_animation('up')
        self.position[1] -= self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("up")

    def move_down(self):
        self.change_animation('down')
        self.position[1] += self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("down")

    def move_up_right(self):
        self.change_animation("right")
        self.position[1] -= self.speed
        self.position[0] += self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("right")

    def move_up_left(self):
        self.change_animation("left")
        self.position[1] -= self.speed
        self.position[0] -= self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("left")

    def move_down_right(self):
        self.change_animation("right")
        self.position[1] += self.speed
        self.position[0] += self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("right")

    def move_down_left(self):
        self.change_animation("left")
        self.position[1] += self.speed
        self.position[0] -= self.speed
        if type(self) == Player:
            self.sauvegarde.sauvegarde_player(self.position)
            self.sauvegarde.sauvegarde_cote("left")

    def arret(self, cote):
        """
        La méthode arret permet d’afficher une image d’arrêt des entités
        """

        if cote is None:
            return

        self.cote = cote

        # ligne pour la marche
        if cote == "up":
            cote = 512
        elif cote == "left":
            cote = 576
        elif cote == "down":
            cote = 640
        elif cote == "right":
            cote = 704

        self.image = self.get_image_64x64(0, cote)
        self.image.set_colorkey([0, 0, 0])

    def update(self):
        """
        La méthode update s’actualise à chaque tick, elle permet de déplacer le rectangle de collision du joueur
        """
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        """
        La méthode move_back permet de replacer le joueur à sa position - 1
        """
        self.position = self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom


class Player(Entity):

    def __init__(self):
        super().__init__("player_no_armor", 0, 0)
        self.oui = False
        self.test = 1
        self.player_attack_radius = 60
        self.player_status = "idle"
        self.health = 100
        self.damage = 10
        self.son = Sound()
        self.mort = 0
        self.start = False
        self.dialog_en_cours = False
        self.respawn_etrange = False

        self.current_time = 0

        self.attacking = False  # variable qui indique si le joueur attaque

        # coup d’épée
        self.mouvement_en_cours = None
        self.compteur = 0

        # savoir le cote et le temps d’arrêt
        self.cote = self.sauvegarde.restoration_cote()
        self.temps = 0
        self.epee = False

    def morta(self, compteur):
        """
        La méthode morta permet de faire le lien avec la classe animation pour animer la mort du joueur
        """
        self.animation_mort(compteur)

    def arret(self, cote):
        """
        La méthode arret permet d’afficher une image d’arrêt du joueur
        """
        if cote is None:
            return

        self.sauvegarde.sauvegarde_cote(cote)
        self.cote = cote

        # ligne pour la marche
        if cote == "up":
            cote = 512
        elif cote == "left":
            cote = 576
        elif cote == "down":
            cote = 640
        elif cote == "right":
            cote = 704

        self.image = self.get_image_64x64(0, cote)
        self.image.set_colorkey([0, 0, 0])

    def sprint(self):
        """
        La méthode sprint permet de faire courir le joueur
        """
        self.change_speed(3)

    def grass_sound(self, var):
        """
        La méthode grass_sound permet de joueur le son du joueur
        """
        self.son_grass(var)


class NPC(Entity):

    def __init__(self, name, cotenpc, nb_points, dialog):
        super().__init__(name, 0, 0)
        self.nb_points = nb_points
        self.dialog = dialog
        self.cotenpc = cotenpc
        self.points = []
        self.name = name
        self.speed = 2
        self.current_point = 0
        self.collision_rect = self.feet = pygame.Rect(0, 0, 0.7 * self.rect.width, 0.7 * self.rect.height)
        self.parler = True

    def changement_direct(self, cote):

        self.cote = cote
        if self.cotenpc == "up" or self.cote == "down":
            self.cotenpc = 512
        elif self.cotenpc == "left" or self.cote == "right":
            self.cotenpc = 576
        elif self.cotenpc == "down" or self.cote == 'up':
            self.cotenpc = 640
        elif self.cotenpc == "right" or self.cote == 'left':
            self.cotenpc = 704

        self.image = self.get_image_64x64(0, self.cotenpc)
        self.image.set_colorkey([0, 0, 0])

    def move(self, start):
        """
        La méthode move permet de faire le déplacement des pnjs
        """
        
        current_point = self.current_point
        target_point = self.current_point + 1

        if not start:
            return
        if self.name == "Boss" and target_point == self.nb_points:
            return
        tab = ["Orc", "Bertrand (villageois)", "Franck (papa)", "Jonathan (villageois)",
               "Agathe (villageoise)", "Catherine (maman)", "Charlène (villageoise)"]
        if self.name in tab and target_point == self.nb_points:
            self.arret(self.cotenpc)
            self.parler = True
            return

        if self.cotenpc == "up":
            self.cotenpc = 512
        elif self.cotenpc == "left":
            self.cotenpc = 576
        elif self.cotenpc == "down":
            self.cotenpc = 640
        elif self.cotenpc == "right":
            self.cotenpc = 704

        self.image = self.get_image_64x64(0, self.cotenpc)
        self.image.set_colorkey([0, 0, 0])

        if target_point >= self.nb_points:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_down()
            self.parler = False
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:
            self.move_up()
            self.parler = False
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_left()
            self.parler = False
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:
            self.move_right()
            self.parler = False

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        """
        La méthode teleport_spawn téléporte le pnj à son emplacement initial
        """
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_point(self, tmx_data):
        """
        La méthode load_point permet de charger les différents points pour les déplacements des pnjs
        """
        for num in range(1, self.nb_points + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)

    def grass_sound(self, var):
        """
        La méthode grass_sound permet de jouer le son de l'herbe
        """
        return self.son_grass_other(var)


class Monster(NPC):
    monster_data = {
        "Minotaure": {"health": 250, "damage": 20, "attack_radius": 25, "notice_radius": 200, "weapon": "axe"},
        "Orc": {"health": 180, "damage": 15, "attack_radius": 30, "notice_radius": 240, "weapon": "spear"},
        "Orc_female": {"health": 170, "damage": 15, "attack_radius": 30, "notice_radius": 240, "weapon": "spear"},
        "Boss": {"health": 1000, "damage": 80, "attack_radius": 30, "notice_radius": 300, "weapon": "sword"},
        "Inosuke": {"health": 330, "damage": 50, "attack_radius": 30, "notice_radius": 150, "weapon": "long_axe"},
        "Sbir": {"health": 60, "damage": 30, "attack_radius": 30, "notice_radius": 400, "weapon": "scythe"},
        "Wolf": {"health": 100, "damage": 35, "attack_radius": 34, "notice_radius": 350, "weapon": "long_axe"}

        }

    def __init__(self, type_monster, cotenpc, nb_points, dialog):
        super().__init__(type_monster, cotenpc, nb_points, dialog)
        self.player_vec = None
        self.direction = None
        self.distance = None
        self.status = "idle"
        self.health = self.monster_data[type_monster]["health"]
        self.damage = self.monster_data[type_monster]["damage"]
        self.attack_radius = self.monster_data[type_monster]["attack_radius"]
        self.notice_radius = self.monster_data[type_monster]["notice_radius"]
        self.weapon = self.monster_data[type_monster]["weapon"]
        self.player = Player()
        self.monster_compteur = 0
        self.monster_cote = None
        self.attacking = False

    def lance_animation(self):
        """
        La méthode lance_animation permet de faire les animations de coup des monstres
        """
        weapon = "axe"

        if self.monster_cote == "up":
            self.change_animation(f'{weapon}_hit_up')

        elif self.monster_cote == "down":
            self.change_animation(f'{weapon}_hit_down')

        elif self.monster_cote == "right":
            self.change_animation(f'{weapon}_hit_right')

        elif self.monster_cote == "left":
            self.change_animation(f'{weapon}_hit_left')

    def stop_monstre(self):
        """
        La méthode stop_monstre permet d’afficher l’image du monstre lorsqu’il est à l’arrêt
        """

        cote = None

        if self.monster_cote is None:
            return

        # ligne pour la marche
        if self.monster_cote == "up":
            cote = 512
        elif self.monster_cote == "left":
            cote = 576
        elif self.monster_cote == "down":
            cote = 640
        elif self.monster_cote == "right":
            cote = 704

        self.image = self.get_image_64x64(0, cote)
        self.image.set_colorkey([0, 0, 0])

    def get_player_distance_direction(self, player, epee):
        """
        La méthode get_player_distance_direction permet de calculer la distance entre le joueur et le monstre
        """
        monster_vec = pygame.math.Vector2(self.rect.center)
        if epee:
            self.player.oui = False
            self.player_vec = pygame.math.Vector2(player.rect.center)
            self.player_vec[0] += 64
            self.player_vec[1] += 64
        else:
            self.player_vec = pygame.math.Vector2(player.rect.center)
        self.distance = (self.player_vec - monster_vec).magnitude()
        if self.distance > 0:
            self.direction = (self.player_vec - monster_vec).normalize()
        else:
            self.direction = pygame.math.Vector2()

        return

    def grass_sound(self, var):
        return self.son_grass_other(var)

    def get_status(self):
        """
        La méthode get_status permet de définir ce que doit faire le monstre
        """
        if self.distance <= self.attack_radius:
            self.status = 'attack'
        elif self.distance <= self.notice_radius:
            self.status = 'chase'
            self.chase()
        else:
            self.status = 'idle'
        return self.check_attacking()

    def chase(self):
        """
        La méthode chase permet de faire en sorte que le monstre se déplace automatiquement vers le joueur
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.save_location()

        if self.direction[0] > 0.65 and self.direction[1] > 0.65:
            self.move_down_right()
            self.monster_cote = "right"
        elif self.direction[0] < -0.65 and self.direction[1] > 0.65:
            self.move_down_left()
            self.monster_cote = "left"
        elif self.direction[0] > 0.65 and self.direction[1] < -0.65:
            self.move_up_right()
            self.monster_cote = "right"
        elif self.direction[0] < -0.65 and self.direction[1] < -0.65:
            self.move_up_left()
            self.monster_cote = "left"
        elif self.direction[0] > 0 and self.direction[1] < 0:
            self.move_right()
            self.monster_cote = "right"
        elif self.direction[0] < 0 and self.direction[1] > 0:
            self.move_left()
            self.monster_cote = "left"
        elif self.direction[0] < 0 and self.direction[1] < 0:
            self.move_up()
            self.monster_cote = "up"
        elif self.direction[0] > 0 and self.direction[1] > 0:
            self.move_down()
            self.monster_cote = "down"
        elif self.direction[0] == 0 and self.direction[1] == 0:
            self.move_up()
            self.monster_cote = "up"
        elif self.direction[0] == 1 and self.direction[1] == 1:
            self.move_down()
            self.monster_cote = "down"
        elif self.direction[0] == 0 and self.direction[1] == 1:
            self.move_left()
            self.monster_cote = "left"
        elif self.direction[0] == 1 and self.direction[1] == 0:
            self.move_right()
            self.monster_cote = "right"

    def check_attacking(self):
        """
        La méthode check_attacking permet de vérifier si le monstre attaque
        """
        if self.status == 'attack':
            self.attacking = True
        else:
            self.attacking = False
        return self.attacking

        # lancer l’animation

    def check_death(self):
        """
        La méthode check_death permet de vérifier si le monstre est toujours en vie
        """
        if self.health <= 0:
            self.kill()
            self.damage = 0

    def monster_update(self, player, epee):
        """
        La méthode monster_update permet d’actualiser les différentes fonctions
        """
        self.check_death()
        self.get_player_distance_direction(player, epee)
        self.get_status()

    def teleport_spawn(self):
        """
        La méthode teleport_spawn permet de téléporter le monstre à son point d’origine
        """
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()
