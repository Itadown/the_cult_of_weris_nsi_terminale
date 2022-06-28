from dataclasses import dataclass
from save import Sauvegarde

import pygame
import pyscroll
import pytmx
from player import NPC, Monster
from dialog import DialogBox


@dataclass
class Portal:
    """
    Class qui permet de changer de map
    """
    from_world: str  # monde d’origine avant le changement
    origin_point: str  # point de collision pour rentrer dans la nouvelle map
    target_world: str  # monde cible
    teleport_point: str  # point d’apparition dans le monde cible


@dataclass
class Map:
    """
    Permet de générer une autre map, on utilise la notion
    de dataclass, elle va seulement représenter des données
    sans contenir de méthode(s)
    """
    name: str  # nom de la map
    walls: list[pygame.Rect]  # gérer les rectangles de collision
    grass: list[pygame.Rect]
    group: pyscroll.PyscrollGroup  # assembler les tuiles du jeu
    tmx_data: pytmx.TiledMap
    portals: list[Portal]  # tout les tps de la map
    npcs: list[NPC]
    monsters: list[Monster]


class MapManager:
    """
    Gère les différentes cartes et les enregistres
    """

    def __init__(self, screen, player):

        self.compteurmort = 0
        self.compteur = 0
        self.player_cooldown = 0
        self.cooldown = 0

        self.maps = dict()
        self.taillefenetre = pygame.display.Info()

        x = self.taillefenetre.current_w // 10
        y = self.taillefenetre.current_h // 10

        self.dialog_box = DialogBox(x, y)
        self.screen = screen
        self.player = player
        self.sauvegarde = Sauvegarde()
        self.current_map = "weris"
        self.oui = False
        self.animation = False
        self.monstre = None
        self.compteur_monstre = 0
        self.epee = False
        self.passage_mino = False
        self.passage_boss = False

        # Lancement des sauvegardes des maps (pour qu’elles soient toujours chargées)

        self.register_map("weris",
                          portals=[Portal(from_world="weris", origin_point="enter_house", target_world="maison",
                                          teleport_point="spawn_house"),
                                   Portal(from_world="weris", origin_point="exit", target_world="foret_debut",
                                          teleport_point="spawn_clairiere"),
                                   Portal(from_world="weris", origin_point="enter_house_parents",
                                          target_world="maison_parents",
                                          teleport_point="spawn_parents_house")
                                   ],

                          npcs=[NPC(name="Charlène (villageoise)", cotenpc='left', nb_points=1,
                                    dialog=["T'as tué le monstre ??",
                                            "Vas voir ton père, il t'attend à la sortie du village!"]),
                                NPC(name="Catherine (maman)", cotenpc='left', nb_points=1,
                                    dialog=["J'espère que le monstre est mort.",
                                            "Il était au centre du village, par chance nous l'avons fuit.",
                                            "Vas voir ton père à la sortie du village après !"]),
                                NPC(name="Agathe (villageoise)", cotenpc='left', nb_points=1,
                                    dialog=["Il n'y a plus de monstre ?",
                                            "Ton père nous a dit qu'il t'attendait à la sortie du village."]),
                                NPC(name="Bertrand (villageois)", cotenpc='left', nb_points=1,
                                    dialog=["Va voir ton père si le monstre est mort.",
                                            "Il est à la sortie du village."]),
                                NPC(name="Jonathan (villageois)", cotenpc='left', nb_points=1,
                                    dialog=["Il est horrible ce monstre, j'espère qu'il est mort.",
                                            "Ah oui, vas voir ton père à la sortie du village, il t'attend !"]),
                                NPC(name="Franck (papa)", cotenpc='left', nb_points=1,
                                    dialog=["Ce n'est vraiment pas normal qu'on se fasse attaquer...",
                                            "Il faut que tu ailles voir, je ne peux plus maintenant...",
                                            "Vas au village voisin pour découvrir ce qui s'y trame !",
                                            "Fais attention sur la route, il y a une forêt étrange...",
                                            "Et potentiellement d'autres monstres !!", "Bonne chance fiston !"])
                                ],
                          monsters=[Monster(type_monster="Orc", cotenpc="right", nb_points=1, dialog=None)
                                    ]

                          )

        self.register_map("weris_debut",
                          portals=[
                              Portal(from_world="weris_debut", origin_point="bouclier", target_world="weris_milieu",
                                     teleport_point="bouclier_recup"),
                              Portal(from_world="weris_debut", origin_point="alarme_declencheuse",
                                     target_world="weris_debut",
                                     teleport_point="player_debut")
                          ],

                          npcs=[NPC(name="Orc", cotenpc='right', nb_points=2, dialog=None),
                                NPC(name="Charlène (villageoise)", cotenpc='left', nb_points=3,
                                    dialog=["On se fait attaquer !!", "Vas chercher ton bouclier !",
                                            "Tu sais pas où il est ?!", "Demande à ton père qui est à l'écart !"]),
                                NPC(name="Catherine (maman)", cotenpc='left', nb_points=2,
                                    dialog=["On se fait attaquer mon chéri !!", "Fais attention à toi !",
                                            "Vas chercher le bouclier pour te défendre.",
                                            "Ton père doit sûrement savoir où il est...",
                                            "Va le voir derrière moi !"]),
                                NPC(name="Agathe (villageoise)", cotenpc='left', nb_points=2,
                                    dialog=["Vas chercher ton bouclier !!",
                                            "Je crois que ton père avait dit qu'il était en haut une fois...",
                                            "Vas le voir pour être sur, il est juste derrière !"]),
                                NPC(name="Bertrand (villageois)", cotenpc='left', nb_points=3,
                                    dialog=["Ton bouclier ??", "Demande à ton père, il est pas loin."]),
                                NPC(name="Jonathan (villageois)", cotenpc='left', nb_points=3,
                                    dialog=["Pourquoi t'as toujours pas ton bouclier ?!",
                                            "Demande vite à ton père où il est !", "Ton père est juste à côté !"]),
                                NPC(name="Franck (papa)", cotenpc='left', nb_points=1,
                                    dialog=["Vas chercher ton bouclier fiston.",
                                            "Il est sur le tronc d'arbre en haut du village.",
                                            "C'est là où tu jouais que tu étais enfant."])
                                ]

                          )

        self.register_map("weris_milieu",
                          portals=[Portal(from_world="weris_milieu", origin_point="enter_house_parents_debut",
                                          target_world="maison_parents_debut",
                                          teleport_point="spawn_parents_house_debut"),
                                   ],

                          npcs=[NPC(name="Orc", cotenpc='right', nb_points=1, dialog=None),
                                NPC(name="Charlène (villageoise)", cotenpc='left', nb_points=1,
                                    dialog=["Vas plus vite !!", "Il te faudrait une épée !", "Demande à ton père !",
                                            "Tu sais rien faire tout seul !!"]),
                                NPC(name="Catherine (maman)", cotenpc='left', nb_points=1,
                                    dialog=["Demande à ton père pour une épée !",
                                            "Nous ne tiendrons plus longtemps !"]),
                                NPC(name="Agathe (villageoise)", cotenpc='left', nb_points=1,
                                    dialog=["Il te faut une arme !", "Ton père sait certainement où en trouver une !"]),
                                NPC(name="Bertrand (villageois)", cotenpc='left', nb_points=1,
                                    dialog=["Aller, viite.", "Demande à ton père pour l'épée !",
                                            "Je commence à être à bout de souffle."]),
                                NPC(name="Jonathan (villageois)", cotenpc='left', nb_points=1,
                                    dialog=["Vite, il me faut une pause", "Va voir ton père !"]),
                                NPC(name="Franck (papa)", cotenpc='left', nb_points=1,
                                    dialog=["Vas chercher mon épée d'aventurier.", "Elle est dans notre maison en haut.",
                                            "Tu la verras certainement en entrant."])
                                ]

                          )

        self.register_map("weris_final",
                          portals=[Portal(from_world="weris_final", origin_point="enter_house",
                                          target_world="maison_joueur_finale",
                                          teleport_point="spawn_house"),
                                   Portal(from_world="weris_final", origin_point="exit", target_world="foret_finale",
                                          teleport_point="spawn_clairiere"),
                                   Portal(from_world="weris_final", origin_point="enter_house_parents",
                                          target_world="maison_parents_finale",
                                          teleport_point="spawn_parents_house")
                                   ],

                          npcs=[NPC(name="PNJtest", cotenpc='up', nb_points=1,
                                    dialog=["Bonjour !", "Je suis le PNJ historique de test de ce jeu !",
                                            "JE SUIS INCROYABLE !",
                                            "RESPECTE MOI !"]),
                                NPC(name="Charlène (villageoise)", cotenpc='left', nb_points=1,
                                    dialog=["Alors ??", "Ah, tant que tu es là ça ira je pense."]),
                                NPC(name="Catherine (maman)", cotenpc='left', nb_points=1,
                                    dialog=["Tu t'es occupé du problème ?", "Bien joué chéri !",
                                            "Tant que ton père et toi seront là, le village ira bien !"]),
                                NPC(name="Agathe (villageoise)", cotenpc='left', nb_points=1,
                                    dialog=["Alors c'était dû à quoi ?",
                                            "Oh ok, j'espère qu'ils ne vont plus attaquer !"]),
                                NPC(name="Bertrand (villageois)", cotenpc='left', nb_points=1,
                                    dialog=["Alors, d'où venait le problème ?",
                                            "J'espère qu'ils n'attaqueront plus...",
                                            "De toute façon tu es là pour nous protéger !"]),
                                NPC(name="Jonathan (villageois)", cotenpc='left', nb_points=1,
                                    dialog=["D'où ça venait ??", "Oh, je vois...",
                                            "Ils n'attaqueront plus après cette raclée qu'ils se sont pris."]),
                                NPC(name="Franck (papa)", cotenpc='left', nb_points=1,
                                    dialog=["Alors, quel était le problème ?",
                                            "Oh, je vois... content que tu sois en vie fiston.",
                                            "Tant que tu es là ça ira !"])
                                ]
                          )

        self.register_map("foret_debut",
                          portals=[Portal(from_world="foret_debut", origin_point="return1", target_world="foret_debut",
                                          teleport_point="respawn"),
                                   Portal(from_world="foret_debut", origin_point="return2", target_world="foret_debut",
                                          teleport_point="respawn"),
                                   Portal(from_world="foret_debut", origin_point="return3", target_world="foret_debut",
                                          teleport_point="respawn"),
                                   Portal(from_world="foret_debut", origin_point="return4", target_world="foret_debut",
                                          teleport_point="respawn"),
                                   Portal(from_world="foret_debut", origin_point="return5", target_world="foret_debut",
                                          teleport_point="respawn"),
                                   Portal(from_world="foret_debut", origin_point="plaine", target_world="plaine_debut",
                                          teleport_point="spawn_plaine"),
                                   Portal(from_world="foret_debut", origin_point="minotaure_parle",
                                          target_world="foret_debut",
                                          teleport_point="minotaure")
                                   ],
                          monsters=[Monster(type_monster="Minotaure", cotenpc="right", nb_points=1, dialog=None),
                                    ]

                          )

        self.register_map("foret_finale",
                          portals=[
                              Portal(from_world="foret_finale", origin_point="return1", target_world="foret_finale",
                                     teleport_point="respawn"),
                              Portal(from_world="foret_finale", origin_point="return2", target_world="foret_finale",
                                     teleport_point="respawn"),
                              Portal(from_world="foret_finale", origin_point="return3", target_world="foret_finale",
                                     teleport_point="respawn"),
                              Portal(from_world="foret_finale", origin_point="return4", target_world="foret_finale",
                                     teleport_point="respawn"),
                              Portal(from_world="foret_finale", origin_point="return5", target_world="foret_finale",
                                     teleport_point="respawn"),
                              Portal(from_world="foret_finale", origin_point="plaine", target_world="plaine_finale",
                                     teleport_point="spawn_plaine_finale"),
                              Portal(from_world="foret_finale", origin_point="weris_village",
                                     target_world="weris_final",
                                     teleport_point="spawn_weris"),
                              Portal(from_world="foret_finale", origin_point="boss_parle",
                                     target_world="foret_finale",
                                     teleport_point="boss_parle_tp")
                          ],
                          monsters=[Monster(type_monster="Boss", cotenpc="right", nb_points=1, dialog=None),
                                    ]

                          )

        self.register_map("maison_parents",
                          portals=[Portal(from_world="maison_parents", origin_point="exit_parents_house",
                                          target_world="weris",
                                          teleport_point="enter_house_exit_parents")]
                          )

        self.register_map("maison_parents_finale",
                          portals=[Portal(from_world="maison_parents_finale", origin_point="exit_parents_house",
                                          target_world="weris_final",
                                          teleport_point="enter_house_exit_parents")]
                          )

        self.register_map("plaine_debut",
                          portals=[
                              Portal(from_world="plaine_debut", origin_point="village", target_world="village_debut",
                                     teleport_point="village_debut_spawn")]
                          )

        self.register_map("plaine_finale",
                          portals=[Portal(from_world="plaine_finale", origin_point="foret", target_world="foret_finale",
                                          teleport_point="fin_foret"),
                                   Portal(from_world="plaine_finale", origin_point="village",
                                          target_world="village_final",
                                          teleport_point="village_final_spawn")]
                          )

        self.register_map("village_debut",
                          portals=[Portal(from_world="village_debut", origin_point="tp_plaine_finale",
                                          target_world="plaine_finale",
                                          teleport_point="tp_plaine")],
                          npcs=[NPC(name="Garde (lieutenant)", cotenpc='right', nb_points=1,
                                    dialog=["J'espère qu'il va réussir à exterminer le village.",
                                            "On va enfin pouvoir s'étendre."]),
                                NPC(name="Garde", cotenpc='right', nb_points=1,
                                    dialog=["Enfin une vraie expédition pour se débarrasser du village !",
                                            "C'est notre meilleur élément...",
                                            "Il va l'exterminer en un clin d'oeil !"]),
                                NPC(name="Boss", cotenpc='left', nb_points=4, dialog=None)]
                          )

        self.register_map("village_final",
                          portals=[Portal(from_world="village_final", origin_point="tp_plaine_finalee",
                                          target_world="plaine_finale",
                                          teleport_point="tp_plaine")],
                          npcs=[NPC(name="Garde (lieutenant)", cotenpc='right', nb_points=1,
                                    dialog=["Il est parti il y a longtemps maintenant",
                                            "J'espère qu'il a réussi à exterminer ce village."]),
                                NPC(name="Garde", cotenpc='right', nb_points=1, dialog=["..."])]
                          )

        self.register_map("maison_joueur", portals=[
            Portal(from_world="maison_joueur", origin_point="exit_house", target_world="weris",
                   teleport_point="enter_house_exit")]

                          )

        self.register_map("maison_joueur_finale", portals=[
            Portal(from_world="maison_joueur_finale", origin_point="exit_house", target_world="weris_final",
                   teleport_point="enter_house_exit")]

                          )

        self.register_map("maison_parents_debut",
                          portals=[Portal(from_world="maison_parents_debut", origin_point="epee",
                                          target_world="maison_parents",
                                          teleport_point="epee_recup")]

                          )
        self.teleport_player("player")
        self.teleport_npc()

    def check_npc_collisions_dialog(self, dialog_box):
        """
        La méthode check_npc_collisions_dialog permet de vérifier si l’utilisateur est en contact avec le pnj pour
        pouvoir lancer son dialogue
        """
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and (type(sprite) is NPC or type(sprite) is Monster):
                if sprite.parler:
                    self.changement_direction_npc(sprite, "up")
                    dialog_box.execute(sprite.name, sprite.dialog)
                    return sprite
        return None

    def check_collisions(self):
        """
        Méthode pour les collisions aux objets de la map et les collisions des portails
        """
        retourne_arriere = ["return1", "return2", "return3", "return4", "return5"]
        # portails
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                if portal.origin_point in retourne_arriere:
                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x, point.y, point.width, point.height)  # Permet de définir le rectangle
                    # de collision du portail
                    if self.player.feet.colliderect(rect):
                        self.current_map = portal.target_world
                        self.player.mort = 2
                        for sprite in self.get_group().sprites():
                            sprite.move_back()
                        self.player.respawn_etrange = True

                if portal.origin_point == "boss_parle" and not self.player.dialog_en_cours and not self.passage_boss:
                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x, point.y, point.width, point.height)
                    if self.player.feet.colliderect(rect):
                        self.player.dialog_en_cours = True
                        self.passage_boss = True

                if portal.origin_point == "minotaure_parle" and not self.player.dialog_en_cours \
                        and self.player.start and not self.passage_mino:
                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x, point.y, point.width, point.height)
                    if self.player.feet.colliderect(rect):
                        self.player.dialog_en_cours = True
                        self.passage_mino = True

                if portal.origin_point == "alarme_declencheuse" \
                        and not self.player.dialog_en_cours and not self.player.start:

                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x, point.y, point.width, point.height)
                    if self.player.feet.colliderect(rect):
                        self.player.dialog_en_cours = True

                else:
                    point = self.get_object(portal.origin_point)
                    rect = pygame.Rect(point.x, point.y, point.width, point.height)
                    if self.player.feet.colliderect(rect):
                        copy_portal = portal
                        self.current_map = portal.target_world
                        if copy_portal.teleport_point == "epee_recup":
                            self.player.name = "player"
                        self.teleport_player(copy_portal.teleport_point)
        # collision
        for sprite in self.get_group().sprites():
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()
            if sprite.feet.collidelist(self.get_grass()) > -1:
                sprite.grass_sound(True)
            else:
                sprite.grass_sound(False)

    def check_player_monster_collisions_damage(self):
        """
        La méthode check_player_monster_collisions_damage permet de vérifier si le joueur et un monstre sont en
        collision pour pouvoir mettre des dégâts
        """
        for monster in self.get_monsters():
            if monster.distance is None:
                monster.distance = 100
            if monster.attack_radius < monster.distance:
                self.cooldown = 0
            if monster.feet.colliderect(self.player.rect) and self.cooldown >= 100:
                self.attack_monstre(monster.damage)
                self.animation = True
                self.player.first = True
                self.monstre = monster
            if self.player.attacking and self.player_cooldown >= 50:
                self.player.attacking = False
                if self.player.player_attack_radius >= monster.distance:
                    self.attack(monster)
                else:
                    self.attack(None)
                self.player.can_attack = False

    def attack_monstre(self, damage):
        """
        La méthode attack_monstre permet d’appliquer les dégâts au joueur
        """
        self.cooldown = 0
        if self.player.health > 0:
            self.player.health -= damage
            self.player.change_barre_de_vie(self.player.health)

        if self.player.health <= 0:
            self.player.change_barre_de_vie(self.player.health)
            if self.player.mort == 0:
                self.player.mort = 1

    def animation_monstres(self):
        """
        La méthode animation_montre permet d’animer les monstres
        """
        if self.animation:
            if self.compteur_monstre >= 40:
                self.compteur_monstre = 0
                self.animation = False
                self.monstre.stop_monstre()
            self.monstre.lance_animation()
            self.compteur_monstre += 1

    def check_mort_player(self):
        """
        La méthode check_mort_player vérifie constamment si le joueur est mort ou non
        """
        if self.compteurmort >= 360:
            self.compteurmort = 0
            self.player.mort = 2
        if self.player.mort == 1:
            self.player.morta(self.compteurmort)
            self.compteurmort += 2 * 4

    def attack(self, monster):
        """
        La méthode attack permet d’appliquer les dégâts aux monstres
        """
        self.player_cooldown = 0
        if monster is not None:
            if monster.health > 0:
                monster.health -= self.player.damage

    def cooldown_monstre(self):
        """
        La méthode cooldown_monstre impose un délai d’attaque aux monstres
        """
        if self.cooldown < 100:
            self.cooldown += 1

    def cooldown_player(self):
        """
        La méthode cooldown_player impose un délai d’attaque au joueur
        """
        if self.player_cooldown < 50:
            self.player_cooldown += 1

    def teleport_player(self, name):
        """
        Méthode pour le spawn du joueur et les tp
        """
        coord_joueur = self.sauvegarde.restoration_coord()
        map = self.sauvegarde.restoration_map()
        if self.player and (name == "player_debut" or name == "minotaure" or name == "boss_parle_tp"):
            return
        if name == "player":
            self.player.position[0] = coord_joueur[0]
            self.player.position[1] = coord_joueur[1]
            self.current_map = map

        else:
            point = self.get_object(name)
            self.player.position[0] = point.x
            self.player.position[1] = point.y
            self.sauvegarde.sauvegarde_player(self.player.position)
            self.sauvegarde.sauvegarde_map(self.current_map)

    def register_map(self, name, portals=None, npcs=None,
                     monsters=None):
        """
        La méthode register_map permet de charger les maps et les objets se trouvant sur cette dernière
        """
        if npcs is None:
            npcs = []
        if monsters is None:
            monsters = []
        if portals is None:
            portals = []
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        if "plaine" in name:
            map_layer.zoom = 1.5

        elif "maison" in name:
            map_layer.zoom = 3

        else:
            map_layer.zoom = 2

        # Définir une liste qui stock les rectangles de collisions
        walls = []
        grass = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            if obj.type == "grass":
                grass.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calque
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=8)
        group.add(self.player)

        # Récupérer tous les npcs pour les ajouter au groupe
        for npc in npcs:
            group.add(npc)

        # Récupérer tous les monstres pour les ajouter au groupe
        for monster in monsters:
            group.add(monster)

        # Créer un objet map
        self.maps[name] = Map(name, walls, grass, group, tmx_data,
                              portals,
                              npcs,  # lier avec la class Map au-dessus (on injecte la nouvelle carte dans le dico)
                              monsters)
    """
    L'ensemble des méthodes get_* permettent de récupérer les différents objects et emplacement sur la map
    """

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_grass(self):
        return self.get_map().grass

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def get_monsters(self):
        return self.get_map().monsters

    def teleport_npc(self):
        """
        La méthode teleport_npc permet de placer les pnjs et les monstres sur la carte
        """
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            monsters = map_data.monsters

            for npc in npcs:
                npc.load_point(map_data.tmx_data)
                npc.teleport_spawn()

            for monster in monsters:
                monster.load_point(map_data.tmx_data)
                monster.teleport_spawn()

    def draw(self):
        """
        La méthode draw permet de dessiner les différents éléments sur l’écran
        """
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        """
        La méthode update est une méthode qui s’actualise à chaque tick, permettant de vérifier
        plusieurs choses constamment
        """
        self.get_group().update()
        self.check_collisions()
        self.check_player_monster_collisions_damage()
        self.cooldown_monstre()
        self.cooldown_player()
        self.check_mort_player()
        self.animation_monstres()

        for npc in self.get_map().npcs:
            npc.move(self.player.start)
        for monster in self.get_map().monsters:
            monster.monster_update(self.player, self.oui)
            self.oui = False

    def changement_direction_npc(self, npc, cote):
        """
        La méthode changement_direction_npc permet de faire tourner les npc vers le joueur quand ce dernier leur parle
        """
        npc.changement_direct(cote)
