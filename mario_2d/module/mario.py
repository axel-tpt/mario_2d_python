# ------ Import ------
import pygame
# --- fichier
from mario_2d.module.sound import Sound
from mario_2d.module.point import Point
from mario_2d.module.timer import Timer

class Mario:
    def __init__(self, screen, w, h, game, main):
        # Info fenêtre
        self.screen = screen
        self.DISPLAY_W = w
        self.DISPLAY_H = h
        self.game = game
        self.main = main
        
        # ------ paramètre image ------
        # sprite sur le poteau
        img_poteau_0 = pygame.image.load('images/mario/SmallMario_Poteau.png').convert_alpha()
        self.img_poteau_0 = pygame.transform.scale(img_poteau_0, (30, 30))
        img_poteau_1 = pygame.image.load('images/mario/BigMario_Poteau.png').convert_alpha()
        self.img_poteau_1 = pygame.transform.scale(img_poteau_1, (30, 60))
        # sprite jump
        img_jump_0 = pygame.image.load('images/mario/SmallMario_Jump.png').convert_alpha()
        self.img_jump_0_right = pygame.transform.scale(img_jump_0, (30, 30))
        self.img_jump_0_left = pygame.transform.flip(self.img_jump_0_right, True, False)
        img_jump_1 = pygame.image.load('images/mario/BigMario_Jump.png').convert_alpha()
        self.img_jump_1_right = pygame.transform.scale(img_jump_1, (30, 60))
        self.img_jump_1_left = pygame.transform.flip(self.img_jump_1_right, True, False)
        # sprite mario grand (size = 1)
        img_1 = pygame.image.load('images/mario/BigMario.png').convert_alpha()
        self.img_1_right = pygame.transform.scale(img_1, (30, 60))
        self.img_1_left = pygame.transform.flip(self.img_1_right, True, False)
        # sprite mario petit (size = 0)
        img_0 = pygame.image.load('images/mario/SmallMario.png').convert_alpha()
        self.img_0_right = pygame.transform.scale(img_0, (30, 30))
        self.img_0_left = pygame.transform.flip(self.img_0_right, True, False)
        self.img_actif = self.img_0_right
        self.size = 0

        self.rect = self.img_actif.get_rect()
        self.rect.x = self.DISPLAY_W//2 - self.rect.width//2
        self.rect.y = self.DISPLAY_H - 5 * 30
        self.dx = 0
        self.dy = 0
        self.blocked = False
        self.dead = False
        self.poteau_anim = False

        # ------ paramètre in game ------
        self.anim = False
        self.speed = 0
        self.jumped = True
        self.hitDelay = Timer(30)
        self.PowerUpTimer = Timer(30)

        self.is_left = False
        self.is_right = False
        self.motion = 0

    def controler(self):
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                print(event)
                

    def update(self):
        self.dx = 0
        self.dy = 0

        # actualise la position de la caméra et celle d'affichage des éléments
        self.game.cam = 2-(self.rect.x-434)
        self.game.borne_gauche = self.rect.x - self.game.dist_affichage
        self.game.borne_droite = self.rect.x + self.game.dist_affichage

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value > 0:
                        self.right()
                    elif event.value < 0:
                        self.left()

        if not self.anim:
            # Simulation de la gravité
            self.speed += 1
            if self.speed > 10:
                self.speed = 10
            self.dy += self.speed

            # gestion contrôle
            keys = pygame.key.get_pressed()
            if keys[self.game.controle["left"]]:
                self.left()
            if keys[self.game.controle["right"]]:
                self.right()

        self.controler()

        self.blocked = False
        self.collision_sol() # contacte avec le sol
        self.collision_mob() # contacte avec les mobs
        self.collision_pu() # contacte avec les power up
        self.collision_piece() # contacte avec les pieces
        self.collision_poteau() # contacte avec le poteau de fin
        if not self.game.end_anim :
            self.collision_decor() # contacte avec le décor
       
        

        self.timer_update()

    def coordonnee(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.rect.bottom > self.DISPLAY_H :
            self.game.marioDead()

    def timer_update(self):
        tab = [self.hitDelay, self.PowerUpTimer]
        for timer in tab:
            timer.update()
        # ------ Animation quand il prend des dégâts ------
        if self.hitDelay.startBool :
            self.flashAnim()
            self.anim = True
        else:
            self.anim = False
            self.drawBool = True
        # ------ Animation quand il prend un power up ------
        if self.PowerUpTimer.startBool :
            self.growAnim()
            self.anim = True
        if not self.PowerUpTimer.startBool and not self.hitDelay.startBool:
            self.anim = False

    def draw(self, cam):
        if self.drawBool :
            self.screen.blit(self.img_actif, (self.rect.x + cam, self.rect.y))

    def jump(self):
        if self.jumped :
            self.speed = -17
            self.jumped = False
            if self.size == 0 :
                if self.img_actif == self.img_0_right:
                    self.img_actif = self.img_jump_0_right
                else:
                    self.img_actif = self.img_jump_0_left
                Sound(self.main, 'Mario Jump Small.wav', 0.05*self.game.menu.volume, False)
            else :
                if self.img_actif == self.img_1_right:
                    self.img_actif = self.img_jump_1_right
                else:
                    self.img_actif = self.img_jump_1_left
                Sound(self.main, 'Mario Jump Super.wav', 0.05*self.game.menu.volume, False)

    # ------ collision par entité ------
    def collision_sol(self):
        for col in self.game.sol :
            for block in col.l_block :
                # collision par le haut / bas
                if block.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.speed > 0: # par le haut
                        if self.size == 0:
                            if self.img_actif == self.img_jump_0_left:
                                self.img_actif = self.img_0_left
                            elif self.img_actif == self.img_jump_0_right:
                                self.img_actif = self.img_0_right
                        else:
                            if self.img_actif == self.img_jump_1_left:
                                self.img_actif = self.img_1_left
                            elif self.img_actif == self.img_jump_1_right:
                                self.img_actif = self.img_1_right
                        self.speed = 0
                        self.dy = block.rect.top - self.rect.bottom
                        self.jumped = True
                
                # collision par la droite / gauche
                if block.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.blocked = True
                    if (block.rect.x + block.rect.width//2) < self.rect.x :
                        self.dx = block.rect.right - self.rect.left
                    if (block.rect.x + block.rect.width//2) > self.rect.x :
                        self.dx = block.rect.left - self.rect.right

    def collision_decor(self):
        for elt in self.game.decor :
            if elt.type != "castle" :
                # collision par le haut / bas
                if elt.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.speed > 0 : # par le haut
                        if self.size == 0:
                            if self.img_actif == self.img_jump_0_left:
                                self.img_actif = self.img_0_left
                            elif self.img_actif == self.img_jump_0_right:
                                self.img_actif = self.img_0_right
                        else:
                            if self.img_actif == self.img_jump_1_left:
                                self.img_actif = self.img_1_left
                            elif self.img_actif == self.img_jump_1_right:
                                self.img_actif = self.img_1_right
                        self.jumped = True
                        self.dy = elt.rect.top - self.rect.bottom
                        self.speed = 0
                    if self.speed < 0 : # par le bas
                        Sound(self.main, "Bump.wav", 0.05*self.game.menu.volume, False)
                        self.dy = elt.rect.bottom - self.rect.top
                        self.speed = 0
                        if elt.type == "mystery" :
                            elt.drop()
                            elt.empty = True

                # collision par la droite / gauche
                if elt.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.blocked = True
                    if (elt.rect.x + elt.rect.width//2) < self.rect.x :
                        self.dx = elt.rect.right - self.rect.left
                    if (elt.rect.x + elt.rect.width//2) > self.rect.x :
                        self.dx = elt.rect.left - self.rect.right

    def collision_decor_y(self): # permet de vérifier si mario est sur un bloc
        col = False
        for elt in self.game.decor :
            if elt.type != "castle" :
                if elt.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                    if self.speed > 0 :
                        col = True
        return col

    def collision_mob(self):
        for mob in self.game.liste_mob :
            if mob.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.rect.width, self.rect.height):
                if self.hitDelay.done() and not self.collision_decor_y():
                    Sound(self.main, 'Stomp.wav', 0.05*self.game.menu.volume, False)
                    self.game.liste_mob.remove(mob)
                    self.game.score += 100
                    self.game.point.append(Point(self.screen, 100, mob.rect.x + mob.rect.width, mob.rect.y))

    def collision_piece(self):
        for piece in self.game.liste_piece :
            if piece.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                Sound(self.main, 'Piece.wav', 0.05*self.game.menu.volume, False)
                self.game.liste_piece.remove(piece)
                self.game.nb_piece += 1

    def collision_pu(self):
        for pu in self.game.liste_pu :
            if pu.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                Sound(self.main, 'Power Up.wav', 0.05*self.game.menu.volume, False)
                self.game.liste_pu.remove(pu)
                self.game.score += 1000
                self.game.point.append(Point(self.screen, 1000, pu.rect.x + pu.rect.width, pu.rect.y))
                if self.size == 0:
                    self.PowerUpTimer.start()

    def collision_poteau(self):
        for elt in self.game.end_level :
            if elt.type == "poteau" :
                if elt.base.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):        
                    self.game.menu.music.pause()
                    self.game.end_anim = True
                    if self.game.menu.music.state == 1 :
                        Sound(self.main, "End Level.wav", 0.08, False)
                if elt.barre.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.rect.width, self.rect.height):
                    self.game.menu.music.pause()
                    if self.game.menu.music.state == 1 :
                        Sound(self.main, "End Level.wav", 0.08, False)
                    if self.size == 0 :
                        self.img_actif = self.img_poteau_0
                    else:
                        self.img_actif = self.img_poteau_1
                    self.game.end_anim = True
                    self.poteau_anim = True
                    s = False
                    for i in range(1, 7):
                        if self.rect.bottom > 570 - 30*i and not s:
                            s = True
                            self.game.score += 1000*i
                            self.game.point.append(Point(self.screen, 1000*i, self.rect.x + self.rect.width, self.rect.bottom))

    # ------ changement de sprite ------
    def left(self):
        self.dx -= 3
        if self.img_actif == self.img_0_right:
            self.img_actif = self.img_0_left
        if self.img_actif == self.img_1_right:
            self.img_actif = self.img_1_left
        if self.img_actif == self.img_jump_0_right:
            self.img_actif = self.img_jump_0_left
        if self.img_actif == self.img_jump_1_right:
            self.img_actif = self.img_jump_1_left
        
    def right(self):
        self.dx += 3
        if self.img_actif == self.img_0_left:
            self.img_actif = self.img_0_right
        if self.img_actif == self.img_1_left:
            self.img_actif = self.img_1_right
        if self.img_actif == self.img_jump_0_left:
            self.img_actif = self.img_jump_0_right
        if self.img_actif == self.img_jump_1_left:
            self.img_actif = self.img_jump_1_right

    def changeSize(self):
        if self.img_actif == self.img_0_right or self.img_actif == self.img_0_left :
            self.grow()
            self.size = 1
        else :
            self.shrink()
            self.size = 0
        x, y = self.rect.x, self.rect.bottom
        self.rect = self.img_actif.get_rect()
        self.rect.x, self.rect.bottom = x, y      

    def grow(self): # quand mario grandi
        self.size = 1
        if self.img_actif == self.img_0_left:
            self.img_actif = self.img_1_left
        if self.img_actif == self.img_0_right:
            self.img_actif = self.img_1_right
        if self.img_actif == self.img_jump_0_left:
            self.img_actif = self.img_jump_1_left
        if self.img_actif == self.img_jump_0_right:
            self.img_actif = self.img_jump_1_right
        x, y = self.rect.x, self.rect.bottom
        self.rect = self.img_actif.get_rect()
        self.rect.x, self.rect.bottom = x, y

    def shrink(self): # quand mario rétréci
        self.size = 0
        if self.img_actif == self.img_1_left:
            self.img_actif = self.img_0_left
        if self.img_actif == self.img_1_right:
            self.img_actif = self.img_0_right
        if self.img_actif == self.img_jump_1_left:
            self.img_actif = self.img_jump_0_left
        if self.img_actif == self.img_jump_1_right:
            self.img_actif = self.img_jump_0_right
        x, y = self.rect.x, self.rect.bottom
        self.rect = self.img_actif.get_rect()
        self.rect.x, self.rect.bottom = x, y

    def flashAnim(self): # quand mario prend des dégât
        if not self.hitDelay.done():
            if self.hitDelay.time%5 == 0:
                self.drawBool = not self.drawBool

    def growAnim(self): # quand mario prend un champion
        if not self.PowerUpTimer.done():
            if self.PowerUpTimer.time%5 == 0:
                if self.size == 0:
                    self.grow()
                else:
                    self.shrink()