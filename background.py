# ------ Import ------
import pygame
# --- fichier

class Background:
    def __init__(self, screen, w, h, game):
        # Info fenêtre
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.game = game

        img = pygame.image.load("images/background/BackgroundMarioSansLeSol.png")
        imgNuage = pygame.image.load("images/background/Nuage.png").convert_alpha()
        self.image = pygame.transform.scale(img, (900, 600))
        self.imageNuage = pygame.transform.scale(imgNuage, (960, 540))
        self.liste_x = []
        self.liste_x_Nuage = []
        # Ajoute les coordonées du fond dans la liste 
        for i in range(-1,self.game.worldSize+2):
            self.liste_x.append(i*900)
        # Ajoute les coordonées des nuages dans une autre liste 
        for j in range(-1,self.game.worldSize+2):
            self.liste_x_Nuage.append(j*900)

    def draw(self, cam) :
        # permet l'affichage du fond
        for x in self.liste_x :
            self.screen.blit(self.image, (x+cam*0.25, 0))
        # permet l'affichage des nuages
        for xN in self.liste_x_Nuage:
            self.screen.blit(self.imageNuage, (xN + cam*0.2, 0))