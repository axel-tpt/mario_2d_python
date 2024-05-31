# ------ Import ------
import pygame
# --- fichier
from mario_2d.module.sound import Sound
from mario_2d.module.background import Background
from mario_2d.module.sol import Sol
from mario_2d.module.mario import Mario
from mario_2d.module.power_up import *

class Brick:
    def __init__(self, screen, x, y):
        self.screen = screen

        img = pygame.image.load('images/block/BrickBlock.png').convert_alpha()
        self.img = pygame.transform.scale(img, (30, 30))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "basic"

    def draw(self, cam) :
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))

class MysteryBlock:
    def __init__(self, screen, game, x, y, main):
        self.screen = screen
        self.game = game
        self.main = main

        img = pygame.image.load('images/block/MysteryBlock.png').convert_alpha()
        img_empty = pygame.image.load('images/block/EmptyBlock.png').convert_alpha()
        self.img_empty = pygame.transform.scale(img_empty, (30, 30))
        self.img = pygame.transform.scale(img, (30, 30))
        self.img_actif = self.img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "mystery"
        self.empty = False

    def draw(self, cam) :
        self.screen.blit(self.img_actif, (self.rect.x + cam, self.rect.y))
        
    def drop(self):
        if not self.empty :
            self.img_actif = self.img_empty
            Sound(self.main, 'Power Up Appears.wav', 0.05, False)
            self.game.liste_pu.append(superChampignon(self.screen, self.game, self.rect.x, self.rect.y - 30))


class Stairs:
    def __init__(self, screen, x, y):
        self.screen = screen

        img = pygame.image.load('images/block/StairsBlock.png').convert_alpha()
        self.img = pygame.transform.scale(img, (30, 30))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "Stairs"

    def draw(self, cam) :
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))