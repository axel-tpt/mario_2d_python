# ------ Import ------
import pygame
# --- fichier
from game import Game
from sound import Sound
from texte import *
from json_reader import *

class Menu :
    def __init__(self, screen, w, h, main):
        # Info fenêtre
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.main = main
        self.controle = getCommandes()

        # Paramètre jeu
        self.done = False
        self.music = Sound('Super Mario Bros Theme.wav', 0.05, True)
        self.music.state = getSoundState()[0]
        if self.music.state == 0:
            self.music.pause()
        self.volume = 1


        # Paramètres menu
        self.menu_actif = MainMenu(screen, w, h, self)
        # self.sound = Sound('Click.wav', 0.1)

        bg = pygame.image.load("images/background/BackgroundMario.png")
        mario = pygame.image.load("images/mario/BigMario.png").convert_alpha()
        self.mario = pygame.transform.scale(mario, (30, 60))
        self.bg = pygame.transform.scale(bg, (900, 720))

    def event(self):
        self.menu_actif.event()

    def update(self):
        self.menu_actif.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.mario, (30, 562))
        self.menu_actif.draw()

class MainMenu :
    def __init__(self, screen, w, h, menu):
        # Info fenêtre / menu
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.menu = menu
        self.optionMenu = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)

        # Paramètres menu
        self.logo = pygame.image.load("images/logo.png")
        self.logo_rect = self.logo.get_rect()
        self.label_button = ["JOUER", "OPTIONS", "QUITTER"]
        self.liste_bouton = []
        for i in range(len(self.label_button)) :
            self.liste_bouton.append(Bouton(self.screen, self.DISPLAY_W//2, self.DISPLAY_H//2 - 30 + 100*i, self.label_button[i]))
        self.bouton_info = Bouton(self.screen, 160, 26, "REGLES/ASTUCES", 20)
        self.b_select = None

        # manette
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[-1].init()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Ferme le jeu en appuyant sur Esc
                    self.menu.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if self.liste_bouton[0].text_rect.collidepoint(x, y): # Bouton JOUER
                        Sound('Click.wav', 0.05, False)
                        self.play()
                    if self.liste_bouton[1].text_rect.collidepoint(x, y): # Bouton OPTION
                        Sound('Click.wav', 0.05, False)
                        self.menu.menu_actif = self.optionMenu
                    if self.liste_bouton[2].text_rect.collidepoint(x, y): # Bouton Quitter
                        Sound('Click.wav', 0.05, False)
                        self.menu.done = True
                    if self.bouton_info.text_rect.collidepoint(x, y): # Bouton REGLES/ASTUCE
                        Sound('Click.wav', 0.05, False)
                        self.menu.menu_actif = Tips(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if self.b_select == 0: # Bouton JOUER
                        Sound('Click.wav', 0.05, False)
                        self.play()
                    if self.b_select == 1: # Bouton OPTION
                        Sound('Click.wav', 0.05, False)
                        self.menu.menu_actif = self.optionMenu
                    if self.b_select == 2: # Bouton Quitter
                        Sound('Click.wav', 0.05, False)
                        self.menu.done = True
                    if self.b_select == -1: # Bouton REGLES/ASTUCE
                        Sound('Click.wav', 0.05, False)
                        self.menu.menu_actif = Tips(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)
            elif event.type == pygame.JOYHATMOTION:
                for i in range(len(self.liste_bouton)):
                    if self.liste_bouton[i].select:
                        self.b_select = i
                if self.b_select == None:
                    if event.value[1] == 1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                    if event.value[1] == -1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                else:
                    if event.value[1] == 1:
                        if self.b_select > 0:
                            self.b_select -= 1
                            self.liste_bouton[self.b_select+1].select = False
                            self.liste_bouton[self.b_select].select = True
                    if event.value[1] == -1:
                        if self.b_select < len(self.liste_bouton)-1:
                            self.b_select += 1
                            self.liste_bouton[self.b_select-1].select = False
                            self.liste_bouton[self.b_select].select = True


    # Changement de couleur des boutons à cause de la souris
    def update(self):
        for bouton in self.liste_bouton :
            if bouton.text_rect.collidepoint(pygame.mouse.get_pos()) :
                bouton.update((0, 0, 0))
            else :
                bouton.update((255, 255, 255))
        if self.bouton_info.text_rect.collidepoint(pygame.mouse.get_pos()) :
            self.bouton_info.update((0, 0, 0))
        else :
            self.bouton_info.update((255, 255, 255))
    
    def draw(self):
        self.logo_rect.center = (self.DISPLAY_W//2, 150)
        self.screen.blit(self.logo, self.logo_rect)
        for bouton in self.liste_bouton :
            bouton.draw()
        self.bouton_info.draw()

    def play(self):
        self.game = Game(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.menu)
        self.menu.main.actif = self.game

class OptionMenu:
    def __init__(self, screen, w, h, mainMenu):
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.mainMenu = mainMenu

        self.done = False
        self.play = False
        self.b_select = None

        self.label_button = ["COMMANDES", "AUDIO", "RETOUR"]
        self.liste_bouton = []
        for i in range(len(self.label_button)) :
            self.liste_bouton.append(Bouton(self.screen, self.DISPLAY_W//2, 250 + 100*i, self.label_button[i]))

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Reviens au menu principal en appuyant sur Esc
                    Sound('Click.wav', 0.05, False)
                    self.mainMenu.menu.menu_actif = MainMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.mainMenu.menu)
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if self.liste_bouton[0].text_rect.collidepoint(x, y): # Bouton COMMANDE
                        Sound('Click.wav', 0.1)
                        self.mainMenu.menu.menu_actif = CommandesOptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)
                    if self.liste_bouton[1].text_rect.collidepoint(x, y): # Bouton AUDIO
                        Sound('Click.wav', 0.1)
                        self.mainMenu.menu.menu_actif = AudioOptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)
                    if self.liste_bouton[len(self.liste_bouton)-1].text_rect.collidepoint(x, y): # Bouton RETOUR
                        Sound('Click.wav', 0.1)
                        self.mainMenu.menu.menu_actif = MainMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.mainMenu.menu)

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if self.b_select == 0: # Bouton JOUER
                        Sound('Click.wav', 0.05, False)
                        self.mainMenu.menu.menu_actif = CommandesOptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)
                    if self.b_select == 1: # Bouton OPTION
                        Sound('Click.wav', 0.05, False)
                        self.mainMenu.menu.menu_actif = AudioOptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self)
                    if self.b_select == 2: # Bouton Quitter
                        Sound('Click.wav', 0.05, False)
                        self.mainMenu.menu.menu_actif = MainMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.mainMenu.menu)
                if event.button == 1:
                    Sound('Click.wav', 0.05, False)
                    self.mainMenu.menu.menu_actif = MainMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.mainMenu.menu)
            elif event.type == pygame.JOYHATMOTION:
                for i in range(len(self.liste_bouton)):
                    if self.liste_bouton[i].select:
                        self.b_select = i
                if self.b_select == None:
                    if event.value[1] == 1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                    if event.value[1] == -1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                else:
                    if event.value[1] == 1:
                        if self.b_select > 0:
                            self.b_select -= 1
                            self.liste_bouton[self.b_select+1].select = False
                            self.liste_bouton[self.b_select].select = True
                    if event.value[1] == -1:
                        if self.b_select < len(self.liste_bouton)-1:
                            self.b_select += 1
                            self.liste_bouton[self.b_select-1].select = False
                            self.liste_bouton[self.b_select].select = True
    # Changement de couleur des boutons à cause de la souris
    def update(self):
        for bouton in self.liste_bouton :
            if bouton.text_rect.collidepoint(pygame.mouse.get_pos()) :
                bouton.update((0, 0, 0))
            else :
                bouton.update((255, 255, 255))

    def draw(self):
        for bouton in self.liste_bouton :
            bouton.draw()

