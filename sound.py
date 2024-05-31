# ------ Import ------
import pygame

class Sound(object):
    def __init__(self, main, file, volume, loop=False):
        self.main = main
        if self.main.mixer_init:
            self.audio = pygame.mixer.Sound("musics/"+file)
            self.audio.set_volume(volume)
            self.state = 1
            if loop :
                self.audio.play(-1)
            else :
                self.audio.play()

    def pause(self):
        if self.main.mixer_init:
            pygame.mixer.pause()

    def unpause(self):
        if self.main.mixer_init:
            pygame.mixer.unpause()

    def changeState(self):
        if self.main.mixer_init:
            if self.state == 1:
                pygame.mixer.pause()
                self.state = 0
            else:
                pygame.mixer.unpause()
                self.state = 1