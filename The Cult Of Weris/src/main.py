import pygame
from game import Game
from sound import Sound

pygame.init()
pygame.mouse.set_visible(False)  # Rendre le pointeur de la souris invisible

if __name__ == "__main__":
    pygame.init()
    musique = Sound()
    musique.ambiance_musique()
    game = Game()
    game.run()
