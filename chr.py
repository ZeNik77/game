import pygame
from os import path

WIDTH = 1000
HEIGHT = 650


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.last = True
        self.canmove = True
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
        self.flag_ability = False

    def attack(self):
        self.attack_r = pygame.Surface((50, 100), pygame.SRCALPHA, 32)
        self.attack_r.fill((255, 255, 255))
        self.attack_rect = self.attack_r.get_rect()
        if not self.last:
            self.attack_rect.centerx, self.attack_rect.centery = self.rect.x, self.rect.y + 50
        else:
            self.attack_rect.centerx, self.attack_rect.centery = self.rect.x + 85, self.rect.y + 50
        self.screen.blit(self.attack_r, self.attack_rect, special_flags=pygame.BLEND_RGBA_MULT)

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
        self.rect.x += self.speedx
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
        if keystate[pygame.K_q]:
            self.flag_ability = True
        self.screen.blit(self.image, self.rect)


class Nikita_Dev(Player, pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, self.screen)
        img_dir = path.join(path.dirname(__file__), 'Assets')

    def update2(self):
        if self.flag_ability:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_1]:
                print('xd')
