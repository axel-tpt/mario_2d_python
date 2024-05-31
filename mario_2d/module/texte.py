# ------ Import ------
import pygame
# --- fichier
from mario_2d.module.json_reader import newValue

class Bouton :
    def __init__(self, screen, x, y, text, size = 50):
        self.screen = screen
        self.t = text
        self.x = x
        self.y = y
        self.size = size
        self.select = False

        self.font = pygame.font.Font("font/super-mario-bros-nes.ttf", self.size)
        self.text = self.font.render(self.t, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center = (self.x, self.y))

    def update(self, color):
        self.text = self.font.render(self.t, True, color)
        self.text_rect = self.text.get_rect(center = (self.x, self.y))

    def draw(self):
        if self.select:
            self.update((0, 0, 0))
        self.screen.blit(self.text, self.text_rect)

class OptionBouton :
    def __init__(self, screen, x, y, t, v):
        self.screen = screen
        self.x = x
        self.y = y
        self.t = t
        self.v = v
        self.default_v = v

        self.font = pygame.font.Font("font/super-mario-bros-nes.ttf", 50)
        self.color = (255, 255, 255)
        self.text = self.font.render(self.t+self.v, True, self.color)
        self.text_rect = self.text.get_rect(center = (self.x, self.y))
        self.state = "non"
        self.select = False

    def click(self, liste):
        ok = True
        for b in liste :
            if b.state == "select":
                ok = False
        if ok == True and self.state == "non" :
            self.state = "select"
            self.waiting()

    def waiting(self):
        self.v = "_"
        self.text = self.font.render(self.t+self.v, True, self.color)
        self.text_rect = self.text.get_rect(center = (self.x, self.y))

    def newValue(self, action, touche):
        v = newValue(action, touche)
        self.default_v, self.v = v, v
        self.state = "non"

    def update(self, color):
        self.color = color
        self.text = self.font.render(self.t+self.v, True, self.color)
        self.text_rect = self.text.get_rect(center = (self.x, self.y))

    def draw(self):
        if self.select:
            self.update((0, 0, 0))
        self.screen.blit(self.text, self.text_rect)

class Texte :
    def __init__(self, screen, x, y, text, size = 40):
        self.screen = screen
        self.t = text
        self.x = x
        self.y = y
        self.size = size

        self.font = pygame.font.Font("font/super-mario-bros-nes.ttf", self.size)
        self.text = self.font.render(self.t, True, (255, 255, 255))

    def draw(self, cam):
        self.screen.blit(self.text, self.text.get_rect(center = (self.x+cam, self.y)))

class TexteMenu :
    def __init__(self, screen, x, y, text, size = 40):
        self.screen = screen
        self.t = text
        self.x = x
        self.y = y
        self.size = size
        self.select = False
        self.state = "non"

        self.font = pygame.font.Font("font/super-mario-bros-nes.ttf", self.size)
        self.text = self.font.render(self.t, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center = (self.x, self.y))

    def update(self, color):
        self.text = self.font.render(self.t, True, color)
        self.text_rect = self.text.get_rect(center = (self.x, self.y))

    def draw(self):
        if self.select:
            self.update((0, 0, 0))
        self.screen.blit(self.text, self.text_rect)

class checkBox :
    def __init__(self, screen, x, y, size, state, color = (255, 255, 255)):
        self.screen = screen
        self.x, self.y = x, y
        self.size = size
        self.color = color
        self.state = state
        self.select = False

    def collision(self, x, y):
        if x >= self.x and x <= self.x+self.size:
            if y >= self.y and y <= self.y+self.size:
                return True
        return False

    def changeState(self):
        if self.state == 1:
            self.state = 0
        else:
            self.state = 1

    def update(self, color):
        self.color = color

    def draw(self):
        if self.select:
            self.update((0, 0, 0))
        if self.state == 1 :
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))
        else:
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size), 3)