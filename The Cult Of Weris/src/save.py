import re


class Sauvegarde:

    def __init__(self):
        self.fichier = "../src/save.txt"

    def sauvegarde_player(self, pos):
        """
        La méthode sauvegarde_player permet d’enregistrer les coordonnées x et y du joueur
        """
        with open(self.fichier, "r+") as f:  # On ouvre le fichier en monde lecture + écriture
            file = f.read()
            file = re.sub("PositionJoueur=[^\n]*",  # Le [^\n]* permet de récupérer tous les caractères
                          # qui se trouvent après le = qui ne sont pas des sauts de lignes
                          f"PositionJoueur={pos}", file)
            f.seek(0)
            f.write(file)
            f.truncate()  # Permet de redimensionner le fichier texte à la taille de ce qu’il y a dedans

    def sauvegarde_cote(self, cote):
        """
        La méthode sauvegarde_cote permet de sauvegarder le côté du joueur
        """
        with open(self.fichier, "r+") as f:
            file = f.read()
            file = re.sub("ImageCote=[^\n]*", f"ImageCote={cote}", file)
            f.write(file)
            f.seek(0)
            f.write(file)
            f.truncate()

    def sauvegarde_map(self, map):
        """
        La méthode sauvegarde_map permet d'enregister la map sur laquelle se trouve le joueur
        """
        with open(self.fichier, "r+") as f:
            file = f.read()
            file = re.sub("MapJoueur=[^\n]*", f"MapJoueur={map}", file)
            f.seek(0)
            f.write(file)
            f.truncate()

    def sauvegarde_image(self, image):
        """
        La méthode sauvegarde_image permet de sauvegarder l’image du joueur (avec ou sans armure)
        """
        with open(self.fichier, "r+") as f:
            file = f.read()
            file = re.sub("Image=[^\n]*", f"Image={image}", file)
            f.seek(0)
            f.write(file)
            f.truncate()

    def restoration_coord(self):
        """
        La méthode restoration_coord permet de récupérer les coordonnées du joueur
        """
        with open(self.fichier, "r") as f:
            contenu = f.readlines()
            coord = contenu[0].split('=')
            coord_joueur = coord[1].split(",")
            coord_joueur[0] = coord_joueur[0].replace('[', "")
            coord_joueur[1] = coord_joueur[1].replace(']', "")
            coord_joueur[1] = coord_joueur[1].replace(' ', "")
            coord_joueur[0], coord_joueur[1] = float(coord_joueur[0]), float(coord_joueur[1])
            return coord_joueur

    def restoration_cote(self):
        """
        La méthode restoration_cote permet de récupérer le côté du joueur
        """
        with open(self.fichier, "r") as f:
            contenu = f.readlines()
            image = contenu[3].split('=')
            cote_joueur = image[1]
            return cote_joueur

    def restoration_map(self):
        """
        La méthode restoration_map permet de récupérer la map du joueur
        """
        with open(self.fichier, "r") as f:
            contenu = f.readlines()
            map = contenu[1].split('=')[1][:-1]
            return map

    def restoration_image(self):
        """
        La méthode restoration_image permet de récupérer l’image du joueur
        """
        with open(self.fichier, "r") as f:
            contenu = f.readlines()
            image = contenu[2].split('=')
            image_joueur = image[1][:-1]

            return image_joueur