class CommandesOptionMenu:
    def __init__(self, screen, w, h, optionMenu):
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.optionMenu = optionMenu
        self.b_select = -1

        self.label_button = [
            "GAUCHE:",
            "DROITE:",
            "SAUT:" ,
            "RETOUR"
        ]
        self.liste_touches = [
            pygame.key.name(self.optionMenu.mainMenu.menu.controle["left"]),
            pygame.key.name(self.optionMenu.mainMenu.menu.controle["right"]),
            pygame.key.name(self.optionMenu.mainMenu.menu.controle["jump"]),
            ""
        ]
        # Crée les boutons
        self.liste_bouton = []
        for i in range(len(self.label_button)) :
            self.liste_bouton.append(OptionBouton(self.screen, self.DISPLAY_W//2, 200 + 100*i, self.label_button[i], self.liste_touches[i]))

    def event(self):
        for event in pygame.event.get():
            touche = ["left", "right", "jump", "cam"]
            if event.type == pygame.KEYDOWN:
                select = False
                for i in range(len(self.liste_bouton)-1):
                    if self.liste_bouton[i].state == "select":
                        select = True
                        if event.key == pygame.K_ESCAPE:
                            self.liste_bouton[i].v = self.liste_bouton[i].default_v
                            self.liste_bouton[i].state = "non"
                        else :
                            self.liste_bouton[i].newValue(touche[i], pygame.key.name(event.key))
                            self.optionMenu.mainMenu.menu.controle[touche[i]] = pygame.key.key_code(newValue(touche[i], pygame.key.name(event.key)))
                if not select and event.key == pygame.K_ESCAPE : # Reviens au menu principal en appuyant sur Esc
                    Sound('Click.wav', 0.05, False)
                    self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)

            elif event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if self.liste_bouton[0].text_rect.collidepoint(x, y): # Bouton left
                        Sound('Click.wav', 0.1)
                        self.liste_bouton[0].click(self.liste_bouton)
                    if self.liste_bouton[1].text_rect.collidepoint(x, y): # Bouton right
                        Sound('Click.wav', 0.1)
                        self.liste_bouton[1].click(self.liste_bouton)
                    if self.liste_bouton[2].text_rect.collidepoint(x, y): # Bouton jump
                        Sound('Click.wav', 0.1)
                        self.liste_bouton[2].click(self.liste_bouton)
                    if self.liste_bouton[len(self.liste_bouton)-1].text_rect.collidepoint(x, y):
                        Sound('Click.wav', 0.1)
                        self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)
            
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if self.b_select == 0:
                        Sound('Click.wav', 0.1)
                        self.liste_bouton[0].click(self.liste_bouton)
                    if self.b_select == 1:
                        Sound('Click.wav', 0.05, False)
                        self.liste_bouton[1].click(self.liste_bouton)
                    if self.b_select == 2:
                        Sound('Click.wav', 0.05, False)
                        self.liste_bouton[1].click(self.liste_bouton)
                    if self.b_select == 3:
                        Sound('Click.wav', 0.05, False)
                        self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)
                if event.button == 1:
                    print(self.b_select)
                    if self.liste_bouton[self.b_select].state == "select":
                        self.liste_bouton[self.b_select].v = self.liste_bouton[self.b_select].default_v
                        self.liste_bouton[self.b_select].state = "non"
                    else:
                        Sound('Click.wav', 0.05, False)
                        self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)
            elif event.type == pygame.JOYHATMOTION:
                for i in range(len(self.liste_bouton)):
                    if self.liste_bouton[i].select:
                        self.b_select = i
                if self.b_select == None:
                    if event.value[1] == 1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                    if event.value[1] == -1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                else:
                    if event.value[1] == 1:
                        if self.b_select > 0:
                            self.b_select -= 1
                            self.liste_bouton[self.b_select+1].select = False
                            self.liste_bouton[self.b_select].select = True
                    if event.value[1] == -1:
                        if self.b_select < len(self.liste_bouton)-1:
                            self.b_select += 1
                            self.liste_bouton[self.b_select-1].select = False
                            self.liste_bouton[self.b_select].select = True
    
    # Changement de couleur des boutons à cause de la souris
    def update(self):
        for bouton in self.liste_bouton :
            if bouton.text_rect.collidepoint(pygame.mouse.get_pos()) :
                bouton.update((0, 0, 0))
            else :
                bouton.update((255, 255, 255))

    def draw(self):
        for bouton in self.liste_bouton :
            bouton.draw()

