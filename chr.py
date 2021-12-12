import pygame
from os import path
import math
import random

WIDTH = 1000
HEIGHT = 650

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.dur = 0
        self.blockdur = 45
        self.attack_damage = 1.5
        self.permspeed = 1
        self.colour = colour
        self.screen = screen
        self.hp = 500
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
        '''
        self.block_r = pygame.sprite.Sprite()
        self.block_r.image = pygame.Surface((50, 100))
        self.block_r.rect = self.attack_r.image.get_rect()
        self.block_r.image.fill((255, 255, 255))
        self.block_r.canblock = True
        '''
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

    def attack(self):
        # , special_flags=pygame.BLEND_RGBA_MULT
        if not self.last:
            self.attack_r.rect.x, self.attack_r.rect.y = self.rect.x-12.5, self.rect.y
        else:
            self.attack_r.rect.x, self.attack_r.rect.y = self.rect.x+55, self.rect.y
        self.screen.blit(self.attack_r.image, self.attack_r.rect, special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        if self.hp <= 0:
            with open('whowon.txt', 'w') as f:
                f.write(f'{self.enemy.colour} WON!!!!!!!')
            exit(0)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.blockdur <= 0:
            self.canblock = False
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[self.abkeys[3]] and self.canblock:
            self.blocking = True
            self.canmove = False
        elif keystate[self.abkeys[4]] or self.attacking == True:
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
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            self.animcount += 1
            if self.left:
                self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_{self.animcount // 9}.png')).convert()
            elif self.right:
                self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_{self.animcount // 9}.png')).convert()
            else:
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_0.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_0.png')).convert()
        else:
            if self.blocking:
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_block.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_block.png')).convert()
                # self.block()
            elif self.attacking:
                self.attackacount += 1
                if self.attackacount >= 30:
                    if self.last:
                        self.rect.x += 10
                    else:
                        self.rect.x -= 10
                if self.last:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
                else:
                    self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
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
            elif self.flag_ability:
                pass
            else:
                self.animcount = 0
                self.blocking = False
                self.canmove = True
        # print(self.hp)
        self.image.set_colorkey((255, 255, 255))
        self.rect.x += self.speedx * self.permspeed
        # print(self.flag_ability)
        self.screen.blit(self.image, self.rect)


class Nikita(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Nikita'
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.ability1_cd = 0
        self.flag_ability1 = False
        self.ability1 = 0
        self.ability1_phase = 0
        self.ability2 = 0
        self.flag_ability2 = False
        self.ability2_cd = 0
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

        self.awakening = 0
        self.awakening_phase = 3
        self.awakening_cnt = 0
        self.awakening_cd = 0

    def update2(self):
        keystate = pygame.key.get_pressed()
        if self.awakening == False:
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
                if self.awakening_cd >= 480:
                    self.awakening_cd = 0

            if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
                self.rat()
            if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
                self.trick()
            if keystate[self.abkeys[2]] and self.awakening_cd == 0:
                self.awakening = True
                self.ability1_cd = 0
                self.ability2_cd = 0
                self.awakening_cd = 1
        elif self.awakening_phase == 1:
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
            if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
                self.speed()
            if keystate[self.abkeys[1]] and self.ability2_cd == 0 and self.flag_ability2 == 0:
                self.attackacount = 15
            if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
                self.punch()

            if self.awakening_cnt >= 720:
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
        elif self.awakening_phase == 2:
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

            self.awakening_cd += 1
            if keystate[self.abkeys[0]] and self.ability1_cd == 0 and self.flag_ability1 == 0:
                self.movement = []
                self.permhp = self.hp
            if keystate[self.abkeys[1]] and self.ability2_cd == 0 and self.flag_ability2 == 0:
                self.permhp = self.hp
            if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
                self.epitaph()
            if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
                self.dash()
            if keystate[self.abkeys[2]] and self.awakening_cd >= 600:
                self.dash_hp = self.hp
                self.awakening_phase = 3
                self.awakening_cd = 1
                self.awakening_cnt = 0
        elif self.awakening_phase == 3:
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
            if self.awakening_cnt >= 900:
                self.enemy.flag_ability = False
                self.awakening_cnt = 0
                self.flag_ability1 = False
                self.flag_ability2 = False
                self.flag_ability3 = False
                self.awakening_phase = 2
                self.attack_damage = 1.5
            if keystate[self.abkeys[0]] and not self.flag_ability1 and self.ability1_cd == 0:
                self.permhp = self.hp
                self.x = self.enemy.rect.x
            if keystate[self.abkeys[1]] and not self.flag_ability2 and self.ability2_cd == 0:
                self.permhp = self.hp
            if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
                self.time_erase()
            if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
                self.invinc()
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
        elif self.awakening_phase == 3:
            if self.ability1_cd != 0:
                self.ability1_cd += 1
                if self.ability1_cd >= 300:
                    self.ability1_cd = 0
            if self.ability2_cd != 0:
                self.ability2_cd += 1
                if self.ability2_cd >= 180:
                    self.ability2_cd = 0
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
            self.ability1_phase = 1
        elif self.ability1_phase == 1:
            self.canmove = False
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            img_dir = path.join(path.dirname(__file__), 'Assets')
            self.attackacount += 1
            if self.attackacount >= 30:
                if self.last:
                    self.rect.x += 10
                else:
                    self.rect.x -= 10
            if self.last:
                self.image = pygame.image.load(path.join(img_dir, f'{self.colour}1_a_{self.attackacount // 15}.png')).convert()
            else:
                self.image = pygame.image.load(path.join(img_dir, f'{self.colour}2_a_{self.attackacount // 15}.png')).convert()
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
                self.attackacount += 1
                if self.attackacount >= 30:
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
    def speed(self):
        self.flag_ability1 = True
        self.permspeed = 1.5
        self.ability1 += 1
        if self.ability1 >= 420:
            self.permspeed = 1
            self.flag_ability1 = False
            self.ability1 = 0
    def punch(self):
        self.flag_ability = True
        self.flag_ability2 = True
        self.canmove = False
        if not self.punch_flag:
            img_dir = path.join(path.dirname(__file__), 'Assets')
            self.attackacount += 1
            if self.attackacount >= 30:
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
            self.movement.append(self.enemy.rect.x)
            self.epitaph_cnt += 1
            self.hp = self.permhp
            if self.epitaph_cnt >= 180:
                self.epitaph_phase = 2
                self.epitaph_cnt = 0
        elif self.epitaph_phase == 2:
            self.enemy.canmove = False
            self.enemy.flag_ability = True
            self.enemy.rect.x = self.movement[self.epitaph_cnt]
            self.epitaph_cnt += 1
            if self.epitaph_cnt >= 120:
                self.epitaph_phase = 3
        else:
            self.epitaph_cnt = 0
            self.epitaph_phase = 1
            self.enemy.canmove = True
            self.flag_ability = False
            self.movement = []
            self.flag_ability1 = False
    def dash(self):
        self.canmove = False
        self.flag_ability = True
        self.flag_ability2 = True
        self.hp = self.permhp
        img_dir = path.join(path.dirname(__file__), 'Assets')
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
                self.te = 0
                self.te_phase = 0
                self.flag_ability1 = False
                self.enemy.flag_ability = False
                self.enemy.blockdur = 45
    def invinc(self):
        self.flag_ability2 = True
        self.invinc_cnt += 1
        self.hp = self.permhp
        if self.invinc_cnt == 240:
            self.invinc_cnt = 0
            self.flag_ability2 = False
            self.ability2_cd = 1
class Georg(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Georg'
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.ability1_cd = 0
        self.flag_ability1 = False
        self.ability1 = 0
        self.ability2 = 0
        self.flag_ability2 = False
        self.ability2_cd = 0
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
        self.ability3_cd = 0
        self.ability3 = 0
    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
            self.fire()
        if(keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
            self.chaos()
        if(keystate[self.abkeys[2]] or self.flag_ability3) and self.ability3_cd == 0:
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
        self.ability1 += 1
        img_dir = path.join(path.dirname(__file__), 'Assets')
        if self.last:
            img_dir = path.join(img_dir, 'fire-right')
        else:
            img_dir = path.join(img_dir, 'fire-left')
        xd = str(self.ability1%60)
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
            self.fires.rect.x += 0.5
        else:
            self.fires.rect.x -= 0.5
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
        self.flag_ability = True
        self.flag_ability2 = True
        if self.ability2_phase == 0:
            self.big_bullet.rect.centerx = self.rect.centerx
            self.big_bullet.rect.y = self.rect.y - 205
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
            if self.ability2 >= 990:
                self.ability2_phase = 3
            elif self.ability2 % 66 == 0:
                self.main_bullet.rect.x = random.randint(1, 1000)
                self.main_bullet.rect.y = 10
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
                self.enemy.hp -= min(350 - 4 * self.ability3, 250)
                self.enemy.canmove = True
                self.enemy.flag_ability = False
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
                self.enemy.hp -= min(350 - 4 * self.ability3, 250)
                self.enemy.canmove = True
                self.enemy.flag_ability = False
        if self.ability3 > 61:
            self.ability3 = 0
            self.flag_ability3 = False
            self.flag_ability = False
            self.ability3_cd = 1
            self.enemy.canmove = True
            self.enemy.flag_ability = False
class Bogdan(Player, pygame.sprite.Sprite):
    def __init__(self, screen, colour):
        self.chr = 'Bogdan'
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.attack_damage = 2
        self.ability1_cd = 0
        self.ability2_cd = 0
        self.ability2 = 0
        self.ab2_flag = False
        self.flag_ability2 = False

    def update2(self):
        keystate = pygame.key.get_pressed()
        if keystate[self.abkeys[0]] and self.ability1_cd == 0:
            self.tp()
        if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
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
        self.rect.x = random.randint(1, 1000)
        self.ability1_cd = 1
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
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, screen, colour)
        self.permhp = 0
        self.ability1 = 0
        self.ability1_cd = 0
        self.flag_ability1 = False
        self.flag_ability2 = False
        self.ability2_cd = 0
        self.ability3_cd = 0
        self.flag_ability3 = False
        self.ability3 = 0
        self.ab3_permhp = 0
        self.ab3_difference = 0
    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
            self.shield()
        if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
            self.atk_2()
        if (keystate[self.abkeys[2]] or self.flag_ability3) and self.ability3_cd == 0:
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
        self.attackacount += 1
        if self.attackacount >= 30:
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
    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
            self.ow5()
        if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
            self.knifes()
        if (keystate[self.abkeys[2]] or self.flag_ability3) and self.ability3_cd == 0:
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
        self.it = pygame.sprite.Sprite()
        self.it.image = pygame.image.load(path.join(img_dir, 'it.png')).convert()
        self.it.rect = self.it.image.get_rect()
        self.it.rect.x = 0
        self.it.rect.y = 0
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
        img_dir = path.join(path.dirname(__file__), 'Assets')
    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[self.abkeys[2]] or self.flag_ability3) and self.ability3_cd == 0:
            self.ult()
        if (keystate[self.abkeys[1]] or self.flag_ability2) and self.ability2_cd == 0:
            self.slowness()
        if (keystate[self.abkeys[0]] or self.flag_ability1) and self.ability1_cd == 0:
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
                    h.hp -= 3
                    # print(h.hp)
                except:
                    h.canblock = False
        self.screen.blit(self.las.image, self.las.rect)
        self.ability1 += 1
        if self.ability1 >= 25:
            self.ability1_cd = 1
            self.flag_ability = False
            self.flag_ability1 = False
            self.ability1 = 0
    def slowness(self):
        # print('xd')
        self.flag_ability2 = True
        self.canmove = True
        self.circle = pygame.sprite.Sprite()
        self.circle.image = pygame.Surface((500, 500))
        self.circle.image.fill((0, 100, 255))
        self.circle.rect = self.circle.image.get_rect()
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
            self.bullets = []
            self.bullet_sprite = []
            self.trajectory = []
            self.rect.y -= 3
            if self.rect.y <= 225:
                self.ability3_phase = 1
        elif self.ability3_phase == 1:
            self.bullet_animcount += 1
            if self.bullet_animcount % 30 == 0:
                # print('BULLET!')
                self.flag_vec.append(False)
                self.bullets.append([pygame.image.load(path.join(img_dir, 'fire.png')).convert(), (self.rect.x + 42.5, self.rect.y + 50)])
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
