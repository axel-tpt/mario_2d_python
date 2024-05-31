# ------ Import ------
import pygame
# --- fichier
from timer import Timer

class Goomba:
    def __init__(self, screen, game, x, y):
        # Info fenêtre
        self.screen = screen
        self.game = game

        # paramètre image
        img = pygame.image.load('images/entité/Goomba.png').convert_alpha()
        self.img_right = pygame.transform.scale(img, (30, 30))
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.direction = 2
        if self.direction > 0:
            self.img = self.img_right
        else :
            self.img = self.img_left
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0

    def update(self):
        self.dx = 0
        self.dy = 0
        self.dx += self.direction

        # Simulation de la gravité
        self.speed += 1
        if self.speed > 10:
            self.speed = 10
        self.dy += self.speed

        self.collision_sol() # contacte avec le sol
        self.collision_decor() # contacte avec le décor
        self.collision_mob()
        self.collision_mario()

        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, cam) :
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))

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
                        if self.img == self.img_left :
                            self.img = self.img_right
                    if (block.rect.x + block.rect.width//2) > self.rect.x :
                        self.dx = block.rect.left - self.rect.right
                        self.direction = -self.direction
                        if self.img == self.img_right :
                            self.img = self.img_left

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
                    if self.img == self.img_left :
                        self.img = self.img_right
                if (elt.rect.x + elt.rect.width//2) > self.rect.x :
                    self.dx = elt.rect.left - self.rect.right
                    self.direction = -self.direction
                    if self.img == self.img_right :
                        self.img = self.img_left

    def collision_mob(self):
        for mob in self.game.liste_mob :
            if self != mob :
                if mob.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    if (mob.rect.x + mob.rect.width//2) < self.rect.x :
                        self.dx = mob.rect.right - self.rect.left
                        self.direction = -self.direction
                        if self.img == self.img_left :
                            self.img = self.img_right
                    if (mob.rect.x + mob.rect.width//2) > self.rect.x :
                        self.dx = mob.rect.left - self.rect.right
                        self.direction = -self.direction
                        if self.img == self.img_right :
                            self.img = self.img_left

    def collision_mario(self):
        if self.game.mario.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
            if self.game.mario.size == 1 :
                self.game.mario.hitDelay.start()
                self.game.mario.flashAnim()
                self.game.mario.changeSize()
                self.direction = -self.direction
            if self.game.mario.size == 0 and self.game.mario.hitDelay.done():
                self.game.marioDead()