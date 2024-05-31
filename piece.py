# ------ Import ------
import pygame

class Piece:
    def __init__(self, screen, x, y):
        self.screen = screen
        img = pygame.image.load("images/entité/piece.png").convert_alpha()
        self.img = pygame.transform.scale(img, (30, 30))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def left(self, speed):
        self.rect.x += speed

    def right(self, speed):
        self.rect.x += speed

    def draw(self, cam):
        self.screen.blit(self.img, (self.rect.x + cam, self.rect.y))
    
