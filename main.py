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

all_sprites = pygame.sprite.Group()
chr_1 = pygame.Surface((150, 150))
chr_rect = chr_1.get_rect()
chr_rect.centerx = 110
chr_rect.centery = 150
player = chr.Nikita_Dev()
all_sprites.add(player)

img_dir = path.join(path.dirname(__file__), 'Assets')
flag_menu = True
main_menu = pygame.image.load(path.join(img_dir, 'main_menu.png')).convert()
main_menu_rect = main_menu.get_rect()
bg = pygame.image.load(path.join(img_dir, 'image.png')).convert()
bg_rect = bg.get_rect()
font = pygame.font.Font(None, 40)
font_color = (0,0,0)
t_chr1 = font.render('Character 1: NikitaDev', True, font_color)
t_chr1_rect = t_chr1.get_rect()
t_chr1_rect.centerx = 170
t_chr1_rect.centery = 30

font2 = pygame.font.Font(None, 100)
font2_color = (0,155,255)
font2_background = (0,0,0)
t = font2.render("game xd. press f to start", True, font2_color, font2_background)
t_rect = t.get_rect()
t_rect.centerx, t_rect.centery = 500, 50
# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                flag_menu = False
    all_sprites.update()
    player.update2()
    screen.fill(BLACK)
    if not flag_menu:
        screen.blit(bg, bg_rect)
        screen.blit(t_chr1, t_chr1_rect)
        all_sprites.draw(screen)
        screen.blit(chr_1, chr_rect)
    else:
        screen.blit(main_menu, main_menu_rect)
        screen.blit(t, t_rect)
    pygame.display.flip()

pygame.quit()
