# ------ Import ------
import csv
from random import randint
# --- fichier
from mario_2d.module.block import *
from mario_2d.module.mob import *
from mario_2d.module.tuyau import Tuyau
from mario_2d.module.piece import Piece
from mario_2d.module.end_part import *

class World:
    def __init__(self, screen, game, width, main):
        self.screen = screen
        self.game = game
        self.worldSize = width
        self.main = main

        self.liste_mob = []
        self.liste_pu = []
        self.liste_piece = []
        self.decor = []
        self.sol = []
        self.end_level = []

    def readCSV(self):
        # ------ début du niveau ------
        fichier = open("niveau/start.csv", 'r', encoding="utf-8")
        reader = csv.DictReader(fichier, delimiter=";")
        nom_col = self.nb_col("niveau/start.csv")
        i = 0
        for dico in reader :
            for j in range(len(nom_col)) :
                self.element(self.minuscule(dico[nom_col[j]]), i, j, 0)
            i += 1
        fichier.close()
        # ------ parties du niveau ------
        listePart = self.choosePart()
        for k in range(1, len(listePart)+1) :
            nom_fichier = "niveau/" + listePart[k-1] + ".csv"
            fichier = open(nom_fichier, 'r', encoding="utf-8")
            reader = csv.DictReader(fichier, delimiter=";")
            nom_col = self.nb_col(nom_fichier)
            i = 0
            for dico in reader :
                for j in range(len(nom_col)) :
                    self.element(self.minuscule(dico[nom_col[j]]), i, j, k)
                i += 1
            fichier.close()
        # ------ fin du niveau ------
        fichier = open("niveau/end.csv", 'r', encoding="utf-8")
        reader = csv.DictReader(fichier, delimiter=";")
        nom_col = self.nb_col("niveau/end.csv")
        i = 0
        for dico in reader :
            for j in range(len(nom_col)) :
                self.element(self.minuscule(dico[nom_col[j]]), i, j, self.worldSize+1)
            i += 1
        fichier.close()

    def element(self, case, i, j, k):
        if case == "g" : # Goomba
            y = 30 * i
            x = 30 * j + 900*k
            self.liste_mob.append(Goomba(self.screen, self.game, x, y))

        # ------ Block -------
        if case == "s" :
            y = 30 * i
            x = 30 * j + 900*k
            self.sol.append(Sol(self.screen, self.game.DISPLAY_W, self.game.DISPLAY_H, x, y))
        if case == "p" : # Plateforme
            y = 30 * i
            x = 30 * j + 900*k
            self.decor.append(Brick(self.screen, x, y))
        if case == "mb" : # mystery block
            y = 30 * i
            x = 30 * j + 900*k
            self.decor.append(MysteryBlock(self.screen, self.game, x, y, self.main))
        if case == "st" : # stairs block
            y = 30 * i
            x = 30 * j + 900*k
            if y < 570 :
                self.buildStairs(x, y)
            self.decor.append(Stairs(self.screen, x, y))
        if case == "t" : # tuyau
            y = 30 * i
            x = 30 * j + 900*k
            self.decor.append(Tuyau(self.screen, x, y))
        if case == "castle" :
            y = 30 * i
            x = 30 * j + 900*k
            self.end_level.append(Castle(self.screen, self.game, x, y))
        if case == "poteau" :
            y = 30 * i
            x = 30 * j + 900*k
            self.end_level.append(Poteau(self.screen, self.game, x, y))

        if case == "pi" : # piece
            y = 30 * i
            x = 30 * j + 900*k
            self.liste_piece.append(Piece(self.screen, x, y))

    def choosePart(self):
        nb = self.worldSize
        partOrder = []
        if nb > 0:
            a = randint(0, 100)
            if a < 25 :
                nb -= 1
            for i in range(nb):
                partOrder.append("part"+str(randint(1, 9)))
            if a < 25 :
                partOrder.append("BONUS")
        return partOrder

    # compte le nombre de colone dans le fichier 
    def nb_col(self, file):
        fichier = open(file, 'r', encoding="utf-8")
        line = fichier.readline()
        nom_col = line.split(";")
        nom_col[len(nom_col)-1] = nom_col[len(nom_col)-1][:-1]
        fichier.close()
        return nom_col

    def minuscule(self, text):
        rep = ""
        if text != None :
            for lettre in text :
                if ord(lettre) >= 65 and ord(lettre) <= 90 :
                    rep += (chr(ord(lettre) + 32))
                else :
                    rep += (lettre)
        return rep

    def buildStairs(self, x, y):
        height = (570 - y)//30
        for i in range(height) :
            y = 570 - 30*i
            new = True
            for block in self.decor :
                if block.rect.y == y and block.rect.x == x:
                    new = False
            if new :
                self.decor.append(Stairs(self.screen, x, y))

    def content(self):
        return self.liste_mob, self.liste_pu, self.liste_piece, self.decor, self.sol, self.end_level