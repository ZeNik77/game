import pygame
from os import path
WIDTH = 1000
HEIGHT = 650
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(path.join(img_dir, 'blue1_0.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (33, HEIGHT - 100)
        self.left = 0
        self.right = 0
        self.animcount = 0
        self.flag_ability = False
    def update(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.speedx = 0
        self.rect.x += self.speedx
        keystate = pygame.key.get_pressed()
        if self.animcount + 1 >= 60:
            self.animcount = 1
        if keystate[pygame.K_LEFT]:
            self.left = True
            self.right = False
            self.speedx = -8
            # self.image = pygame.image.load(path.join(img_dir, 'blue2.png')).convert()
            self.image.set_colorkey((255, 255, 255))
        elif keystate[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            self.speedx = 8
            # self.image = pygame.image.load(path.join(img_dir, 'blue1.png')).convert()
            self.image.set_colorkey((255, 255, 255))
        else:
            self.left = False
            self.right = False
            self.animcount = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.animcount += 1
        if self.left:
            self.image = pygame.image.load(path.join(img_dir, f'blue2_{self.animcount // 9}.png')).convert()
        else:
            self.image = pygame.image.load(path.join(img_dir, f'blue1_{self.animcount // 9}.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect.x += self.speedx
        if keystate[pygame.K_f]:
            self.flag_ability = True
class Nikita_Dev(Player, pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
    def update2(self):
        if self.flag_ability:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_1]:
                print('xd')
