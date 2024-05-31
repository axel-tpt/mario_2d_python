# ------ Import ------
import pygame
# --- fichier
from random import randint

class superChampignon(object):
    def __init__(self, screen, game, x, y):
        # parametre fenetre
        self.screen = screen
        self.game = game

        # parametre image
        img = pygame.image.load('images/entité/SuperChampi.png').convert_alpha()
        self.img_right = pygame.transform.scale(img, (20, 20))
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.setDirection()
        self.rect = self.img_actif.get_rect()
        self.rect.x = x
        self.rect.y = y + 10

        self.speed = -5

    def setDirection(self):
        self.direction = 2
        if randint(0, 1) == 0 :
            self.direction = -self.direction
            self.img_actif = self.img_left
        else :
            self.img_actif = self.img_right

    def update(self):
        self.dy = 0
        self.dx = 0

        self.dx += self.direction

        # Simulation de la gravité
        self.speed += 1
        if self.speed > 10:
            self.speed = 10
        self.dy += self.speed

        self.collision_sol() # contacte avec le sol
        self.collision_decor() # contacte avec le décor

        self.rect.y += self.dy
        self.rect.x += self.dx

    def collision_sol(self):
        for col in self.game.sol :
            for block in col.l_block :
                if block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.speed > 0:
                        self.speed = 0
                        self.dy = block.rect.top - self.rect.bottom
                        self.jumped = True
                        
                if block.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    if (block.rect.x + block.rect.width//2) < self.rect.x :
                        self.dx = block.rect.right - self.rect.left
                        self.direction = -self.direction
                        if self.img_actif == self.img_left :
                            self.img_actif = self.img_right
                    if (block.rect.x + block.rect.width//2) > self.rect.x :
                        self.dx = block.rect.left - self.rect.right
                        self.direction = -self.direction
                        if self.img_actif == self.img_right :
                            self.img_actif = self.img_left

    def collision_decor(self):
        for elt in self.game.decor :
            if elt.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.speed > 0 :
                    self.dy = elt.rect.top - self.rect.bottom
                    self.speed = 0
            if elt.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                if (elt.rect.x + elt.rect.width//2) < self.rect.x :
                    self.dx = elt.rect.right - self.rect.left
                    self.direction = -self.direction
                    if self.img_actif == self.img_left :
                        self.img_actif = self.img_right
                if (elt.rect.x + elt.rect.width//2) > self.rect.x :
                    self.dx = elt.rect.left - self.rect.right
                    self.direction = -self.direction
                    if self.img_actif == self.img_right :
                        self.img_actif = self.img_left

    def draw(self, cam):
        self.screen.blit(self.img_actif, (self.rect.x + cam, self.rect.y))