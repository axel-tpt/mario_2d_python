# ------ Import ------
import pygame
# --- fichier
from mario_2d.module.block import Brick

class Castle:
    def __init__(self, screen, game, x, y):
        # Info fenêtre
        self.screen = screen
        self.game = game

        img = pygame.image.load('images/end_level/castle.png').convert_alpha()
        self.img = pygame.transform.scale(img, (30*5, 30*4))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "castle"

    def update(self):
        pass

    def draw(self, cam):
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))
    
    def xDoor(self):
        return self.rect.x + 90

# ------ Poteau ------
class Poteau:
    def __init__(self, screen, game, x, y):
        # Info fenêtre
        self.screen = screen
        self.game = game
        self.type = "poteau"

        self.x, self.y = x, y
        self.barre = Barre(screen, x+10, y-30*6)
        self.drapeau = Drapeau(screen, x+20, y-30)
        self.base = Brick(screen, x, y)
        img_b = pygame.image.load('images/end_level/boule.png').convert_alpha()
        self.img_boule = pygame.transform.scale(img_b, (15, 15))

    def draw(self, cam):
        self.base.draw(cam)
        self.drapeau.draw(cam)
        self.barre.draw(cam)
        self.screen.blit(self.img_boule, (self.x+7.5 + cam, self.y-30*6-15))

class Barre:
    def __init__(self, screen, x, y):
        # Info fenêtre
        self.screen = screen

        img = pygame.image.load('images/end_level/tube.png').convert_alpha()
        self.img = pygame.transform.scale(img, (10, 30*6))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "barre"

    def draw(self, cam):
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))

class Drapeau:
    def __init__(self, screen, x, y):
        # Info fenêtre
        self.screen = screen

        img = pygame.image.load('images/end_level/drapeau.png').convert_alpha()
        self.img = pygame.transform.scale(img, (30, 20))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "drapeau"

    def draw(self, cam):
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))