# ------ Import ------
import pygame
# --- fichier
from world_builder import World
from background import Background
from sol import Sol
from mario import Mario
from block import *
from texte import Bouton, Texte
from point import Point
from json_reader import *

class Game:
    def __init__(self, screen, w, h, menu, main):
        # Info fenêtre
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.menu = menu
        self.controle = self.menu.controle
        self.main = main

        # Création monde
        self.worldSize = 3
        world = World(screen, self, self.worldSize, self.main)
        world.readCSV()
        self.liste_mob, self.liste_pu, self.liste_piece, self.decor, self.sol, self.end_level = world.content() # récupère les éléments du csv pour le jeu
        self.l_controle = [ # liste des controles en jeu
            Texte(screen, w//2, 170, "Gauche:" + pygame.key.name(self.controle["left"])),
            Texte(screen, w//2, 240, "Droite:" + pygame.key.name(self.controle["right"])),
            Texte(screen, w//2, 310, "Saut:" + pygame.key.name(self.controle["jump"]))
        ]
        self.warning = Texte(screen, 130, 450, "NON! A DROITE! ->", 15)

        # Initialisation acteurs
        self.bg = Background(screen, w, h, self)
        self.mario = Mario(screen, w, h, self, self.main)
        self.dist_affichage = 480
        self.borne_gauche = self.mario.rect.x - self.dist_affichage
        self.borne_droite = self.mario.rect.x + self.dist_affichage

        # Paramètre jeu
        self.pauseMenu = PauseMenu(screen, w, h, self)
        self.ATH = ATH(screen, self, w, h)
        self.play = True
        self.end_game = False
        self.cam = 1
        self.score = 0
        self.nb_piece = 0
        self.end_anim = False
        self.draw_mario = True
        self.point = []

        # manette
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            self.joysticks.append(pygame.joystick.Joystick(i))
            self.joysticks[-1].init()

    def event(self):
        if self.play and not self.end_anim:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.end_game:
                            Sound(self.main, 'Pause.wav', 0.05*self.menu.volume, False)
                            self.play = False
                    if event.key == self.controle["jump"]:
                        self.mario.jump()
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        if event.value > 0.3:
                            self.mario.rect.x += 3
                            self.mario.right()
                        if event.value < -0.3:
                            self.mario.rect.x -= 3
                            self.mario.left()
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        self.mario.jump()
                    if event.button == 7:
                        if not self.end_game:
                            Sound(self.main, 'Pause.wav', 0.05*self.menu.volume, False)
                            self.play = False

        if not self.play and not self.end_anim and not self.end_game:
            self.pauseMenu.event()
        if self.end_game:
            self.endMenu.event()

    def update(self):
        if self.play and not self.end_anim:
            if not self.mario.anim:
                self.ATH.update()
                for mob in self.liste_mob :
                    if self.borne_gauche < mob.rect.x and self.borne_droite > mob.rect.x :
                        mob.update()
                for pu in self.liste_pu :
                    pu.update()
                for p in self.point :
                    p.update()
            self.mario.update()
            self.mario.coordonnee()

        if not self.play and not self.end_anim and not self.end_game:
            self.pauseMenu.update()
        if self.end_anim:
            self.endGame()
        if self.end_game:
            self.endMenu.update()

    def draw(self):
        pygame.draw.rect(self.screen, (195, 84, 28), (0, 0, self.DISPLAY_W, self.DISPLAY_H)) # affiche le fond marron
        self.bg.draw(self.cam)
        # Affiche les mobs
        for mob in self.liste_mob :
            if self.borne_gauche < mob.rect.x and self.borne_droite > mob.rect.x :
                mob.draw(self.cam)
        # Affiche les power up
        for pu in self.liste_pu :
            pu.draw(self.cam)
        # Affiche les pièces
        for piece in self.liste_piece :
            if self.borne_gauche < piece.rect.x and self.borne_droite > piece.rect.x :
                piece.draw(self.cam)
        # Affiche les éléments du décor
        for elt in self.decor :
            if self.borne_gauche < elt.rect.x and self.borne_droite > elt.rect.x :
                elt.draw(self.cam)
                if elt.type == "castle" :
                    elt.hitboxDoor(self.cam).draw(self.screen)
        
        for elt in self.end_level :
            elt.draw(self.cam)
        for sol in self.sol :
            sol.draw(self.cam, self.borne_gauche, self.borne_droite)
        if self.draw_mario :
            self.mario.draw(self.cam)

        # Affiche les points gagnés en tuant les goombas
        for p in self.point:
            p.draw(self.cam)
            if not p.display :
                self.point.remove(p)
        
        # affichage dépendant de la pause
        if not self.play and not self.end_anim and not self.end_game:
            self.pauseMenu.draw()
        if not self.end_game and self.play:
            self.ATH.draw()
            for t in self.l_controle:
                t.draw(self.cam)
                if self.mario.rect.x <= 150:
                    self.warning.draw(self.cam)
        # affichage en fonction de si la partie est terminée
        if self.end_game:
            self.endMenu.draw()
        if not self.end_game:
            self.ATH.draw()

    def endGame(self):
        self.play = False
        self.marioInCastle = False
        # ------ déplacement ------
        if self.mario.poteau_anim : # mario descend le poteau 
            self.animPoteau()
        if not self.mario.poteau_anim : # mario va vers le château
            dx = 3
            for elt in self.end_level :
                if elt.type == "castle":
                    if elt.xDoor() <= self.mario.rect.x + self.mario.rect.width :
                        if elt.rect.x + elt.rect.width >= self.mario.rect.x + dx :
                            self.marioInCastle = True
                            self.draw_mario = False
                            dx = 0
            self.mario.rect.x += dx
        
            self.mario.speed += 1
            if self.mario.speed > 10:
                self.mario.speed = 10
                
            self.mario.dy += self.mario.speed
        self.mario.rect.y += self.mario.dy
        self.mario.collision_sol()

        # ------ Score ------
        if (self.ATH.duration - self.ATH.time_w) != 0:
            self.ATH.time_w += 1
            self.score += 20
        if self.nb_piece != 0 and (self.ATH.duration - self.ATH.time_w) == 0:
            if self.menu.main.time % 5 == 0 :
                self.nb_piece -= 1
                self.score += 100
        if self.nb_piece == 0 and (self.ATH.duration - self.ATH.time_w) == 0 and self.marioInCastle:
            if self.score > getBestScore():
                newBestScore(self.score)
            self.endMenu = EndMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self, self.main)
            self.end_anim = False
            self.end_game = True
            self.menu.music.changeState()
            self.menu.music.changeState()
        
    def animPoteau(self):
        self.mario.dy = 3
        for elt in self.end_level :
            if elt.type == "poteau" :
                if elt.drapeau.rect.top >= 390-3 : # fait monter le drapeau
                    elt.drapeau.rect.y -= 3
                if elt.base.rect.colliderect(self.mario.rect.x, self.mario.rect.y, self.mario.rect.width, self.mario.rect.height):
                    self.mario.poteau_anim = False
                    if self.mario.size == 0:
                        self.mario.img_actif = self.mario.img_0_right
                    else:
                        self.mario.img_actif = self.mario.img_1_right

    def marioDead(self):
        self.draw_mario = False
        self.play = False
        self.score += 100*self.nb_piece
        self.endMenu = EndMenu(self.screen, self.DISPLAY_W, self.DISPLAY_H, self, self.main)
        self.end_game = True


class ATH(object):
    def __init__(self, screen, game, w, h):
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.score = 0
        self.time = 0
        self.time_w = 0
        self.game = game
        self.duration = 100*(self.game.worldSize+1)

        self.font = pygame.font.Font("font/super-mario-bros-nes.ttf", 30)

    def draw_score(self):
        m = "mari"+str(0)
        text = self.font.render(m, True, (255, 255, 255))
        text_rect = text.get_rect(topleft = (50, 20))
        text_score = self.font.render(self.write_score(), True, (255, 255, 255))
        text_score_rect = text_score.get_rect(topleft = (50, 60))
        self.screen.blit(text, text_rect)
        self.screen.blit(text_score, text_score_rect)

    def draw_time(self):
        text = self.font.render("time", True, (255, 255, 255))
        text_rect = text.get_rect(topright = (self.DISPLAY_W - 50, 20))
        text_time = self.font.render(str(self.write_time()), True, (255, 255, 255))
        text_time_rect = text_time.get_rect(topright = (self.DISPLAY_W - 50, 60))
        self.screen.blit(text, text_rect)
        self.screen.blit(text_time, text_time_rect)

    def draw_piece_score(self):
        img_preload = pygame.image.load("images/entité/piece.png").convert_alpha()
        img = pygame.transform.scale(img_preload, (45, 50))
        img_rect = img.get_rect(topright = (self.DISPLAY_W - 500, 50))
        text_piece = self.font.render(str(self.write_piece_score()), True, (255, 255, 255))
        text_piece_rect = text_piece.get_rect(topright = (self.DISPLAY_W - 380, 60))
        self.screen.blit(img, img_rect)
        self.screen.blit(text_piece, text_piece_rect)

    def write_score(self):
        score = str(self.game.score)
        score_to_display = ""
        for i in range(len(score)):
            score_to_display += score[i]
        while len(score_to_display) != 5 :
            score_to_display = "0" + score_to_display
        return score_to_display

    def write_piece_score(self):
        nb = str(self.game.nb_piece)
        text_to_display = ""
        for i in range(len(nb)):
            text_to_display += nb[i]
        while len(text_to_display) != 3 :
            text_to_display = "0" + text_to_display
        text_to_display = "x" + text_to_display
        return text_to_display

    def write_time(self):
        time = str(self.duration-self.time_w)
        time_to_display = ""
        for i in range(len(time)):
            time_to_display += time[i]
        while len(time_to_display) != 4 :
            time_to_display = "0" + time_to_display
        return time_to_display

    def update(self, point = 0):
        self.score += point
        self.time += 1
        if self.duration*10 - self.time >= 0 :     
            if self.time % 10 == 0:
                self.time_w += 1

    def draw(self):
        self.draw_score()
        self.draw_time()
        self.draw_piece_score()

class PauseMenu :
    def __init__(self, screen, w, h, game):
        # Info fenêtre
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.game = game

        # Paramètre jeu
        self.done = False
        self.b_select = None

        # Paramètres menu
        self.label_button = ["REPRENDRE", "MENU"]
        self.liste_bouton = []
        for i in range(len(self.label_button)) :
            self.liste_bouton.append(Bouton(self.screen, self.DISPLAY_W//2, self.DISPLAY_H//2 - 100 + 100*i, self.label_button[i]))

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.play = True
            elif event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if self.liste_bouton[0].text_rect.collidepoint(x, y): # bouton reprendre
                        Sound(self.main, 'Click.wav', 0.05*self.game.menu.volume, False)
                        self.game.play = True
                    if self.liste_bouton[1].text_rect.collidepoint(x, y): # bouton pour retourner au menu
                        Sound(self.main, 'Click.wav', 0.05*self.game.menu.volume, False)
                        self.game.menu.main.actif = self.game.menu
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 7 or event.button == 1:
                    Sound(self.main, 'Click.wav', 0.05*self.game.menu.volume, False)
                    self.game.play = True
                if event.button == 0:
                    if self.b_select == 0:
                        Sound(self.main, 'Click.wav', 0.05*self.game.menu.volume, False)
                        self.game.play = True
                    if self.b_select == 1:
                        Sound(self.main, 'Click.wav', 0.05*self.game.menu.volume, False)
                        self.game.menu.main.actif = self.game.menu
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

    def update(self):
        for bouton in self.liste_bouton :
            if bouton.text_rect.collidepoint(pygame.mouse.get_pos()) :
                bouton.update((0, 0, 0))
            else :
                bouton.update((255, 255, 255))

    def draw(self):
        for bouton in self.liste_bouton :
            bouton.draw()

class EndMenu:
    def __init__(self, screen, w, h, game, main):
        # Info fenêtre
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.game = game
        self.main = main

        # Paramètre jeu
        self.done = False

        # Paramètres menu
        best_s = getBestScore()
        best_score = "BEST SCORE : " + str(best_s)
        score = "SCORE : " + str(self.game.score)
        font = pygame.font.Font("font/super-mario-bros-nes.ttf", 40)
        self.best_score = font.render(best_score, True, (255, 255, 255))
        self.best_score_rect = self.best_score.get_rect(center = (self.DISPLAY_W//2, self.DISPLAY_H//2 - 170))
        
        font = pygame.font.Font("font/super-mario-bros-nes.ttf", 50)
        self.score = font.render(score, True, (255, 255, 255))
        self.score_rect = self.score.get_rect(center = (self.DISPLAY_W//2, self.DISPLAY_H//2 - 100))
        self.label_button = ["MENU PRINCIPAL"]
        self.liste_bouton = []
        for i in range(len(self.label_button)) :
            self.liste_bouton.append(Bouton(self.screen, self.DISPLAY_W//2, self.DISPLAY_H//2, self.label_button[i]))

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN :
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    if self.liste_bouton[0].text_rect.collidepoint(x, y):
                        Sound(self.main, 'Click.wav', 0.05*self.game.menu.volume, False)
                        self.game.menu.main.actif = self.game.menu


    def update(self):
        for bouton in self.liste_bouton :
            if bouton.text_rect.collidepoint(pygame.mouse.get_pos()) :
                bouton.update((0, 0, 0))
            else :
                bouton.update((255, 255, 255))

    def draw(self):
        self.screen.blit(self.best_score, self.best_score_rect)
        self.screen.blit(self.score, self.score_rect)
        for bouton in self.liste_bouton :
            bouton.draw()