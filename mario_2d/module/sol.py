# ------ Import ------
import pygame
# --- fichier

class Sol(object):
    def __init__(self, screen, w, h, x, y):
        # mesure écran
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h

        self.x = x
        self.y = y
        self.height = (self.DISPLAY_H - self.y)//30

        # création sol
        self.l_block = [None for i in range(self.height)]
        for Y in range(self.height):
            self.l_block[Y] = Block(screen, self.x, self.y + 30 * Y)

    def draw(self, cam, borne_gauche, borne_droite):
        for b in self.l_block :
            if borne_gauche < b.rect.x and borne_droite > b.rect.x :
                b.draw(cam)

class Block(object):
    def __init__(self, screen, x, y):
        self.screen = screen
        
        img = pygame.image.load('images/block/GroundBlock.png').convert_alpha()
        self.img = pygame.transform.scale(img, (30, 30))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, cam):
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))
        #pygame.draw.rect(self.screen,(88, 41, 0), (self.x, self.y, 30, 30))