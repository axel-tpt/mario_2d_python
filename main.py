# ------ Import ------
import pygame
from random import randint
# --- fichier
from menu import Menu

# -----------------------------------------------------
# ----------------------- Main ------------------------
# -----------------------------------------------------
class Main:
    def __init__(self):
        # Initialisation
        pygame.init()
        self.mixer_init = True
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
        except pygame.error:
            print("Could not initialize mixer, continuing without sound.")
            self.mixer_init = False
        pygame.font.init()

        # Création fenêtre
        self.width = 900
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        icon = pygame.image.load("images/block/MysteryBlock.png")
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Super Mario Bros. NES")
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.time = 0

        # Menu principale
        self.menu = Menu(self.screen, self.width, self.height, self)
        self.actif = self.menu

    def loop(self):
        while not self.menu.done :
            self.time += 1
            self.actif.event()
            self.actif.update()
            self.actif.draw()

            pygame.display.flip()
            self.clock.tick(self.fps)

# ------ Start the game ------
main = Main()
main.loop() 
pygame.quit()