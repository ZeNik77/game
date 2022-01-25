import pygame
from os import path
import math
import random
import asyncio

WIDTH = 1000
HEIGHT = 650
pygame.init()
pygame.mixer.init()

def text(screen, phrase, coords):
    font = pygame.font.Font(None, 30)
    font_color = (255, 255, 255)
    t = font.render(phrase, True, font_color)
    t_rect = t.get_rect()
    t_rect.centerx = coords[0]
    t_rect.y = coords[1] - 10
    screen.blit(t, t_rect)


class Player(pygame.sprite.Sprite):

    def __init__(self, screen, colour):
        self.called_phrases = []
        self.dur = 0
        self.blockdur = 45
        self.attack_damage = 1.5
        self.permspeed = 1
        self.colour = colour
        self.screen = screen
        self.hp = 1000
        self.enemy = 0
        self.enemygroup = 0
        self.canblock = True
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.colour == 'blue':
            self.last = True
            self.abkeys = [pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_f, pygame.K_c]
        else:
            self.last = False
            self.abkeys = [pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_h, pygame.K_n]
        self.canmove = True

        self.attack_r = pygame.sprite.Sprite()
        self.attack_r.image = pygame.Surface((50, 100))
        self.attack_r.rect = self.attack_r.image.get_rect()
        self.attack_r.image.fill((255, 255, 255))
        self.block_cd = 0
        self.blocking = False
        self.attacking = False
        self.flag_ability = False
        if self.last:
            self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_0.png')).convert()
        else:
            self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_0.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        if self.colour == 'blue':
            self.rect.center = (33, HEIGHT - 100)
        else:
            self.rect.center = (WIDTH - 33, HEIGHT - 100)
        self.left = 0
        self.right = 0
        self.animcount = 0
        self.attackacount = 15
        self.atk_sound = pygame.mixer.Sound(file=path.join(img_dir, 'hitHurt.wav'))
        self.atk_flag = False
        self.block_sound = pygame.mixer.Sound(path.join(img_dir, 'block.wav'))
        self.block_flag = False
        self.blockBroken_sound = pygame.mixer.Sound(path.join(img_dir, 'blockBroken.wav'))
        self.ability1_name = ''
        self.ability1_maxcd = 0
        self.ability2_name = ''
        self.ability2_maxcd = 0
        self.ability3_name = ''
        self.ability3_maxcd = 0
        self.font2 = pygame.font.Font(None, 35)
        if self.colour == 'blue':
            self.font2_color = (0, 255, 240)
        else:
            self.font2_color = (255, 10, 100)
        self.font2_background = (0, 0, 0)
        self.t_cd1 = self.font2.render(self.ability1_name + f": {self.ability1_maxcd - self.ability1_cd}", True,
                                       self.font2_color, self.font2_background)
        self.t_cd1_rect = self.t_cd1.get_rect()
        if self.colour == 'blue':
            self.t_cd1_rect.x = 240
        else:
            self.t_cd1_rect.right = 1000 - 240
        self.t_cd1_rect.y = 75
        self.t_cd2 = self.font2.render(self.ability2_name + f": {self.ability2_maxcd - self.ability2_cd}", True,
                                       self.font2_color, self.font2_background)
        self.t_cd2_rect = self.t_cd2.get_rect()
        if self.colour == 'blue':
            self.t_cd2_rect.x = 240
        else:
            self.t_cd2_rect.right = 1000 - 240
        self.t_cd2_rect.y = 75 + 55

        self.t_cd3 = self.font2.render(self.ability3_name + f": {self.ability3_maxcd - self.ability3_cd}", True,
                                       self.font2_color, self.font2_background)
        self.t_cd3_rect = self.t_cd3.get_rect()
        if self.colour == 'blue':
            self.t_cd3_rect.x = 240
        else:
            self.t_cd3_rect.right = 1000 - 240
        self.t_cd3_rect.y = 75 + 55 + 55

    def attack(self):
        # , special_flags=pygame.BLEND_RGBA_MULT
        if not self.last:
            self.attack_r.rect.x, self.attack_r.rect.y = self.rect.x - 12.5, self.rect.y
        else:
            self.attack_r.rect.x, self.attack_r.rect.y = self.rect.x + 55, self.rect.y
        self.screen.blit(self.attack_r.image, self.attack_r.rect, special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        for el in self.called_phrases:
            text(self.screen, el[0], (el[1], el[2]))
            el[2] -= 1
            if el[2] <= self.rect.y - 95:
                self.called_phrases.remove(el)
        self.t_cd1 = self.font2.render(self.ability1_name + f": {round((self.ability1_maxcd - self.ability1_cd)//60)}", True,
                                       self.font2_color, self.font2_background)
        self.t_cd1_rect = self.t_cd1.get_rect()
        if self.colour == 'blue':
            self.t_cd1_rect.x = 240
        else:
            self.t_cd1_rect.right = 1000 - 240
        self.t_cd1_rect.y = 75
        self.t_cd2 = self.font2.render(self.ability2_name + f": {round((self.ability2_maxcd - self.ability2_cd)//60)}", True,
                                       self.font2_color, self.font2_background)
        self.t_cd2_rect = self.t_cd2.get_rect()
        if self.colour == 'blue':
            self.t_cd2_rect.x = 240
        else:
            self.t_cd2_rect.right = 1000 - 240
        self.t_cd2_rect.y = 75 + 55

        self.t_cd3 = self.font2.render(self.ability3_name + f": {round((self.ability3_maxcd - self.ability3_cd)//60)}", True,
                                       self.font2_color, self.font2_background)
        self.t_cd3_rect = self.t_cd3.get_rect()
        if self.colour == 'blue':
            self.t_cd3_rect.x = 240
        else:
            self.t_cd3_rect.right = 1000 - 240
        self.t_cd3_rect.y = 75 + 55 + 55
        if self.ability1_cd != 0 and self.ability1_name != '':
            self.screen.blit(self.t_cd1, self.t_cd1_rect)
        if self.ability2_cd != 0 and self.ability2_name != '':
            self.screen.blit(self.t_cd2, self.t_cd2_rect)
        if self.ability3_cd != 0 and self.ability3_name != '':
            self.screen.blit(self.t_cd3, self.t_cd3_rect)
        if self.hp <= 0:
            with open('whowon.txt', 'w') as f:
                f.write(f'{self.enemy.colour} WON!!!!!!!')
            exit(0)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.blockdur <= 0:
            self.canblock = False
            self.blockdur = 0
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[self.abkeys[3]] and self.canblock and not self.flag_ability:
            self.blocking = True
            self.canmove = False
            if self.blockdur == 31:
                self.block_flag = True
            elif self.block_flag and self.blockdur == 30:
                self.block_flag = False
                self.block_sound.play()
            else:
                self.block_flag = False
        elif keystate[self.abkeys[4]] and not self.flag_ability or self.attacking == True:
            self.canmove = False
            self.attacking = True
        else:
            if not self.flag_ability:
                self.blocking = False
                self.canmove = True
                if self.blockdur != 45:
                    self.dur += 1
                    if self.dur >= 60:
                        self.dur = 0
                        self.blockdur = 45

        if self.canblock == False and self.flag_ability == False:
            self.blocking = False
            self.canmove = False
            if self.last:
                self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_0.png')).convert()
                self.rect.x -= 0.05
            else:
                self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_0.png')).convert()
                self.rect.x += 0.05
            self.block_cd += 1
            if self.block_cd == 1:
                self.blockBroken_sound.play()
            if self.block_cd >= 90:
                self.block_cd = 0
                self.canblock = True
        if self.animcount + 1 >= 60:
            self.animcount = 1
        if self.canmove:
            self.attack_r.rect.x = 800
            self.attack_r.rect.y = 500
            if self.colour == 'blue':
                if keystate[pygame.K_a]:
                    self.last = False
                    self.left = True
                    self.right = False
                    self.speedx = -8
                    self.image.set_colorkey((255, 255, 255))
                elif keystate[pygame.K_d]:
                    self.last = True
                    self.right = True
                    self.left = False
                    self.speedx = 8
                    self.image.set_colorkey((255, 255, 255))
                else:
                    self.left = False
                    self.right = False
                    self.animcount = 0
            elif self.colour == 'red':
                if keystate[pygame.K_j]:
                    self.last = False
                    self.left = True
                    self.right = False
                    self.speedx = -8
                    self.image.set_colorkey((255, 255, 255))
                elif keystate[pygame.K_l]:
                    self.last = True
                    self.right = True
                    self.left = False
                    self.speedx = 8
                    self.image.set_colorkey((255, 255, 255))
                else:
                    self.left = False
                    self.right = False
                    self.animcount = 0
            self.animcount += 1
            if self.left:
                self.image = pygame.image.load(
                    path.join(img_dir, f'{self.colour}2_{self.animcount // 9}.png')).convert()
            elif self.right:
                self.image = pygame.image.load(
                    path.join(img_dir, f'{self.colour}1_{self.animcount // 9}.png')).convert()
            else:
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_0.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_0.png')).convert()
        else:
            if self.blocking and not self.flag_ability:
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_block.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_block.png')).convert()
                # self.block()
            elif self.attacking and not self.flag_ability:
                self.attackacount += 1
                if self.attackacount >= 30:
                    if not self.atk_flag:
                        self.atk_sound.play()
                        self.atk_flag = True
                    if self.last:
                        self.rect.x += 10
                    else:
                        self.rect.x -= 10
                if self.last:
                    self.image = pygame.image.load(
                        path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
                else:
                    self.image = pygame.image.load(
                        path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
                self.attack()
                hits = pygame.sprite.spritecollide(self.attack_r, self.enemygroup, False)
                for hit in hits:
                    if not hit.blocking or hit.blockdur <= 0:
                        hit.hp -= self.attack_damage
                    else:
                        hit.blockdur -= 1
                if self.attackacount >= 44:
                    self.attackacount = 15
                    self.canmove = True
                    self.attacking = False
                    self.atk_flag = False
            elif self.flag_ability:
                pass
            else:
                self.animcount = 0
                self.blocking = False
                self.canmove = True
        # print(self.hp)
        self.image.set_colorkey((255, 255, 255))
        self.rect.x += self.speedx * self.permspeed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # print(self.flag_ability)
        self.screen.blit(self.image, self.rect)
class Kostya(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Kostya'
        self.colour = colour
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability3_cd = 0
        Player.__init__(self, screen, colour)
        pygame.sprite.Sprite.__init__(self)
        self.ability1_name = 'dash'
        self.ability1_maxcd = 90
        self.ability2_name = 'dash-punch'
        self.ability2_maxcd = 120
        self.ability3_name = 'mini-knifes'
        # blockdur -= 2
        self.ability3_maxcd = 240
        self.ability1_desc = 'телепортация в сторону в которую смотрит персонаж'
        self.ability2_desc = 'телепортация, если враг окажется в промежутке, то урон врагу'
        self.ability3_desc = 'последовательно пускает 3 маленьких ножа'
        self.chr_desc = 'Костя мобильный и быстрый спам персонаж'
        
        self.knife_flag = False
        self.flag_ability3 = False
        self.knife_cnt = 0
        self.ability3 = 0
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.knifes = []

        self.dash_sound = pygame.mixer.Sound(path.join(img_dir, 'dash.wav'))
    def update2(self):
        keystate = pygame.key.get_pressed()
        if keystate[self.abkeys[0]] and self.ability1_cd == 0:
            self.dash()
        if keystate[self.abkeys[1]] and self.ability2_cd == 0:
            self.dash_punch()
        if keystate[self.abkeys[2]] and self.ability3_cd == 0 and self.flag_ability3 == False:
            self.knife_flag = self.last
        if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
            self.ult()

        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= self.ability1_maxcd:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= self.ability2_maxcd:
                self.ability2_cd = 0
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= self.ability3_maxcd:
                self.ability3_cd = 0
    def dash(self):
        self.called_phrases.append(['I\'m gone', self.rect.x, self.rect.y])
        if self.last:
            self.rect.x += 200
        else:
            self.rect.x -= 200
        self.dash_sound.play()
        self.ability1_cd = 1
    def dash_punch(self):
        flag = False
        self.called_phrases.append(['Too slow', self.rect.x, self.rect.y])
        if self.last:
            if self.rect.x <= self.enemy.rect.x <= self.rect.x + 130:
                if self.enemy.blocking:
                    self.enemy.blockdur = 0
                else:
                    self.enemy.hp -= 50
                flag = True
            self.rect.x += 130

        else:
            if self.rect.x - 130 <= self.enemy.rect.x <= self.rect.x:
                if self.enemy.blocking:
                    self.enemy.blockdur = 0
                else:
                    self.enemy.hp -= 50
                flag = True
            self.rect.x -= 130
        if flag:
            self.atk_sound.play()
        else:
            self.dash_sound.play()
        self.ability2_cd = 1
    def ult(self):
        self.flag_ability3 = True
        if self.ability3 == 0:
            self.called_phrases.append(['Hm', self.rect.x, self.rect.y])
        self.ability3 += 1
        if self.knife_cnt < 3 and (self.ability3 - 1) % 25 == 0:
            if self.knife_flag:
                self.knife_cnt += 1
                x = pygame.sprite.Sprite()
                img_dir = path.join(path.dirname(__file__), 'Assets')
                x.image = pygame.image.load(path.join(img_dir, 'mini-knife1.png'))
                x.image.set_colorkey((255, 255, 255))
                x.rect = x.image.get_rect()
                x.rect.x = self.rect.x + 85 + 3
                x.rect.centery = self.rect.centery
                self.knifes.append([x, 1])
                #right?
            else:
                self.knife_cnt += 1
                x = pygame.sprite.Sprite()
                img_dir = path.join(path.dirname(__file__), 'Assets')
                x.image = pygame.image.load(path.join(img_dir, 'mini-knife2.png'))
                x.image.set_colorkey((255, 255, 255))
                x.rect = x.image.get_rect()
                x.rect.x = self.rect.x - 40 - 3
                x.rect.centery = self.rect.centery
                self.knifes.append([x, 0])
        for knife in self.knifes:
            if knife[1] == 1:
                knife[0].rect.x += 20
            else:
                knife[0].rect.x -= 20
            hits = pygame.sprite.spritecollide(knife[0], self.enemygroup, False)
            for hit in hits:
                if hit.blocking:
                    hit.blockdur -= 2
                else:
                    hit.hp -= 10
            self.screen.blit(knife[0].image, knife[0].rect)
        if self.ability3 >= 140:
            self.flag_ability3 = 0
            self.ability3_cd = 1
            self.knifes = []
            self.knife_cnt = 0
            self.ability3 = 0
class Senia(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Senia'
        self.colour = colour
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability3_cd = 0
        Player.__init__(self, screen, colour)
        pygame.sprite.Sprite.__init__(self)
        self.ability1_name = 'new knowledge'
        self.ability1_maxcd = 300
        self.ability2_name = 'gaster blaster'
        self.ability2_maxcd = 240
        self.ability3_name = 'blockade'
        self.ability3_maxcd = 720
        self.permattack = 1.5
        self.permpermspeed = 1
        img_dir = path.join(path.dirname(__file__), 'Assets')

        self.blaster_left = pygame.sprite.Sprite()
        self.blaster_left.image = pygame.image.load(path.join(img_dir, 'blaster_left.png')).convert()
        self.blaster_left.image.set_colorkey((246, 246, 246))
        self.blaster_left.rect = self.blaster_left.image.get_rect()

        self.blaster_right = pygame.sprite.Sprite()
        self.blaster_right.image = pygame.image.load(path.join(img_dir, 'blaster_right.png')).convert()
        self.blaster_right.image.set_colorkey((246, 246, 246))
        self.blaster_right.rect = self.blaster_right.image.get_rect()

        self.ability2_phase = 0
        self.flag_ability2 = False
        self.ability2 = 0
        self.blaster_multiplier = 1
        self.blaster = ''
        self.blaster_rect = pygame.sprite.Sprite()
        self.blaster_rect.image = pygame.Surface((1500, 36))
        self.blaster_rect.rect = self.blaster_rect.image.get_rect()

        self.flag_ability3 = False
        self.ability3 = 0
        self.blockade_multiplier = 2
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.improve_sound = pygame.mixer.Sound(path.join(img_dir, 'improve.wav'))
        self.gblaster_sound = pygame.mixer.Sound(path.join(img_dir, 'blaster2.wav'))
        self.ult_sound = pygame.mixer.Sound(path.join(img_dir, 'senia.wav'))
        self.ability1_desc = 'сеня учится чему-то новому, а статы взлетают вверх'
        self.ability2_desc = 'гастер бластер.'
        self.ability3_desc = 'блокирует использование способностей у врага. заодно ставит их на откат.'
        self.chr_desc = 'у Сени есть сильная блокировка способностей. а бафф характеристик делает его непобедимым в конце'

    def update2(self):
        self.permspeed = self.permpermspeed
        self.attack_damage = self.permattack

        keystate = pygame.key.get_pressed()
        if keystate[self.abkeys[0]] and not self.flag_ability and self.ability1_cd == 0:
            self.improve()
        if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
            self.gblaster()
        if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
            self.ult()
        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 300:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 240:
                self.ability2_cd = 0
        # print(self.ability3_cd)
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= 720:
                self.ability3_cd = 0

    def improve(self):
        self.permpermspeed += 0.1
        self.permattack += 0.3
        self.blaster_multiplier += 0.3
        self.blockade_multiplier += 0.1
        self.ability1_cd = 1
        self.improve_sound.play()
        self.called_phrases.append(['New knowledge will someday come in handy', self.rect.centerx, self.rect.y])

    def gblaster(self):
        self.flag_ability = True
        self.flag_ability2 = True
        self.canmove = False
        if self.ability2_phase == 0:
            if self.last:
                self.blaster = self.blaster_right
                self.blaster.rect.x = self.rect.x + 85 + 6
            else:
                self.blaster = self.blaster_left
                self.blaster.rect.x = self.rect.x - 41 - 5
            self.blaster.rect.centery = self.rect.centery
            self.gblaster_sound.play()
            self.called_phrases.append(['sans\'s legacy', self.rect.centerx, self.rect.y])
            self.ability2_phase = 1
        elif self.ability2_phase == 1:
            self.ability2 += 1
            self.screen.blit(self.blaster.image, self.blaster.rect)
            if self.ability2 >= int(45 / 1.5):
                self.ability2_phase = 2
                self.ability2 = 0
        elif self.ability2_phase == 2:
            self.screen.blit(self.blaster.image, self.blaster.rect)
            if self.last:
                self.blaster_rect.rect.x = self.rect.x + 85 + 41 + 5
            else:
                self.blaster_rect.rect.x = self.rect.x - 41 - 5 - 1500
            self.blaster_rect.rect.centery = self.rect.centery
            self.screen.blit(self.blaster_rect.image, self.blaster_rect.rect)
            hits = pygame.sprite.spritecollide(self.blaster_rect, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking:
                    hit.hp -= 4 * self.blaster_multiplier
                else:
                    hit.blockdur -= 1
            self.ability2 += 1
            if self.ability2 >= int(60 / 1.5):
                self.ability2_phase = 0
                self.ability2 = 0
                self.flag_ability2 = False
                self.flag_ability = False
                self.ability2_cd = 1

    def ult(self):
        self.enemy.ability1_cd = self.enemy.ability1_maxcd // self.blockade_multiplier
        self.enemy.ability2_cd = self.enemy.ability2_maxcd // self.blockade_multiplier
        self.flag_ability3 = True
        if self.ability3 == 0:
            self.ult_sound.play()
            self.called_phrases.append(['Aaaaand you can\'t use your abilities now', self.rect.centerx, self.rect.y])
        try:
            self.enemy.ability3_cd = self.enemy.ability3_maxcd // self.blockade_multiplier
        except:
            pass
        self.ability3 += 1
        if self.ability3 >= 390:
            self.flag_ability3 = False
            self.ability3 = 0
            self.ability3_cd = 1
class Nikita(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Nikita'
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability3_cd = 0
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.ability1_name = 'rat'
        self.ability1_maxcd = 480
        self.ability2_name = 'trick'
        self.ability2_maxcd = 480
        self.ability3_name = 'awakening'
        self.ability3_maxcd = 15 * 60

        self.flag_ability1 = False
        self.ability1 = 0
        self.ability1_phase = 0
        self.ability2 = 0
        self.flag_ability2 = False
        self.ability2_phase = 1
        self.awakening_cd = 0
        self.punch_flag = 0
        self.punch_cnt = 0
        self.movement = []
        self.epitaph_phase = 1
        self.epitaph_cnt = 0
        self.permhp = 0
        self.te_phase = 0
        self.te = 0
        self.dash_hp = self.hp
        self.invinc_cnt = 0
        self.flag_ability3 = False
        self.ability3_phase = 0
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.nebo = pygame.sprite.Sprite()
        self.nebo.image = pygame.image.load(path.join(img_dir, 'nebo.png')).convert()
        self.nebo.rect = self.nebo.image.get_rect()
        self.knifes_left = []
        self.knifes_right = []
        self.moving_right = []
        self.moving_left = []
        self.ult_cnt = 0
        self.knifes_cnt = 0
        self.knifes_amount = 0

        self.awakening = 0
        self.awakening_phase = 1
        self.awakening_cnt = 0
        self.awakening_cd = 0
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.awakening_sound = pygame.mixer.Sound(path.join(img_dir, 'awakening.wav'))
        self.speed_sound = pygame.mixer.Sound(path.join(img_dir, 'accel.wav'))
        self.epitaph_flag1 = False
        self.epitaph_flag2 = False
        self.epitaph_sound1 = pygame.mixer.Sound(path.join(img_dir, 'epitaph-1.wav'))
        self.epitaph_sound2 = pygame.mixer.Sound(path.join(img_dir, 'epitaph-2.wav'))
        self.dash_sound = pygame.mixer.Sound(path.join(img_dir, 'dash.wav'))
        self.te_sound1 = pygame.mixer.Sound(path.join(img_dir, 'te-1.wav'))
        self.te_sound2 = pygame.mixer.Sound(path.join(img_dir, 'te-2.wav'))
        self.invinc_sound = pygame.mixer.Sound(path.join(img_dir, 'invinc.wav'))
        self.ow7_sound = pygame.mixer.Sound(path.join(img_dir, 'knife.wav'))
        self.ability3_cd = 1
        self.ability1_desc = 'тп за спину с уроном, ускорение, эпитафия, вырезание времени. первое и последнее имба :)'
        self.ability2_desc = 'фокус, У Д А Р, деш, неуязвимость. первое бесполезное, второе сильное, последнее имба :)'
        self.ability3_desc = 'пробуждение. дает разные способности. во время полной концентрации создает много ножей'
        self.chr_desc = 'сложный персонаж, пробуждения дают разные способности. в конце неубиваем.'

    def update2(self):
        keystate = pygame.key.get_pressed()
        if self.awakening == False:
            self.ability3_cd = self.awakening_cd
            font = pygame.font.Font(None, 40)
            if self.colour == 'blue':
                font_color = (0, 255, 240)
            else:
                font_color = (255, 10, 100)
            self.t = font.render("Base", True, font_color)
            self.t_rect = self.t.get_rect()
            if self.colour == 'blue':
                self.t_rect.left = 5
            else:
                self.t_rect.right = 995
            self.t_rect.centery = 425

            if self.awakening_cd != 0:
                self.awakening_cd += 1
                if self.awakening_cd >= 480 and self.awakening_phase == 1:
                    self.awakening_cd = 0
                if self.awakening_cd >= 450 and self.awakening_phase == 2:
                    self.awakening_cd = 0

            if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
                self.rat()
            if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
                self.trick()
            if keystate[self.abkeys[2]] and not self.flag_ability and self.awakening_cd == 0:
                self.awakening_sound.play()
                self.awakening = True
                self.ability1_cd = 0
                self.ability2_cd = 0
                self.awakening_cd = 1
                self.called_phrases.append(['To the greater form, I go', self.rect.centerx, self.rect.y])
        elif self.awakening_phase == 1:
            self.ability1_name = 'Acceleration'
            self.ability1_maxcd = 180
            self.ability2_name = 'P U N C H'
            self.ability2_maxcd = 240
            self.ability3_name = ''
            font = pygame.font.Font(None, 40)
            if self.colour == 'blue':
                font_color = (0, 255, 240)
            else:
                font_color = (255, 10, 100)
            self.t = font.render("RAGE", True, font_color)
            self.t_rect = self.t.get_rect()
            if self.colour == 'blue':
                self.t_rect.left = 5
            else:
                self.t_rect.right = 995
            self.t_rect.centery = 425

            self.awakening_cnt += 1
            self.attack_damage = 2
            if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
                self.attack_damage = 3
                self.speed()
            if keystate[self.abkeys[1]] and not self.flag_ability and self.ability2_cd == 0 and self.flag_ability2 == 0:
                self.attackacount = 15
            if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
                self.punch()
            hits = pygame.sprite.spritecollide(self, self.enemygroup, False)
            for hit in hits:
                hit.hp -= 0.9
            if self.awakening_cnt >= 720:
                self.ability1_name = 'rat'
                self.ability1_maxcd = 480
                self.ability2_name = 'trick'
                self.ability2_maxcd = 480
                self.ability3_name = 'awakening'
                self.ability3_maxcd = 450
                self.awakening = False
                self.awakening_cnt = 0
                self.awakening_cd = 1
                self.awakening_phase = 2
                self.attack_damage = 1.5
                self.ability1_cd = 0
                self.ability2_cd = 0
                self.permspeed = 1
                self.flag_ability1 = False
                self.flag_ability2 = False
                self.flag_ability = False
        elif self.awakening_phase == 2:
            self.ability3_cd = self.awakening_cd
            self.ability1_name = 'epitaph'
            self.ability1_maxcd = 240
            self.ability2_name = 'dash'
            self.ability2_maxcd = 180
            self.ability3_name = 'awakening'
            self.ability3_maxcd = 900
            font = pygame.font.Font(None, 40)
            if self.colour == 'blue':
                font_color = (0, 255, 240)
            else:
                font_color = (255, 10, 100)
            self.t = font.render("Concentration", True, font_color)
            self.t_rect = self.t.get_rect()
            if self.colour == 'blue':
                self.t_rect.left = 5
            else:
                self.t_rect.right = 995
            self.t_rect.centery = 425
            if keystate[self.abkeys[0]] and not self.flag_ability and self.ability1_cd == 0 and self.flag_ability1 == 0:
                self.movement = []
                self.permhp = self.hp
            if keystate[self.abkeys[1]] and not self.flag_ability and self.ability2_cd == 0 and self.flag_ability2 == 0:
                self.permhp = self.hp
            if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
                self.epitaph()
            if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
                self.dash()
            if keystate[self.abkeys[2]] and not self.flag_ability and self.awakening_cd == 0:
                self.called_phrases.append(['It\'s time to be the [[BIG SHOT]]', self.rect.centerx, self.rect.y])
                self.awakening_sound.play()
                self.dash_hp = self.hp
                self.awakening_phase = 3
                self.awakening_cd = 1
                self.awakening_cnt = 0
                self.ability3_cd = 240
                self.flag_ability1 = False
        elif self.awakening_phase == 3:
            self.ability1_name = 'time erase'
            self.ability1_maxcd = 300
            self.ability2_name = 'dash'
            self.ability2_maxcd = 180
            self.ability3_name = '[ACT: OVERWRITE]'
            self.ability3_maxcd = 480
            self.attack_damage = 1
            font = pygame.font.Font(None, 40)
            if self.colour == 'blue':
                font_color = (0, 255, 240)
            else:
                font_color = (255, 10, 100)
            self.t = font.render("Full Concentration", True, font_color)
            self.t_rect = self.t.get_rect()
            if self.colour == 'blue':
                self.t_rect.left = 5
            else:
                self.t_rect.right = 995
            self.t_rect.centery = 425

            self.awakening_cnt += 1
            if self.awakening_cnt >= 900 and self.flag_ability3 == False:
                self.enemy.flag_ability = False
                self.awakening_cnt = 0
                self.flag_ability = False
                self.flag_ability1 = False
                self.flag_ability2 = False
                self.flag_ability3 = False
                self.awakening_phase = 2
                self.attack_damage = 1.5
                self.epitaph_cnt = 0
                self.awakening_cd = 1
            if keystate[self.abkeys[0]] and not self.flag_ability and not self.flag_ability1 and self.ability1_cd == 0:
                self.permhp = self.hp
                self.x = self.enemy.rect.x
            if keystate[self.abkeys[1]] and not self.flag_ability and not self.flag_ability2 and self.ability2_cd == 0:
                self.permhp = self.hp
            if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
                self.time_erase()
            if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
                self.invinc()
            if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
                self.ow7()

            if self.dash_hp - self.hp > 70:
                self.hp = self.dash_hp
                r = random.randint(1, 1000)
                while abs(r - self.rect.x) <= 200:
                    r = random.randint(1, 1000)
                self.rect.x = r
            if self.hp < self.dash_hp:
                a = random.randint(1, 3)
                if a == 1:
                    self.hp = self.dash_hp
                else:
                    self.dash_hp = self.hp
        if self.awakening == False:
            if self.ability1_cd != 0:
                self.ability1_cd += 1
                if self.ability1_cd >= 480:
                    self.ability1_cd = 0
            if self.ability2_cd != 0:
                self.ability2_cd += 1
                if self.ability2_cd >= 480:
                    self.ability2_cd = 0
            if self.awakening_cd != 0:
                self.awakening_cd += 1
                if self.awakening_cd >= 15 * 60:
                    self.awakening_cd = 0
        elif self.awakening_phase == 1:
            if self.ability1_cd != 0:
                self.ability1_cd += 1
                if self.ability1_cd >= 180:
                    self.ability1_cd = 0
            if self.ability2_cd != 0:
                self.ability2_cd += 1
                if self.ability2_cd >= 240:
                    self.ability2_cd = 0
        elif self.awakening_phase == 2:
            if self.ability1_cd != 0:
                self.ability1_cd += 1
                if self.ability1_cd >= 240:
                    self.ability1_cd = 0
            if self.ability2_cd != 0:
                self.ability2_cd += 1
                if self.ability2_cd >= 180:
                    self.ability2_cd = 0
            if self.awakening_cd != 0:
                self.awakening_cd += 1
                if self.awakening_cd >= 900:
                    self.awakening_cd = 0
        elif self.awakening_phase == 3:
            if self.ability1_cd != 0:
                self.ability1_cd += 1
                if self.ability1_cd >= 300:
                    self.ability1_cd = 0
            if self.ability2_cd != 0:
                self.ability2_cd += 1
                if self.ability2_cd >= 180:
                    self.ability2_cd = 0
            if self.ability3_cd != 0:
                self.ability3_cd += 1
                if self.ability3_cd >= 480:
                    self.ability3_cd = 0

        self.screen.blit(self.t, self.t_rect)

    def rat(self):
        self.flag_ability = True
        self.flag_ability1 = True
        if self.ability1_phase == 0:
            self.last = not self.last
            if self.last:
                self.rect.x = self.enemy.rect.x - 90
            else:
                self.rect.x = self.enemy.rect.x + 90
            self.called_phrases.append(['YOU\'RE SLOW', self.rect.centerx, self.rect.y])
            self.ability1_phase = 1
        elif self.ability1_phase == 1:
            self.canmove = False
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            img_dir = path.join(path.dirname(__file__), 'Assets')
            self.attackacount += 1
            if self.attackacount >= 30:
                if not self.atk_flag:
                    self.atk_sound.play()
                    self.atk_flag = True
                if self.last:
                    self.rect.x += 10
                else:
                    self.rect.x -= 10
            if self.last:
                self.image = pygame.image.load(
                    path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
            else:
                self.image = pygame.image.load(
                    path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
            self.attack()
            hits = pygame.sprite.spritecollide(self.attack_r, self.enemygroup, False)
            for hit in hits:
                if not self.enemy.blocking:
                    hit.hp -= 3
                else:
                    hit.blockdur -= 1
            if self.attackacount >= 44:
                self.ability1_phase = 2
        else:
            self.atk_flag = False
            self.enemy.blockdur = 45
            self.attackacount = 15
            self.canmove = True
            self.flag_ability1 = False
            self.ability1_cd = 1
            self.flag_ability = False
            self.ability1_phase = 0
            self.enemy.flag_ability = False
            self.enemy.canmove = True

    def trick(self):
        self.flag_ability = True
        self.flag_ability2 = True
        if self.ability2_phase == 1:
            if abs(self.rect.x - self.enemy.rect.x) < 250 and self.enemy.blocking == True:
                self.enemy.canmove = False
                self.enemy.flag_ability = True
                img_dir = path.join(path.dirname(__file__), 'Assets')
                if self.attackacount == 15:
                    self.called_phrases.append(['Got\'cha', self.rect.centerx, self.rect.y])
                self.attackacount += 1
                if self.attackacount >= 30:
                    if not self.atk_flag:
                        self.atk_sound.play()
                        self.atk_flag = True
                    if self.last:
                        self.rect.x += 15
                    else:
                        self.rect.x -= 15
                if self.last:
                    self.image = pygame.image.load(
                        path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
                else:
                    self.image = pygame.image.load(
                        path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
                self.attack()
                hits = pygame.sprite.spritecollide(self.attack_r, self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 10
                if self.attackacount >= 44:
                    self.ability2_phase = 2
            else:
                self.ability2_phase = 2
        elif self.ability2_phase == 2:
            self.flag_ability = False
            self.flag_ability2 = False
            self.enemy.canmove = True
            self.enemy.flag_ability = False
            self.attackacount = 15
            self.ability2_cd = 1
            self.ability2_phase = 1
            self.atk_flag = False

    def speed(self):
        if self.ability1 == 0:
            self.called_phrases.append(['ACCELERATE!', self.rect.centerx, self.rect.y])
            self.speed_sound.play()
        self.flag_ability1 = True
        self.permspeed = 2
        self.ability1 += 1
        if self.ability1 >= 420:
            self.permspeed = 1
            self.flag_ability1 = False
            self.ability1 = 0
            self.attack_damage = 2
            self.ability1_cd = 1

    def punch(self):
        self.flag_ability = True
        self.flag_ability2 = True
        self.canmove = False
        if not self.punch_flag:
            img_dir = path.join(path.dirname(__file__), 'Assets')
            if self.attackacount == 15:
                self.called_phrases.append(['YOU\'RE ANNOYING', self.rect.centerx, self.rect.y])
            self.attackacount += 1
            if self.attackacount >= 30:
                if not self.atk_flag:
                    self.atk_sound.play()
                    self.atk_flag = True
                if self.last:
                    self.rect.x += 10
                else:
                    self.rect.x -= 10
            if self.last:
                self.image = pygame.image.load(
                    path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
            else:
                self.image = pygame.image.load(
                    path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
            self.attack()

            hits = pygame.sprite.spritecollide(self.attack_r, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking:
                    hit.hp -= 70
                    self.punch_flag = 1
                    self.atk_sound.play()
                else:
                    hit.blockdur = 0
                    self.punch_flag = 2
            if self.attackacount >= 44:
                self.punch_flag = 3
        elif self.punch_flag == 1:
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            if self.last:
                self.enemy.rect.x += 10
            else:
                self.enemy.rect.x -= 10
            self.punch_cnt += 1
            if self.punch_cnt >= 45:
                self.punch_flag = 3
        elif self.punch_flag == 2:
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            if self.last:
                self.enemy.rect.x += 4
            else:
                self.enemy.rect.x -= 4
            self.punch_cnt += 1
            if self.punch_cnt >= 45:
                self.punch_flag = 3
        else:
            self.atk_flag = False
            self.punch_cnt = 0
            self.punch_flag = 0
            self.enemy.flag_ability = False
            self.canmove = True
            self.flag_ability = False
            self.flag_ability2 = False
            self.ability2_cd = 1
            self.attackacount = 15

    def epitaph(self):
        self.flag_ability1 = True
        if self.epitaph_phase == 1:
            if self.epitaph_cnt == 0:
                self.epitaph_sound1.play()
                self.called_phrases.append(['And now I see where you go', self.rect.centerx, self.rect.y])
            self.movement.append(self.enemy.rect.x)
            self.epitaph_cnt += 1
            self.hp = self.permhp
            if self.epitaph_cnt >= 120:
                self.epitaph_phase = 2
                self.epitaph_cnt = 0
        elif self.epitaph_phase == 2:
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            self.enemy.rect.x = self.movement[self.epitaph_cnt]
            if self.epitaph_cnt == 0:
                self.epitaph_sound2.play()
            self.epitaph_cnt += 1
            if self.epitaph_cnt >= 120:
                self.epitaph_phase = 3
        else:
            self.ability1_cd = 1
            self.epitaph_cnt = 0
            self.epitaph_phase = 1
            self.enemy.canmove = True
            self.flag_ability = False
            self.enemy.flag_ability = False
            self.movement = []
            self.flag_ability1 = False

    def dash(self):
        self.canmove = False
        self.flag_ability = True
        self.flag_ability2 = True
        self.hp = self.permhp
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.animcount == 1:
            self.dash_sound.play()
            self.called_phrases.append(['I\'m outta here', self.rect.centerx, self.rect.y])
        self.animcount += 1
        if not self.last:
            self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_{self.animcount // 9}.png')).convert()
        else:
            self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_{self.animcount // 9}.png')).convert()
        if self.last:
            self.right = True
            self.left = False
            self.rect.x += 12
            self.image.set_colorkey((255, 255, 255))
        else:
            self.right = False
            self.left = True
            self.rect.x -= 12
            self.image.set_colorkey((255, 255, 255))
        self.animcount += 1
        if self.animcount + 1 >= 60:
            self.animcount = 1
            self.flag_ability2 = False
            self.ability2_cd = 1
            self.flag_ability = False

    def time_erase(self):
        self.flag_ability1 = True
        if self.te_phase == 0:
            self.te_sound1.play()
            self.called_phrases.append(['There you go', self.rect.centerx, self.rect.y])
            if 1000 - self.enemy.rect.centerx > 500:
                self.enemy.last = True
            else:
                self.enemy.last = False
            self.te_phase = 1
        elif self.te_phase == 1:
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            self.enemy.blockdur = -1
            if self.enemy.last == True:
                self.x += 1
            else:
                self.x -= 1
            self.hp = self.permhp
            self.enemy.rect.x = self.x
            self.te += 1
            if self.te >= 360:
                self.te_sound2.play()
                self.te = 0
                self.te_phase = 0
                self.flag_ability1 = False
                self.enemy.flag_ability = False
                self.enemy.blockdur = 45

    def invinc(self):
        self.flag_ability2 = True
        if self.invinc_cnt == 0:
            self.invinc_sound.play()
            self.called_phrases.append(['I\'m invincible now', self.rect.centerx, self.rect.y])
        self.invinc_cnt += 1
        self.hp = self.permhp
        if self.invinc_cnt == 240:
            self.invinc_cnt = 0
            self.flag_ability2 = False
            self.ability2_cd = 1

    def ow7(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.flag_ability3 = True
        if self.ability3_phase == 0:
            if abs(self.rect.centerx - self.enemy.rect.centerx) < 300:
                self.called_phrases.append(['This is where the fun begins', self.rect.centerx, self.rect.y])
                self.rect.x = 100
                self.enemy.rect.x = 500
                self.rect.centery = 400
                self.enemy.rect.centery = 400
                for i in range(10):
                    image = pygame.image.load(path.join(img_dir, 'knife1.png')).convert()
                    image.set_colorkey((0, 0, 0))
                    s = pygame.sprite.Sprite()
                    s.image = image
                    s.rect = s.image.get_rect()
                    s.rect.y = self.rect.bottomleft[1] - 5 - i * 10
                    s.rect.x = self.rect.x + 100 + 30
                    self.knifes_left.append(s)
                for i in range(10):
                    image = pygame.image.load(path.join(img_dir, 'knife2.png')).convert()
                    image.set_colorkey((0, 0, 0))
                    s = pygame.sprite.Sprite()
                    s.image = image
                    s.rect = s.image.get_rect()
                    s.rect.x = 500 + 85 + 200
                    s.rect.y = self.rect.bottomleft[1] - 5 - i * 10
                    self.knifes_right.append(s)
                self.canmove = False
                self.enemy.canmove = False
                self.flag_ability = True
                self.enemy.flag_ability = True
                self.ability3_phase = 1
            else:
                self.ability3_phase = 200
        elif self.ability3_phase == 1:
            pygame.transform.flip(self.image, False, True)
            pygame.transform.flip(self.enemy.image, False, True)
            self.image.set_colorkey((255, 255, 255))
            #self.enemy.image.set_colorkey((255, 255, 255))
            self.nebo.rect.x, self.nebo.rect.y = 0, 0
            self.screen.blit(self.nebo.image, self.nebo.rect)
            self.screen.blit(self.image, self.rect)
            self.screen.blit(self.enemy.image, self.enemy.rect)
            self.ult_cnt += 1
            if self.ult_cnt >= 90:
                self.ability3_phase = 2
                self.ult_cnt = 0
        elif self.ability3_phase == 2:
            pygame.transform.flip(self.image, False, True)
            pygame.transform.flip(self.enemy.image, False, True)
            self.image.set_colorkey((255, 255, 255))
            self.enemy.image.set_colorkey((255, 255, 255))
            #self.nebo.image = pygame.image.load(path.join(img_dir, 'nebo.png')).convert()
            #self.nebo.rect = self.nebo.image.get_rect()
            self.nebo.rect.x, self.nebo.rect.y = 0, 0
            self.screen.blit(self.nebo.image, self.nebo.rect)
            self.screen.blit(self.image, self.rect)
            self.screen.blit(self.enemy.image, self.enemy.rect)
            for s in self.knifes_left:
                self.screen.blit(s.image, s.rect)
            self.ult_cnt += 1
            if self.ult_cnt >= 90:
                self.ability3_phase = 3
        elif self.ability3_phase == 3:
            global HEIGHT
            self.enemy.rect.centery = HEIGHT - 100
            self.rect.centery = HEIGHT - 100
            i = 0
            for s in self.knifes_right:
                s.rect.y = self.rect.bottomleft[1] - 5 - i * 10
                i += 1
            i = 0
            for s in self.knifes_left:
                s.rect.y = self.rect.bottomleft[1] - 5 - i * 10
                i += 1
            pygame.transform.flip(self.image, False, True)
            pygame.transform.flip(self.enemy.image, False, True)
            self.image.set_colorkey((255, 255, 255))
            self.enemy.image.set_colorkey((255, 255, 255))
            self.nebo.image = pygame.image.load(path.join(img_dir, 'nebo.png')).convert()
            self.nebo.rect = self.nebo.image.get_rect()
            self.nebo.rect.x, self.nebo.rect.y = 0, 0
            self.screen.blit(self.nebo.image, self.nebo.rect)
            self.screen.blit(self.image, self.rect)
            self.screen.blit(self.enemy.image, self.enemy.rect)
            for s in self.knifes_left:
                self.screen.blit(s.image, s.rect)
            for s in self.knifes_right:
                self.screen.blit(s.image, s.rect)
            self.rect.x = 100
            self.enemy.rect.x = 500
            self.ability3_phase = 4
            self.ult_cnt = 0
        elif self.ability3_phase == 4:
            self.canmove = False
            self.enemy.canmove = False
            self.flag_ability = True
            self.enemy.flag_ability = True
            self.rect.x = 100
            self.enemy.rect.x = 500
            self.ult_cnt += 1
            if self.ult_cnt % 7 == 0:
                self.ow7_sound.play()
                self.knifes_amount += 1
                a = random.randint(1, 2)
                if a == 1:
                    for i in range(3):
                        a = random.randint(0, 9)
                        self.moving_right.append(self.knifes_left[a])
                        self.knifes_left.pop(a)
                        image = pygame.image.load(path.join(img_dir, 'knife1.png')).convert()
                        image.set_colorkey((0, 0, 0))
                        s = pygame.sprite.Sprite()
                        s.image = image
                        s.rect = s.image.get_rect()
                        s.rect.y = self.moving_right[-1].rect.y
                        s.rect.x = self.moving_right[-1].rect.x
                        self.knifes_left.append(s)
                else:
                    for i in range(3):
                        a = random.randint(0, 9)
                        self.moving_left.append(self.knifes_right[a])
                        self.knifes_right.pop(a)
                        image = pygame.image.load(path.join(img_dir, 'knife2.png')).convert()
                        image.set_colorkey((0, 0, 0))
                        s = pygame.sprite.Sprite()
                        s.image = image
                        s.rect = s.image.get_rect()
                        s.rect.x = self.moving_left[-1].rect.x
                        s.rect.y = self.moving_left[-1].rect.y
                        self.knifes_right.append(s)
            i = 0
            while i < len(self.moving_right):
                self.moving_right[i].rect.x += 20
                self.screen.blit(self.moving_right[i].image, self.moving_right[i].rect)
                hits = pygame.sprite.spritecollide(self.moving_right[i], self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 0.1
                if self.moving_right[i].rect.x >= 800:
                    del self.moving_right[i]
                i += 1

            i = 0
            while i < len(self.moving_left):
                self.moving_left[i].rect.x -= 20
                self.screen.blit(self.moving_left[i].image, self.moving_left[i].rect)
                hits = pygame.sprite.spritecollide(self.moving_left[i], self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 0.1
                if self.moving_left[i].rect.x >= 800:
                    del self.moving_left[i]
                i += 1
            for knife in self.knifes_right:
                self.screen.blit(knife.image, knife.rect)
            for knife in self.knifes_left:
                self.screen.blit(knife.image, knife.rect)
            if self.ult_cnt >= 420:
                self.ability3_phase = 5
        elif self.ability3_phase == 5:
            for knife in self.knifes_left:
                knife.rect.x += 20
                if knife.rect.x >= 800:
                    self.ability3_phase = 200
                hits = pygame.sprite.spritecollide(knife, self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 0.2
                self.screen.blit(knife.image, knife.rect)

            for knife in self.knifes_right:
                knife.rect.x -= 20
                if knife.rect.x <= 20:
                    self.ability3_phase = 200
                hits = pygame.sprite.spritecollide(knife, self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 0.2
                self.screen.blit(knife.image, knife.rect)
            for knife in self.knifes_left:
                knife.rect.x += 20
                if knife.rect.x >= 800:
                    self.ability3_phase = 200
                hits = pygame.sprite.spritecollide(knife, self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 0.5
                self.screen.blit(knife.image, knife.rect)
        else:
            self.canmove = True
            self.enemy.canmove = True
            self.flag_ability = False
            self.enemy.flag_ability = False
            self.flag_ability3 = False
            self.ability3_cd = 1
            self.ult_cnt = 0
            self.ability3_phase = 0
            self.knifes_left = []
            self.knifes_right = []
            self.moving_left = []
            self.moving_right = []
class Georg(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Georg'
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability3_cd = 0
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.ability1_name = 'fire'
        self.ability1_maxcd = 720
        self.ability2_name = 'chaos, chaos'
        self.ability2_maxcd = 900
        self.ability3_name = 'TRAIN'
        self.ability3_maxcd = 1200
        self.flag_ability1 = False
        self.ability1 = 0
        self.ability2 = 0
        self.flag_ability2 = False
        self.ability2_phase = 0
        self.main_bullet = pygame.sprite.Sprite()
        self.main_bullet.image = pygame.Surface((30, 30))
        self.main_bullet.rect = self.main_bullet.image.get_rect()
        self.big_bullet = pygame.sprite.Sprite()
        self.big_bullet.image = pygame.Surface((250, 166))
        self.big_bullet.rect = self.big_bullet.image.get_rect()
        self.big_bullet.rect.x = 1350
        self.big_bullet.rect.y = 950
        self.bcolour = 0
        self.flag_ability3 = False
        self.ability3 = 0
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.fire_sound = pygame.mixer.Sound(file=path.join(img_dir, 'fire.wav'))
        self.chaos_sound1 = pygame.mixer.Sound(file=path.join(img_dir, 'chaos-1.wav'))
        self.chaos_sound2 = pygame.mixer.Sound(file=path.join(img_dir, 'chaos-2.wav'))
        self.train_sound1 = pygame.mixer.Sound(file=path.join(img_dir, 'train-1.wav'))
        self.train_sound2 = pygame.mixer.Sound(file=path.join(img_dir, 'train-2.wav'))
        self.ability1_desc = 'огонь. фатальный ближний урон'
        self.ability2_desc = 'запускает вверх огромный сгусток хаоса. потом с неба летят мелкие сгустки хаоса. большой урон'
        self.ability3_desc = 'ЛЕТИТ И УБИВАЕТ ОГРОМНЫЙ ФАТАЛЬНЫЙ УЖАСНЫЙ УРОН. но только если вобьет врага в стенку'
        self.chr_desc = 'все способности Георга наносят огромный урон, но имеют большой откат'
    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
            self.fire()
        if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
            self.chaos()
        if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
            self.train()

        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 720:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 900:
                self.ability2_cd = 0
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= 1200:
                self.ability3_cd = 0

    def fire(self):
        self.flag_ability = True
        self.flag_ability1 = True
        self.canmove = False
        if self.ability1 == 0:
            self.fire_sound.play()
            self.called_phrases.append(['My fire.', self.rect.centerx, self.rect.y])
        self.ability1 += 1
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.last:
            img_dir = path.join(img_dir, 'fire-right')
        else:
            img_dir = path.join(img_dir, 'fire-left')
        xd = str(self.ability1 % 60)
        if int(xd) < 10:
            xd = '0' + xd
        if self.ability1 == 1:
            self.fires = pygame.sprite.Sprite()
            self.fires.image = pygame.image.load(path.join(img_dir, f'frame_{xd}_delay-0.02s.gif'))
            self.fires.image.set_colorkey((0, 0, 0))
            self.fires.rect = self.fires.image.get_rect()
            if self.last:
                self.fires.rect.x = self.rect.x + 85 + 3
            else:
                self.fires.rect.x = self.rect.x - 75 - 3
        self.fires.image = pygame.image.load(path.join(img_dir, f'frame_{xd}_delay-0.02s.gif'))
        self.fires.image.set_colorkey((0, 0, 0))
        self.fires.rect.centery = self.rect.centery
        if self.last:
            self.fires.rect.x += 1
        else:
            self.fires.rect.x -= 1
        self.screen.blit(self.fires.image, self.fires.rect)
        hits = pygame.sprite.spritecollide(self.fires, self.enemygroup, False)
        for hit in hits:
            hit.hp -= 10
        if self.ability1 >= 90:
            self.ability1 = 0
            self.flag_ability1 = False
            self.flag_ability = False
            self.canmove = True
            self.ability1_cd = 1

    def chaos(self):
        self.flag_ability2 = True
        self.flag_ability = True
        if self.ability2_phase == 0:
            self.big_bullet.rect.centerx = self.rect.centerx
            self.big_bullet.rect.y = self.rect.y - 205
            self.chaos_sound1.play()
            self.called_phrases.append(['CHAOS, CHAOS', self.rect.centerx, self.rect.y])
            self.ability2_phase = 1
        if self.ability2_phase == 1:
            self.canmove = False
            self.big_bullet.rect.y -= 3
            self.big_bullet.image.fill((self.bcolour, self.bcolour, self.bcolour))
            self.bcolour = 255 - self.bcolour
            self.screen.blit(self.big_bullet.image, self.big_bullet.rect)
            if self.big_bullet.rect.centery - 100 <= 10:
                self.ability2_phase = 2
                self.canmove = True
        if self.ability2_phase == 2:
            self.canmove = True
            self.flag_ability = False
            if self.ability2 >= 990:
                self.ability2_phase = 3
            elif self.ability2 % 66 == 0:
                self.main_bullet.rect.x = random.randint(1, 1000)
                self.main_bullet.rect.y = 10
                self.chaos_sound2.play()
            else:
                self.main_bullet.rect.y += 15
            self.ability2 += 1
            # print(self.main_bullet.rect.center)
            self.main_bullet.image.fill((self.bcolour, self.bcolour, self.bcolour))
            self.bcolour = 255 - self.bcolour
            self.screen.blit(self.main_bullet.image, self.main_bullet.rect)
            hits = pygame.sprite.spritecollide(self.main_bullet, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 12.5
                else:
                    hit.blockdur -= 1
        if self.ability2_phase == 3:
            self.flag_ability = False
            self.flag_ability2 = False
            self.ability2 = 0
            self.ability2_phase = 0
            self.ability2_cd = 1

    def train(self):
        self.flag_ability3 = True
        self.flag_ability = True
        self.attacking = False
        if self.ability3 == 0:
            self.called_phrases.append(['WARNING, I\'M COMING', self.rect.centerx, self.rect.y])
            self.train_sound1.play()
        self.ability3 += 1
        if self.last:
            if self.ability3 <= 61 and self.enemy.rect.x + 85 < 1000:
                self.rect.x += 10
                hits = pygame.sprite.spritecollide(self, self.enemygroup, False)
                for hit in hits:
                    hit.rect.x += 10
                    hit.canmove = False
                    hit.flag_ability = True
                    hit.hp -= 2
            elif self.enemy.rect.x + 85 >= 1000:
                self.ability3 = 0
                self.flag_ability3 = False
                self.flag_ability = False
                self.ability3_cd = 1
                self.ability1_cd = 420
                self.enemy.hp -= min(350 - 4 * self.ability3, 250)
                self.enemy.canmove = True
                self.enemy.flag_ability = False
                self.train_sound2.play()
        else:
            if self.ability3 <= 61 and self.enemy.rect.x > 0:
                self.rect.x -= 10
                hits = pygame.sprite.spritecollide(self, self.enemygroup, False)
                for hit in hits:
                    hit.rect.x -= 10
                    hit.canmove = False
                    hit.flag_ability = True
                    hit.hp -= 2


            elif self.enemy.rect.x <= 0:
                self.ability3 = 0
                self.flag_ability3 = False
                self.flag_ability = False
                self.ability3_cd = 1
                self.ability1_cd = 420
                self.enemy.hp -= min(350 - 4 * self.ability3, 250)
                self.enemy.canmove = True
                self.enemy.flag_ability = False
                self.train_sound2.play()
        if self.ability3 > 61:
            self.ability3 = 0
            self.flag_ability3 = False
            self.flag_ability = False
            self.ability3_cd = 1
            self.ability1_cd = 420
            self.enemy.canmove = True
            self.enemy.flag_ability = False
class Bogdan(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Bogdan'
        self.screen = screen
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability3_cd = 0
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.ability1_name = 'random teleport'
        self.ability1_maxcd = 180
        self.ability2_name = 'gravity distortion'
        self.ability2_maxcd = 180
        self.ability3_name = ''
        self.attack_damage = 2
        self.ability2 = 0
        self.ab2_flag = False
        self.flag_ability2 = False
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.tp_sound = pygame.mixer.Sound(file=path.join(img_dir, 'teleport.wav'))
        self.gravity_sound = pygame.mixer.Sound(file=path.join(img_dir, 'gravity.wav'))
        self.ability3_maxcd = 0
        self.ability1_desc = 'рандомная телепортация'
        self.ability2_desc = 'гравитация искажается. надо было богдану лучше физику учить. не дает врагу ходить'
        self.ability3_desc = ''
        self.chr_desc = 'Богдан ничего не учит, но тут у него от этого большие преимущества'


    def update2(self):
        keystate = pygame.key.get_pressed()
        if keystate[self.abkeys[0]] and not self.flag_ability and self.ability1_cd == 0:
            self.tp()
        if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
            self.stun()

        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 180:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 180:
                self.ability2_cd = 0

    def tp(self):
        self.called_phrases.append(['bye lol', self.rect.centerx, self.rect.y])
        self.rect.x = random.randint(1, 1000)
        self.ability1_cd = 1
        self.tp_sound.play()

    def stun(self):
        self.enemy.canmove = False
        self.enemy.blockdur = -1
        self.enemy.flag_ability = True
        self.flag_ability2 = True
        self.enemy.rect.y = self.rect.y + 15
        if self.ab2_flag:
            self.enemy.rect.y += 2
        else:
            self.enemy.rect.y -= 2
        self.ab2_flag = not self.ab2_flag
        if self.ability2 == 0:
            self.gravity_sound.play()
            self.called_phrases.append(['And now you\'re down', self.rect.centerx, self.rect.y])
        self.ability2 += 1
        if self.ability2 == 180:
            self.enemy.rect.y = self.rect.y
            self.ability2 = 0
            self.flag_ability2 = False
            self.ability2_cd = 1
            self.enemy.blockdur = 45
            self.enemy.canblock = True
            self.enemy.dur = 0
            self.enemy.canmove = True
            self.enemy.flag_ability = False
class Grisha(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Grisha'
        self.screen = screen
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability3_cd = 0
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.ability1_name = 'shield'
        self.ability1_maxcd = 480
        self.ability2_name = 'strong punch'
        self.ability2_maxcd = 180
        self.ability3_name = 'ZA WARUDO'
        self.ability3_maxcd = 1200
        self.permhp = 0
        self.ability1 = 0
        self.flag_ability1 = False
        self.flag_ability2 = False
        self.flag_ability3 = False
        self.ability3 = 0
        self.ab3_permhp = 0
        self.ab3_difference = 0
        img_dir = path.join(path.dirname(__file__), 'Assets')
        # self.shield_flag = False
        self.shield_sound = pygame.mixer.Sound(file=path.join(img_dir, 'shield.wav'))
        self.atk_2_flag = False
        self.atk_2_sound = pygame.mixer.Sound(file=path.join(img_dir, 'hitHurt.wav'))
        self.timestop_sound = pygame.mixer.Sound(file=path.join(img_dir, 'timestop.wav'))
        self.ability1_desc = 'щит. защищает от любого урона'
        self.ability2_desc = 'сильный ближний удар. большой урон если начинать удар близко к врагу(но не в упор)'
        self.ability3_desc = 'остановка времени'
        self.chr_desc = 'без таймстопа он почти ничего не сделает.'

    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
            self.shield()
        if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
            self.atk_2()
        if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
            self.timestop()
        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 480:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 180:
                self.ability2_cd = 0
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= 1200:
                self.ability3_cd = 0

    def shield(self):
        self.flag_ability = True
        self.flag_ability1 = True
        self.canmove = False
        if self.ability1 == 0:
            self.permhp = self.hp
            self.shield_sound.play()
            self.called_phrases.append(['HAHAHAHA LOOK AT YOU', self.rect.centerx, self.rect.y])
        self.hp = self.permhp
        self.ability1 += 1
        if self.ability1 == 240:
            self.ability1 = 0
            self.permhp = 0
            self.flag_ability = False
            self.flag_ability1 = False
            self.canmove = True
            self.ability1_cd = 1

    def atk_2(self):
        self.canmove = False
        self.flag_ability = True
        self.flag_ability2 = True
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.attackacount == 15:
            self.called_phrases.append(['YOU\'RE DEAD', self.rect.centerx, self.rect.y])
        self.attackacount += 1
        if self.attackacount >= 30:
            if not self.atk_2_flag:
                self.atk_2_sound.play()
                self.atk_2_flag = True
            if self.last:
                self.rect.x += 20
            else:
                self.rect.x -= 20
        if self.last:
            self.image = pygame.image.load(
                path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
        else:
            self.image = pygame.image.load(
                path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
        self.attack()
        hits = pygame.sprite.spritecollide(self.attack_r, self.enemygroup, False)
        for hit in hits:
            if not hit.blocking or hit.blockdur <= 0:
                hit.hp -= 5
            else:
                hit.blockdur -= 1
        if self.attackacount >= 44:
            self.atk_2_flag = False
            self.attackacount = 15
            self.canmove = True
            self.flag_ability2 = False
            self.ability2_cd = 1
            self.flag_ability = False

    def timestop(self):
        self.enemy.canmove = False
        self.enemy.flag_ability = True
        self.enemy.blockdur = -1
        self.flag_ability3 = True
        if self.ability3 == 0:
            self.ab3_permhp = self.enemy.hp
            self.timestop_sound.play()
            if self.hp < 200:
                self.called_phrases.append(['THIS TIME IS MIIIIINE!', self.rect.centerx, self.rect.y])
            else:
                self.called_phrases.append(['THE WORLD!', self.rect.centerx, self.rect.y])

        self.ability3 += 1
        if self.enemy.hp < self.ab3_permhp:
            self.ab3_difference += (self.ab3_permhp - self.enemy.hp)
            self.enemy.hp = self.ab3_permhp
        if self.ability3 == 300:
            self.enemy.canmove = True
            self.enemy.flag_ability = False
            self.flag_ability3 = False
            self.ability3 = 0
            self.enemy.hp -= self.ab3_difference
            self.ab3_permhp = 0
            self.ab3_difference = 0
            self.ability3_cd = 1
class Nikita_Dev(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Nikita_Dev'
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, self.screen, colour)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.flag_ability1 = False
        self.ability1_phase = 1
        self.ability1 = 0
        self.ability1_cd = 0
        self.flag_ability2 = False
        self.ability2 = 0
        self.ability2_cd = 0
        self.ability2_phase = 1
        self.a2flag1 = True
        self.a2flag2 = True
        self.a2flag3 = True
        self.flag_ability3 = False
        self.ability3 = 0
        self.ability3_cd = 0

        self.it = pygame.sprite.Sprite()
        self.it.image = pygame.image.load(path.join(img_dir, 'it.png')).convert()
        self.it.rect = self.it.image.get_rect()
        self.it.rect.x = 0
        self.it.rect.y = 0

    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
            self.ow5()
        if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
            self.knifes()
        if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
            self.ult()
        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 600:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 300:
                self.ability2_cd = 0
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= 300:
                self.ability3_cd = 0

    def ow5(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.flag_ability = True
        self.flag_ability1 = True
        self.canmove = False
        if self.ability1_phase == 1:
            self.ability1 += 1
            if self.last:
                a = 95
                xd = 1
            else:
                a = -95
                xd = 2
            if self.ability1 == 90:
                self.ability1 = 0
                self.ability1_phase = 2
            self.friend1 = pygame.sprite.Sprite()
            self.friend1.image = pygame.image.load(path.join(img_dir, f'{self.colour}{xd}_0.png')).convert()
            self.friend1.rect = self.friend1.image.get_rect()
            if self.last:
                self.friend1.rect.x = self.rect.x - a - a
            else:
                self.friend1.rect.x = self.rect.x + a + a
            self.friend1.rect.y = self.rect.y
            self.friend2 = pygame.sprite.Sprite()
            self.friend2.image = pygame.image.load(path.join(img_dir, f'{self.colour}{xd}_0.png')).convert()
            self.friend2.rect = self.friend2.image.get_rect()
            if self.last:
                self.friend2.rect.x = self.rect.x - a
            else:
                self.friend2.rect.x = self.rect.x + a
            self.friend2.rect.y = self.rect.y + 50
            self.friend3 = pygame.sprite.Sprite()
            self.friend3.image = pygame.image.load(path.join(img_dir, f'{self.colour}{xd}_0.png')).convert()
            self.friend3.rect = self.friend3.image.get_rect()
            if self.last:
                self.friend3.rect.x = self.rect.x - a
            else:
                self.friend3.rect.x = self.rect.x + a
            self.friend3.rect.y = self.rect.y - 50
            self.friend1.image.set_colorkey((255, 255, 255))
            self.friend2.image.set_colorkey((255, 255, 255))
            self.friend3.image.set_colorkey((255, 255, 255))
            self.screen.blit(self.friend3.image, self.friend3.rect)
            self.screen.blit(self.friend1.image, self.friend1.rect)
            self.screen.blit(self.friend2.image, self.friend2.rect)
        if self.ability1_phase == 2:
            if self.last:
                if self.enemy.rect.x < self.rect.x:
                    self.ability1_phase = 5
                else:
                    self.friend3.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_0.png')).convert()
                    self.friend3.image.set_colorkey((255, 255, 255))
                    self.enemy.canmove = False
                    self.enemy.flag_ability = True
                    self.friend3.rect.x = self.enemy.rect.x + 85 + 10
                    self.ability1 += 1
                    if self.ability1 == 30:
                        self.ability1_phase = 3
                        self.ability1 = 0
                    self.screen.blit(self.friend3.image, self.friend3.rect)
                    self.screen.blit(self.friend1.image, self.friend1.rect)
                    self.screen.blit(self.friend2.image, self.friend2.rect)
            else:
                if self.enemy.rect.x > self.rect.x:
                    self.ability1_phase = 5
                else:
                    self.friend3.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_0.png')).convert()
                    self.friend3.image.set_colorkey((255, 255, 255))
                    self.enemy.canmove = False
                    self.enemy.flag_ability = True
                    self.friend3.rect.x = self.enemy.rect.x - 85 - 10
                    self.ability1 += 1
                    if self.ability1 == 30:
                        self.ability1_phase = 3
                        self.ability1 = 0
                    self.screen.blit(self.friend3.image, self.friend3.rect)
                    self.screen.blit(self.friend1.image, self.friend1.rect)
                    self.screen.blit(self.friend2.image, self.friend2.rect)
        if self.ability1_phase == 3:
            self.rhand = pygame.sprite.Sprite()
            self.lhand = pygame.sprite.Sprite()
            if self.last:
                self.rhand.image = pygame.image.load(path.join(img_dir, 'right_hand.png')).convert()
                self.lhand.image = pygame.image.load(path.join(img_dir, 'left_hand.png')).convert()
            else:
                self.rhand.image = pygame.image.load(path.join(img_dir, 'right_hand2.png')).convert()
                self.lhand.image = pygame.image.load(path.join(img_dir, 'left_hand2.png')).convert()
            self.rhand.rect = self.rhand.image.get_rect()
            self.lhand.rect = self.lhand.image.get_rect()
            self.rhand.image.set_colorkey((255, 255, 255))
            self.lhand.image.set_colorkey((255, 255, 255))
            if self.last:
                self.rhand.rect.x = self.friend1.rect.x - 10
                self.rhand.rect.y = self.friend1.rect.y - 42.5 - 15
                self.lhand.rect.x = self.friend1.rect.x - 40 - 10 - 30
                self.lhand.rect.y = self.friend1.rect.y - 15 + 30
            else:
                self.rhand.rect.x = self.friend1.rect.x + 42.5 - 10
                self.rhand.rect.y = self.friend1.rect.y - 35 - 10
                self.lhand.rect.x = self.friend1.rect.x + 85 + 10 + 10
                self.lhand.rect.y = self.friend1.rect.y - 10
            self.blaster1 = pygame.sprite.Sprite()
            self.blaster2 = pygame.sprite.Sprite()
            self.blaster3 = pygame.sprite.Sprite()
            self.blaster1.image = pygame.image.load(path.join(img_dir, 'blaster.png')).convert()
            self.blaster2.image = pygame.image.load(path.join(img_dir, 'blaster.png')).convert()
            self.blaster3.image = pygame.image.load(path.join(img_dir, 'blaster.png')).convert()
            self.blaster1.image.set_colorkey((246, 246, 246))
            self.blaster2.image.set_colorkey((246, 246, 246))
            self.blaster3.image.set_colorkey((246, 246, 246))
            self.blaster1.rect = self.blaster1.image.get_rect()
            self.blaster2.rect = self.blaster1.image.get_rect()
            self.blaster3.rect = self.blaster1.image.get_rect()
            self.blaster2.rect.centerx = self.enemy.rect.centerx
            self.blaster2.rect.y = self.enemy.rect.y - 41 - 10
            self.blaster1.rect.x = self.blaster2.rect.x - 30 - 5
            self.blaster1.rect.y = self.enemy.rect.y - 41 - 10
            self.blaster3.rect.x = self.blaster2.rect.x + 30 + 5
            self.blaster3.rect.y = self.enemy.rect.y - 41 - 10
            self.bone1 = pygame.sprite.Sprite()
            self.bone2 = pygame.sprite.Sprite()
            self.bone3 = pygame.sprite.Sprite()
            self.bone1.image = pygame.image.load(path.join(img_dir, 'bone.png')).convert()
            self.bone2.image = self.bone1.image
            self.bone3.image = self.bone1.image
            self.bone1.image.set_colorkey((255, 255, 255))
            self.bone2.image.set_colorkey((255, 255, 255))
            self.bone3.image.set_colorkey((255, 255, 255))
            self.bone1.rect = self.bone1.image.get_rect()
            self.bone2.rect = self.bone2.image.get_rect()
            self.bone3.rect = self.bone3.image.get_rect()
            if self.last:
                self.bone1.rect.x = self.enemy.rect.x + 85 + 5
                self.bone2.rect.x = self.enemy.rect.x + 85 + 5
                self.bone3.rect.x = self.enemy.rect.x + 85 + 5
            else:
                self.bone1.rect.x = self.enemy.rect.x - 30 - 5
                self.bone2.rect.x = self.enemy.rect.x - 30 - 5
                self.bone3.rect.x = self.enemy.rect.x - 30 - 5

            self.bone1.rect.y = self.enemy.rect.y
            self.bone2.rect.y = self.enemy.rect.y + 28
            self.bone3.rect.y = self.bone2.rect.y + 28
            self.screen.blit(self.rhand.image, self.rhand.rect)
            self.screen.blit(self.lhand.image, self.lhand.rect)
            self.screen.blit(self.blaster1.image, self.blaster1.rect)
            self.screen.blit(self.blaster2.image, self.blaster2.rect)
            self.screen.blit(self.blaster3.image, self.blaster3.rect)
            self.screen.blit(self.bone3.image, self.bone3.rect)
            self.screen.blit(self.bone2.image, self.bone2.rect)
            self.screen.blit(self.bone1.image, self.bone1.rect)
            self.screen.blit(self.friend1.image, self.friend1.rect)
            self.screen.blit(self.friend2.image, self.friend2.rect)
            self.screen.blit(self.friend3.image, self.friend3.rect)
            self.ability1 += 1
            if self.ability1 == 30:
                self.ability1 = 0
                self.ability1_phase = 4
        if self.ability1_phase == 4:
            self.screen.blit(self.rhand.image, self.rhand.rect)
            self.screen.blit(self.lhand.image, self.lhand.rect)
            self.screen.blit(self.blaster1.image, self.blaster1.rect)
            self.screen.blit(self.blaster2.image, self.blaster2.rect)
            self.screen.blit(self.blaster3.image, self.blaster3.rect)
            self.screen.blit(self.bone3.image, self.bone3.rect)
            self.screen.blit(self.bone2.image, self.bone2.rect)
            self.screen.blit(self.bone1.image, self.bone1.rect)
            self.screen.blit(self.friend1.image, self.friend1.rect)
            self.screen.blit(self.friend2.image, self.friend2.rect)
            self.screen.blit(self.friend3.image, self.friend3.rect)
            self.lhand_blaster = pygame.sprite.Sprite()
            self.rhand_blaster = pygame.sprite.Sprite()
            self.b1_laser = pygame.sprite.Sprite()
            self.b2_laser = pygame.sprite.Sprite()
            self.b3_laser = pygame.sprite.Sprite()
            self.lhand_blaster.image = pygame.Surface((1000, 90))
            self.rhand_blaster.image = pygame.Surface((1000, 90))
            self.lhand_blaster.image.fill((255, 0, 0))
            self.rhand_blaster.image.fill((255, 0, 0))
            self.lhand_blaster.rect = self.lhand_blaster.image.get_rect()
            self.rhand_blaster.rect = self.rhand_blaster.image.get_rect()
            if self.last:
                self.lhand_blaster.rect.x = self.lhand.rect.x + 80 + 5
                self.rhand_blaster.rect.x = self.rhand.rect.x + 80 + 5
            else:
                self.lhand_blaster.rect.x = self.lhand.rect.x - 1000 - 5
                self.rhand_blaster.rect.x = self.rhand.rect.x - 1000 - 5
            self.lhand_blaster.rect.centery = self.lhand.rect.y + 75
            self.rhand_blaster.rect.centery = self.rhand.rect.y + 75
            self.b1_laser.image = pygame.Surface((25, 1000))
            self.b2_laser.image = pygame.Surface((25, 1000))
            self.b3_laser.image = pygame.Surface((25, 1000))
            self.b1_laser.image.fill((0, 220, 255))
            self.b2_laser.image.fill((0, 220, 255))
            self.b3_laser.image.fill((0, 220, 255))
            self.b1_laser.rect = self.b1_laser.image.get_rect()
            self.b2_laser.rect = self.b2_laser.image.get_rect()
            self.b3_laser.rect = self.b3_laser.image.get_rect()
            self.b1_laser.rect.centerx = self.blaster1.rect.centerx
            self.b1_laser.rect.y = self.blaster1.rect.y + 40 + 5
            self.b2_laser.rect.centerx = self.blaster2.rect.centerx
            self.b2_laser.rect.y = self.blaster2.rect.y + 40 + 5
            self.b3_laser.rect.centerx = self.blaster3.rect.centerx
            self.b3_laser.rect.y = self.blaster3.rect.y + 40 + 5

            self.ability1 += 1

            self.screen.blit(self.rhand_blaster.image, self.rhand_blaster.rect)
            self.screen.blit(self.lhand_blaster.image, self.lhand_blaster.rect)
            self.screen.blit(self.b1_laser.image, self.b1_laser.rect)
            self.screen.blit(self.b2_laser.image, self.b2_laser.rect)
            self.screen.blit(self.b3_laser.image, self.b3_laser.rect)

            if self.last:
                self.bone1.rect.x -= 1
                self.bone2.rect.x -= 1
                self.bone3.rect.x -= 1
            else:
                self.bone1.rect.x += 1
                self.bone2.rect.x += 1
                self.bone3.rect.x += 1
            self.screen.blit(self.rhand.image, self.rhand.rect)
            self.screen.blit(self.lhand.image, self.lhand.rect)
            self.screen.blit(self.blaster1.image, self.blaster1.rect)
            self.screen.blit(self.blaster2.image, self.blaster2.rect)
            self.screen.blit(self.blaster3.image, self.blaster3.rect)
            self.screen.blit(self.bone3.image, self.bone3.rect)
            self.screen.blit(self.bone2.image, self.bone2.rect)
            self.screen.blit(self.bone1.image, self.bone1.rect)
            self.screen.blit(self.friend1.image, self.friend1.rect)
            self.screen.blit(self.friend2.image, self.friend2.rect)
            self.screen.blit(self.friend3.image, self.friend3.rect)
            hits = pygame.sprite.spritecollide(self.bone1, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.bone2, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.bone3, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.b1_laser, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.b2_laser, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.b3_laser, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.rhand_blaster, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1
            hits = pygame.sprite.spritecollide(self.lhand_blaster, self.enemygroup, False)
            for hit in hits:
                if not hit.blocking or hit.blockdur <= 0:
                    hit.hp -= 0.25
                else:
                    hit.blockdur -= 1

            if self.ability1 == 90:
                self.ability1 = 0
                self.ability1_phase = 5
        if self.ability1_phase == 5:
            self.enemy.canmove = True
            self.enemy.flag_ability = False
            self.flag_ability = False
            self.flag_ability1 = False
            self.ability1_cd = 1
            self.canmove = True
            self.ability1_phase = 1

    def knifes(self):
        self.canmove = False
        self.flag_ability2 = True
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.ability2_phase == 1:
            self.knife1 = pygame.sprite.Sprite()
            self.knife2 = pygame.sprite.Sprite()
            self.knife3 = pygame.sprite.Sprite()
            self.knife1.image = pygame.image.load(path.join(img_dir, 'knife1.png')).convert()
            self.knife2.image = pygame.image.load(path.join(img_dir, 'knife2.png')).convert()
            self.knife3.image = pygame.image.load(path.join(img_dir, 'knife3.png')).convert()
            self.knife1.image.set_colorkey((0, 0, 0))
            self.knife2.image.set_colorkey((0, 0, 0))
            self.knife3.image.set_colorkey((0, 0, 0))

            # 120x30, 30x120
            self.knife1.rect = self.knife1.image.get_rect()
            self.knife2.rect = self.knife2.image.get_rect()
            self.knife3.rect = self.knife3.image.get_rect()
            self.knife1.rect.x = self.enemy.rect.x - 120 - 20
            self.knife1.rect.centery = self.enemy.rect.centery
            self.knife2.rect.x = self.enemy.rect.x + 120 + 20
            self.knife2.rect.centery = self.enemy.rect.centery
            self.knife3.rect.centerx = self.enemy.rect.centerx
            self.knife3.rect.y = self.enemy.rect.y - 120 - 60
            self.ability2 += 1

            if self.ability2 == 20:
                self.ability2_phase = 2
                self.ability2 = 0
            self.screen.blit(self.knife1.image, self.knife1.rect)
            self.screen.blit(self.knife2.image, self.knife2.rect)
            self.screen.blit(self.knife3.image, self.knife3.rect)
            self.a2flag1 = True
            self.a2flag2 = True
            self.a2flag3 = True
        if self.ability2_phase == 2:
            self.knife1.rect.x += 1
            self.knife2.rect.x -= 1
            self.knife3.rect.y += 7
            if self.a2flag1:
                self.screen.blit(self.knife1.image, self.knife1.rect)
                hits = pygame.sprite.spritecollide(self.knife1, self.enemygroup, False)
                for hit in hits:
                    if not hit.blocking or hit.blockdur <= 0:
                        hit.hp -= 1
                    else:
                        hit.blockdur -= 1
            if self.a2flag2:
                self.screen.blit(self.knife2.image, self.knife2.rect)
                hits = pygame.sprite.spritecollide(self.knife2, self.enemygroup, False)
                for hit in hits:
                    if not hit.blocking or hit.blockdur <= 0:
                        hit.hp -= 1
                    else:
                        hit.blockdur -= 1
            if self.a2flag3:
                self.screen.blit(self.knife3.image, self.knife3.rect)
                hits = pygame.sprite.spritecollide(self.knife3, self.enemygroup, False)
                for hit in hits:
                    hit.hp -= 15
            self.ability2 += 1
            if self.ability2 == 120:
                self.canmove = True
                self.flag_ability2 = False
                self.ability2_phase = 1
                self.ability2 = 0
                self.ability2_cd = 1

    def ult(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.flag_ability3 = True
        self.enemy.canmove = False
        self.enemy.flag_ability = True
        self.ability3 += 1
        self.screen.blit(self.it.image, self.it.rect)
        hits = pygame.sprite.spritecollide(self.it, self.enemygroup, False)
        for hit in hits:
            hit.hp -= 1.3
        if self.ability3 == 240:
            self.flag_ability3 = False
            self.enemy.canmove = True
            self.enemy.flag_ability = False
            self.ability3 = 0
            self.ability3_cd = 1
class Lesha(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Lesha'
        self.bullet_sprite = []
        self.trajectory = []
        self.bullets = []
        self.bullet_animcount = 0
        self.bullet_count = 0
        self.flag_vec = []
        self.flag_ability1 = False
        self.screen = screen
        self.ability1 = 0
        self.ability1_cd = 0
        self.ability2 = 0
        self.ability2_cd = 0
        self.ability3_phase = 0
        self.ability3 = 0
        self.ability3_cd = 0
        self.flag_ability3 = False

        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.bullet = pygame.sprite.Sprite()
        self.bullet.image = self.image = pygame.image.load(path.join(img_dir, 'testing-bullet.png')).convert()
        self.bullet.rect = self.bullet.image.get_rect()
        self.bullet.speed = 15

        self.flag_ability2 = False
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, self.screen, colour)
        self.ability1_name = 'laser'
        self.ability1_maxcd = 90
        self.ability2_name = 'slowness aura'
        self.ability2_maxcd = 300
        self.ability3_name = 'FLY POWPOW ULT'
        self.ability3_maxcd = 420
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.laser_flag = False
        self.laser_sound = pygame.mixer.Sound(file=path.join(img_dir, 'laserShoot.wav'))
        self.slowness_flag = False
        self.slowness_sound = pygame.mixer.Sound(file=path.join(img_dir, 'slowness.wav'))
        self.ult_flag = False
        self.ult_sound = pygame.mixer.Sound(file=path.join(img_dir, 'leshaShoot.wav'))
        self.ability1_desc = 'лазер. хороший урон, маленький откат, игнорирует блок'
        self.ability2_desc = 'аура замедления. ЗАМЕДЛЯЕТ'
        self.ability3_desc = 'леша подлетает, выстреливает 3 снаряда, которые следуют за игроком'
        self.chr_desc = 'Леша. Спам машина, маленькие откаты, средний урон'
        self.why_cnt = 0

    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[2]] and not self.flag_ability or self.flag_ability3) and self.ability3_cd == 0:
            self.ult()
        if (keystate[self.abkeys[1]] and not self.flag_ability or self.flag_ability2) and self.ability2_cd == 0:
            self.slowness()
        if (keystate[self.abkeys[0]] and not self.flag_ability or self.flag_ability1) and self.ability1_cd == 0:
            self.laser()
        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 90:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 300:
                self.ability2_cd = 0
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= 420:
                self.ability3_cd = 0

    def laser(self):
        flag = True
        self.flag_ability = True
        self.flag_ability1 = True
        self.canmove = False
        self.las = pygame.sprite.Sprite()
        self.las.image = pygame.Surface((300, 20))
        self.las.image.fill((255, 0, 0))
        self.las.rect = self.las.image.get_rect()
        if self.last:
            self.las.rect.x, self.las.rect.y = self.rect.x + 85, self.rect.y + 50
        else:
            self.las.rect.x, self.las.rect.y = self.rect.x - 85 - 42.5 - 23 - 150, self.rect.y + 50
        hit = pygame.sprite.spritecollide(self.las, self.enemygroup, False)
        for h in hit:
            if flag:
                try:
                    h.hp -= 2.3
                except:
                    h.canblock = False
        if not self.laser_flag:
            self.laser_sound.play()
            self.laser_flag = True
        self.screen.blit(self.las.image, self.las.rect)
        self.ability1 += 1
        if self.ability1 >= 45:
            self.ability1_cd = 1
            self.flag_ability = False
            self.flag_ability1 = False
            self.ability1 = 0
            self.laser_flag = False

    def slowness(self):
        # print('xd')
        self.flag_ability2 = True
        self.circle = pygame.sprite.Sprite()
        self.circle.image = pygame.Surface((500, 500))
        self.circle.image.fill((0, 100, 255))
        self.circle.rect = self.circle.image.get_rect()
        if not self.slowness_flag:
            self.slowness_sound.play()
            self.called_phrases.append(['And what will you do now?', self.rect.centerx, self.rect.y])
            self.slowness_flag = True
        if self.ability2 <= 300:
            self.circle.rect.x = self.rect.x - 210
            self.circle.rect.y = self.rect.y - 210
            self.ability2 += 1
            hits = pygame.sprite.spritecollide(self.circle, self.enemygroup, False)
            for hit in hits:
                try:
                    hit.permspeed = 0.3
                except:
                    pass
                    # print('xd')
            if len(hits) == 0:
                self.enemy.permspeed = 1
            self.screen.blit(self.circle.image, self.circle.rect)
        else:
            self.slowness_flag = False
            self.enemy.permspeed = 1
            self.ability2 = 0
            self.ability2_cd = 1
            self.flag_ability2 = False

    def move_towards_player(self, bullet, i):
        if len(self.flag_vec) == 0 or self.flag_vec[i] == False:
            # Find direction vector (dx, dy) between enemy and player.
            self.dx, self.dy = self.enemy.rect.x - bullet.rect.x, self.enemy.rect.y - bullet.rect.y
            self.dist = math.hypot(self.dx, self.dy)
            self.dx, self.dy = self.dx / self.dist, self.dy / self.dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            bullet.rect.x += self.dx * bullet.speed
            bullet.rect.y += self.dy * bullet.speed
            self.trajectory.append([self.dx * bullet.speed, self.dy * bullet.speed])
        elif self.flag_vec[i] == True:
            bullet.rect.x += self.trajectory[i][0]
            bullet.rect.y += self.trajectory[i][1]

    def ult(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.flag_ability3 = True
        self.canmove = False
        self.flag_ability = True
        if self.ability3_phase == 0:
            if self.why_cnt == 0:
                self.called_phrases.append(['Are you ready? I AM', self.rect.centerx, self.rect.y])
            self.why_cnt += 1
            self.bullets = []
            self.bullet_sprite = []
            self.trajectory = []
            self.rect.y -= 3
            if self.rect.y <= 225:
                self.ability3_phase = 1
        elif self.ability3_phase == 1:
            self.bullet_animcount += 1
            if self.bullet_animcount % 31 == 0:
                self.ult_sound.play()
                # print('BULLET!')
                self.flag_vec.append(False)
                self.bullets.append([pygame.image.load(path.join(img_dir, 'fire.png')).convert(),
                                     (self.rect.x + 42.5, self.rect.y + 50)])
            try:
                for i in range(len(self.bullets)):
                    b = self.bullet_sprite[i]
                    self.move_towards_player(b, i)
                    hits = pygame.sprite.spritecollide(b, self.enemygroup, False)
                    for hit in hits:
                        if not hit.blocking or hit.blockdur <= 0:
                            hit.hp -= 0.75
                        else:
                            hit.blockdur -= 1
                    self.screen.blit(b.image, b.rect)
            except:
                for i in range(len(self.bullets)):
                    # print(self.bullets)
                    b = pygame.sprite.Sprite()
                    b.image = self.bullets[i][0]
                    b.image.set_colorkey((255, 255, 255))
                    b.rect = b.image.get_rect()
                    b.rect.x = self.bullets[i][1][0]
                    b.rect.y = self.bullets[i][1][1]
                    b.speed = 20
                    self.bullet_sprite.append(b)
                    self.screen.blit(b.image, b.rect)
            if self.bullet_animcount >= 151:
                self.ability3_phase = 2
        elif self.ability3_phase == 2:
            if self.rect.center[1] < HEIGHT - 100:
                self.rect.y += 5
            elif self.rect.center[1] > HEIGHT - 100:
                self.rect.y = HEIGHT - 100 - 50
            elif self.rect.center[1] == HEIGHT - 100:
                self.why_cnt = 0
                self.ability3_phase = 0
                self.flag_ability3 = False
                self.canmove = True
                self.flag_ability = False
                self.bullets = []
                self.ability3_cd += 1
                self.bullet_animcount = 0


class Dummy(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.hp = 500
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(path.join(img_dir, 'blue2_0.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 250, HEIGHT - 100

    def update(self):
        self.screen.blit(self.image, self.rect)
        print(self.hp)
class TestingBullet(pygame.sprite.Sprite):
    def __init__(self, screen, enemygroup, speed, x):
        self.screen = screen
        self.speed = speed
        self.enemygroup = enemygroup
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(path.join(img_dir, 'testing-bullet.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, HEIGHT - 100
        self.flag = True

    def update(self):
        if self.flag:
            self.rect.x -= self.speed
            hit = pygame.sprite.spritecollide(self, self.enemygroup, False)
            for el in hit:
                try:
                    el.hp -= 99
                    self.flag = False
                except:
                    el.canblock = False
                    self.flag = False
            self.screen.blit(self.image, self.rect)
