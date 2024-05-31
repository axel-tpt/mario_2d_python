# ------ Import ------
import pygame
# --- fichier

class Tuyau(object):
    def __init__(self, screen, x, y):
        self.screen = screen
        img = pygame.image.load("images/block/pipe.png").convert_alpha()
        self.image = pygame.transform.scale(img, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = "tuyau"

    def draw(self, cam) :
        self.screen.blit(self.image, (self.rect.x + cam, self.rect.y))