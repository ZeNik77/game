import pygame
from os import path
import chr
WIDTH = 1000
HEIGHT = 650
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)



# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("xd")
clock = pygame.time.Clock()
img_dir = path.join(path.dirname(__file__), 'Assets')

all_sprites = pygame.sprite.Group()
chr_1 = pygame.image.load(path.join(img_dir, 'gaster.png')).convert()
chr_rect = chr_1.get_rect()
chr_rect.centerx = 110
chr_rect.centery = 150
player = chr.Nikita_Dev(screen)
dummy = chr.Dummy(screen)
player.enemy = dummy

flag_menu = True
main_menu = pygame.image.load(path.join(img_dir, 'main_menu.png')).convert()
main_menu_rect = main_menu.get_rect()
bg = pygame.image.load(path.join(img_dir, 'image.png')).convert()
bg_rect = bg.get_rect()
font = pygame.font.Font(None, 40)
font_color = (0,0,0)
t_chr1 = font.render('Player 1: NikitaDev', True, font_color)
t_chr1_rect = t_chr1.get_rect()
t_chr1_rect.centerx = 170
t_chr1_rect.centery = 30

font2 = pygame.font.Font(None, 100)
font2_color = (0,255,220)
font2_background = (0,0,0)
t = font2.render("game xd. press z to start", True, font2_color, font2_background)
t_rect = t.get_rect()
t_rect.centerx, t_rect.centery = 500, 50

player1_group = pygame.sprite.Group()
player1_group.add(player)
player1_group.add(player.block_r)
# bullet1 = chr.TestingBullet(enemygroup=player1_group, screen=screen, speed=10, x=540)

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                flag_menu = False
    # all_sprites.update()
    screen.fill(BLACK)
    if not flag_menu:
        screen.blit(bg, bg_rect)
        screen.blit(t_chr1, t_chr1_rect)
        # all_sprites.draw(screen)
        player.update()
        dummy.update()
        # bullet1.update()
        screen.blit(chr_1, chr_rect)
    else:
        screen.blit(main_menu, main_menu_rect)
        screen.blit(t, t_rect)
    pygame.display.flip()

pygame.quit()