class AudioOptionMenu:
    def __init__(self, screen, w, h, optionMenu):
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.optionMenu = optionMenu
        self.soundState = getSoundState()
        self.label_button = [
            "MUSIQUE:",
            "EFFETS:",
            "RETOUR"
        ]
        self.b_select = None

        self.liste_bouton = []
        for i in range(len(self.label_button)) :
            self.liste_bouton.append(TexteMenu(screen, w//2, 250+100*i, self.label_button[i], 50))
        self.liste_checkBox = []
        for i in range(2):
            x = w//2 + self.liste_bouton[i].text_rect.width//2 + 15
            self.liste_checkBox.append(checkBox(screen, x, 225+100*i, 50, self.soundState[i]))

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    Sound('Click.wav', 0.05, False)
                    self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)

            elif event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    # bouton musique du jeu
                    if self.liste_bouton[0].text_rect.collidepoint(x, y) or self.liste_checkBox[0].collision(x, y):
                        self.optionMenu.mainMenu.menu.music.changeState()
                        self.liste_checkBox[0].changeState()
                        newSoundState("music", self.liste_checkBox[0].state)
                        Sound('Click.wav', 0.1)

                    # bouton effets sonores
                    if self.liste_bouton[1].text_rect.collidepoint(x, y) or self.liste_checkBox[1].collision(x, y):
                        Sound('Click.wav', 0.1)
                        self.liste_checkBox[1].changeState()
                        newSoundState("effects", self.liste_checkBox[1].state)
                        self.optionMenu.mainMenu.menu.volume = self.liste_checkBox[1].state
                    # bouton revenir au menu option
                    if self.liste_bouton[len(self.liste_bouton)-1].text_rect.collidepoint(x, y):
                        Sound('Click.wav', 0.1)
                        self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)
           
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if self.b_select == 0:
                        self.optionMenu.mainMenu.menu.music.changeState()
                        self.liste_checkBox[0].changeState()
                        newSoundState("music", self.liste_checkBox[0].state)
                        Sound('Click.wav', 0.1)
                    if self.b_select == 1:
                        Sound('Click.wav', 0.1)
                        self.liste_checkBox[1].changeState()
                        newSoundState("effects", self.liste_checkBox[1].state)
                        self.optionMenu.mainMenu.menu.volume = self.liste_checkBox[1].state
                    if self.b_select == 2:
                        Sound('Click.wav', 0.1)
                        self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)
                if event.button == 1:
                    Sound('Click.wav', 0.1)
                    self.optionMenu.mainMenu.menu.menu_actif = OptionMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.optionMenu.mainMenu)

            elif event.type == pygame.JOYHATMOTION:
                for i in range(len(self.liste_bouton)):
                    if self.liste_bouton[i].select:
                        self.b_select = i
                if self.b_select == None:
                    if event.value[1] == 1 or event.value[1] == -1:
                        self.b_select = 0
                        self.liste_bouton[0].select = True
                        self.liste_checkBox[0].select = True
                else:
                    if event.value[1] == 1:
                        if self.b_select > 0:
                            self.b_select -= 1
                            self.liste_bouton[self.b_select+1].select = False
                            self.liste_bouton[self.b_select].select = True
                        if self.b_select < len(self.liste_checkBox)-1:
                            self.liste_checkBox[self.b_select+1].select = False
                            self.liste_checkBox[self.b_select].select = True
                    if event.value[1] == -1:
                        if self.b_select < len(self.liste_bouton)-1:
                            self.b_select += 1
                            self.liste_bouton[self.b_select-1].select = False
                            self.liste_bouton[self.b_select].select = True
                        if self.b_select < len(self.liste_checkBox):
                            self.liste_checkBox[self.b_select-1].select = False
                            self.liste_checkBox[self.b_select].select = True

    # Changement de couleur des boutons à cause de la souris
    def update(self):
        for i in range(2):
            x, y = pygame.mouse.get_pos()
            if self.liste_bouton[i].text_rect.collidepoint(x, y) or self.liste_checkBox[i].collision(x, y):
                self.liste_bouton[i].update((0, 0, 0))
                self.liste_checkBox[i].update((0, 0, 0))
            else :
                self.liste_bouton[i].update((255, 255, 255))
                self.liste_checkBox[i].update((255, 255, 255))

    def draw(self):
        for bouton in self.liste_bouton :
            bouton.draw()
        for c in self.liste_checkBox:
            c.draw()

class Tips:
    def __init__(self, screen, w, h, mainMenu):
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.mainMenu = mainMenu

        self.bouton_retour = Bouton(self.screen, self.DISPLAY_W//2, 565, "RETOUR", 40)
        self.img = pygame.image.load("images/regle.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.img.get_rect().width+15, self.img.get_rect().height+25))
        self.img_rect = self.img.get_rect()
        self.img_rect.topleft = (self.DISPLAY_W//2-270, 40)

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Sound('Click.wav', 0.05, False)
                    self.mainMenu.menu.menu_actif = MainMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.mainMenu.menu)
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    if self.bouton_retour.text_rect.collidepoint(pygame.mouse.get_pos()):
                        Sound('Click.wav', 0.05, False)
                        self.mainMenu.menu.menu_actif = MainMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self.mainMenu.menu)
    
    # Changement de couleur du bouton à cause de la souris
    def update(self):
        if self.bouton_retour.text_rect.collidepoint(pygame.mouse.get_pos()) :
            self.bouton_retour.update((0, 0, 0))
        else :
            self.bouton_retour.update((255, 255, 255))

    def draw(self):
        self.bouton_retour.draw()
        self.screen.blit(self.img, self.img_rect)
        