# ------ Import ------
import pygame
# --- fichier
from timer import Timer

class Point:
    def __init__(self, screen, score, x, y):
        pygame.font.init()
        self.screen = screen
        self.x = x
        self.y = y
        self.timer = Timer(60)
        self.timer.start()

        self.display = True
        self.font = pygame.font.Font("font/super-mario-bros-nes.ttf", 15)
        self.t = "+" + str(score)
        self.text = self.font.render(self.t, True, (255, 255, 255))

    def update(self):
        self.timer.update()

    def draw(self, cam):
        if not self.timer.done() :
            self.text_rect = self.text.get_rect(bottomright = (self.x + cam, self.y))
            self.screen.blit(self.text, self.text_rect)
        else :
            self.display = False