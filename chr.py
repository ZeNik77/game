import pygame
from os import path
import math

WIDTH = 1000
HEIGHT = 650


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.hp = 500
        self.enemy = 0
        self.enemygroup = 0
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.last = True
        self.canmove = True

        self.attack_r = pygame.sprite.Sprite()
        self.attack_r.image = pygame.Surface((50, 100))
        self.attack_r.rect = self.attack_r.image.get_rect()
        self.attack_r.image.fill((255, 255, 255))

        self.block_cd = 0
        self.block_r = pygame.sprite.Sprite()
        self.block_r.image = pygame.Surface((50, 100))
        self.block_r.rect = self.attack_r.image.get_rect()
        self.block_r.image.fill((255, 255, 255))
        self.block_r.canblock = True

        self.blocking = False
        self.attacking = False
        self.flag_ability = False
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
        if not self.last:
            self.block_r.rect.x, self.block_r.rect.y = self.rect.x-12.5, self.rect.y
        else:
            self.block_r.rect.x, self.block_r.rect.y = self.rect.x+55, self.rect.y
        self.screen.blit(self.block_r.image, self.block_r.rect, special_flags=pygame.BLEND_RGBA_MULT)

    def update(self):
        # print(self.hp)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.speedx = 0
        # print(f'canblock {self.block_r.canblock}   blocking {self.blocking}    cooldown {self.block_cd}')
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_f] and self.block_r.canblock:
            self.blocking = True
            self.canmove = False
        elif keystate[pygame.K_c] or self.attacking == True:
            self.canmove = False
            self.attacking = True
        else:
            if not self.flag_ability:
                self.blocking = False
                self.canmove = True
        if self.block_r.canblock == False and self.flag_ability == False:
            self.block_r.rect.x, self.block_r.rect.y = 800, 500
            self.blocking = False
            self.canmove = False
            if self.last:
                self.image = pygame.image.load(path.join(img_dir, 'blue1_0.png')).convert()
                self.rect.x -= 0.05
            else:
                self.image = pygame.image.load(path.join(img_dir, 'blue2_0.png')).convert()
                self.rect.x += 0.05
            self.block_cd += 1
            if self.block_cd >= 90:
                self.block_cd = 0
                self.block_r.canblock = True
        if self.animcount + 1 >= 60:
            self.animcount = 1
        if self.canmove:
            self.attack_r.rect.x = 800
            self.attack_r.rect.y = 500
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
        # else:
        else:
            if self.blocking:
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
                flag = True
                hits = pygame.sprite.spritecollide(self.attack_r, self.enemygroup, False)
                for hit in hits:
                    try:
                        hit.hp -= 1
                        # print(hit.hp)
                        break
                    except:
                        hit.block_r.canblock = False
                        break
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
        self.rect.x += self.speedx
        # print(self.flag_ability)
        self.screen.blit(self.image, self.rect)


class Nikita_Dev(Player, pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, self.screen)
        img_dir = path.join(path.dirname(__file__), 'Assets')

class Lesha(Player, pygame.sprite.Sprite):
    def __init__(self, screen):
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
        Player.__init__(self, self.screen)
        img_dir = path.join(path.dirname(__file__), 'Assets')
    def update2(self):
        keystate = pygame.key.get_pressed()
        if (keystate[pygame.K_e] or self.flag_ability3) and self.ability3_cd == 0:
            self.ult()
        if (keystate[pygame.K_w] or self.flag_ability2) and self.ability2_cd == 0:
            self.slowness()
        if (keystate[pygame.K_q] or self.flag_ability1) and self.ability1_cd == 0:
            self.laser()
        if self.ability1_cd != 0:
            self.ability1_cd += 1
            if self.ability1_cd >= 300:
                self.ability1_cd = 0
        if self.ability2_cd != 0:
            self.ability2_cd += 1
            if self.ability2_cd >= 1000:
                self.ability2_cd = 0
        if self.ability3_cd != 0:
            self.ability3_cd += 1
            if self.ability3_cd >= 300:
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
                    h.hp -= 1.5
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
                    hit.speedx = hit.speedx // 2
                    if abs(hit.speedx) <= 4:
                        hit.speedx *= 2
                except:
                    pass
                    # print('xd')
            self.screen.blit(self.circle.image, self.circle.rect)
        else:
            self.ability2 = 0
            self.ability2_cd = 1
            self.flag_ability2 = False
            self.flag_ability = False

    def move_towards_player(self, bullet, i):
        if len(self.flag_vec) == 0 or self.flag_vec[i] == False:
            # Find direction vector (dx, dy) between enemy and player.
            self.dx, self.dy = self.enemy.rect.x - bullet.rect.x, self.enemy.rect.y - bullet.rect.y
            self.dist = math.hypot(self.dx, self.dy)
            self.dx, self.dy = self.dx / self.dist, self.dy / self.dist  # Normalize.
            # Move along this normalized vector towards the player at current speed.
            self.trajectory.append((self.dx * bullet.speed, self.dy * bullet.speed))
            self.flag_vec.append(True)
            return [bullet.rect.x + self.trajectory[i][0], bullet.rect.y + self.trajectory[i][1]]
        elif self.flag_vec[i] == True:
            return [bullet.rect.x + self.trajectory[i][0], bullet.rect.y + self.trajectory[i][1]]

    def ult(self):
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.flag_ability3 = True
        self.canmove = False
        self.flag_ability = True
        if self.ability3_phase == 0:
            self.rect.y -= 3
            if self.rect.y <= 225:
                self.ability3_phase = 1
        elif self.ability3_phase == 1:
            self.bullet_animcount += 1
            if self.bullet_animcount % 30 == 0:
                # print('BULLET!')
                self.flag_vec.append(False)
                self.bullets.append([pygame.image.load(path.join(img_dir, 'testing-bullet.png')).convert(), (self.rect.x + 42.5, self.rect.y + 42.5)])
            try:
                for i in range(len(self.bullets)):
                    b = self.bullet_sprite[i]
                    xd = self.move_towards_player(b, i)
                    b.rect.x = xd[0]
                    b.rect.y = xd[1]
            except:
                for i in range(len(self.bullets)):
                    b = pygame.sprite.Sprite()
                    b.image = self.bullets[i][0]
                    b.rect = b.image.get_rect()
                    b.rect.x = self.bullets[i][1][0]
                    b.rect.y = self.bullets[i][1][1]
                    b.speed = 20
                    xd = self.move_towards_player(b, i)
                    print(b.rect)
                    b.rect.x = xd[0]
                    b.rect.y = xd[1]
                    self.bullets[i] = b
                    print(b.rect)
                    print()
                    self.screen.blit(b.image, b.rect)
                    hits = pygame.sprite.spritecollide(b, self.enemygroup, False)
                    for hit in hits:
                        try:
                            hit.hp -= 10
                        except:
                            hit.canblock = False
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
        # print(self.hp)
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
