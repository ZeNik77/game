import pygame
from os import path

WIDTH = 1000
HEIGHT = 650


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.hp = 100
        self.enemy = 0
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.last = True
        self.canmove = True

        self.attack_r = pygame.sprite.Sprite()
        self.attack_r.image = pygame.Surface((50, 100))
        self.attack_r.rect = self.attack_r.image.get_rect()
        self.attack_r.image.fill((255, 255, 255))

        self.blocking = False
        self.attacking = False
        if self.last:
            self.image = pygame.image.load(path.join(img_dir, 'blue1_0.png')).convert()
        else:
            self.image = pygame.image.load(path.join(img_dir, 'blue2_0.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (33, HEIGHT - 100)
        self.left = 0
        self.right = 0
        self.animcount = 0
        self.attackacount = 15

    def attack(self):
        # , special_flags=pygame.BLEND_RGBA_MULT
        if not self.last:
            self.attack_r.rect.x, self.attack_r.rect.y = self.rect.x-12.5, self.rect.y
        else:
            self.attack_r.rect.x, self.attack_r.rect.y = self.rect.x+55, self.rect.y
        self.screen.blit(self.attack_r.image, self.attack_r.rect, special_flags=pygame.BLEND_RGBA_MULT)

    def block(self):
        self.block_r = pygame.Surface((50, 100), pygame.SRCALPHA, 32)
        self.block_r.fill((255, 255, 255))
        self.block_rect = self.block_r.get_rect()
        # tmp = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        # tmp.fill((255, 255, 255, 128))
        if not self.last:
            self.block_rect.centerx, self.block_rect.centery = self.rect.x, self.rect.y + 50
        else:
            self.block_rect.centerx, self.block_rect.centery = self.rect.x + 85, self.rect.y + 50
        self.screen.blit(self.block_r, self.block_rect, special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.speedx = 0
        # self.rect.x += self.speedx
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_f]:
            self.blocking = True
            self.canmove = False
        if keystate[pygame.K_c]:
            self.attacking = True
            self.canmove = False
        if self.animcount + 1 >= 60:
            self.animcount = 1
        if self.canmove:
            self.attack_r.rect.x = 800
            self.attack_r.rect.y = 500
            if keystate[pygame.K_LEFT]:
                self.last = False
                self.left = True
                self.right = False
                self.speedx = -8
                self.image.set_colorkey((255, 255, 255))
            elif keystate[pygame.K_RIGHT]:
                self.last = True
                self.right = True
                self.left = False
                self.speedx = 8
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
            elif self.right:
                self.image = pygame.image.load(path.join(img_dir, f'blue1_{self.animcount // 9}.png')).convert()
            else:
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, 'blue1_0.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, 'blue2_0.png')).convert()
        else:
            if keystate[pygame.K_f]:
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, 'blue1_block.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, 'blue2_block.png')).convert()
                self.block()
            elif self.attacking:
                self.attackacount += 1
                if self.attackacount >= 30:
                    if self.last:
                        self.rect.x += 10
                    else:
                        self.rect.x -= 10
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, f'blue1_a_{self.attackacount // 15}.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, f'blue2_a_{self.attackacount // 15}.png')).convert()
                self.attack()
                hits = pygame.sprite.collide_rect(self.enemy, self.attack_r)
                if hits:
                    self.enemy.hp -= 1

                if self.attackacount >= 40:
                    self.attackacount = 15
                    self.canmove = True
                    self.attacking = False
            else:
                self.animcount = 0
                self.blocking = False
                self.canmove = True
        self.image.set_colorkey((255, 255, 255))
        self.rect.x += self.speedx
        self.screen.blit(self.image, self.rect)


class Nikita_Dev(Player, pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, self.screen)
        img_dir = path.join(path.dirname(__file__), 'Assets')

class Dummy(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.hp = 100
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(path.join(img_dir, 'blue2_0.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 250, HEIGHT - 100
    def update(self):
        self.screen.blit(self.image, self.rect)
