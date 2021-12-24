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

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("xd")
clock = pygame.time.Clock()
img_dir = path.join(path.dirname(__file__), 'Assets')

all_sprites = pygame.sprite.Group()
player = chr.Lesha(screen, 'blue')
player2 = chr.Lesha(screen, 'red')
# dummy = chr.Dummy(screen)

flag = True
select_phase = False
main_menu = pygame.image.load(path.join(img_dir, 'main_menu.png')).convert()
main_menu_rect = main_menu.get_rect()
bg = pygame.image.load(path.join(img_dir, 'image.png')).convert()
bg_rect = bg.get_rect()
font = pygame.font.Font(None, 40)
font_color = (0,0,0)

if player.chr == 'Nikita_Dev':
    a = 'NikitaDev'
    p = 'a.png'
elif player.chr == 'Lesha':
    a = 'Lesha'
    p = 'lesha.png'

if player2.chr == 'Nikita_Dev':
    a2 = 'NikitaDev'
    p2 = 'gaster.png'
elif player2.chr == 'Lesha':
    a2 = 'Lesha'
    p2 = 'lesha.png'

chr_1 = pygame.image.load(path.join(img_dir, p)).convert()
chr1_rect = chr_1.get_rect()
chr1_rect.centerx = 120
chr1_rect.centery = 150

chr_2 = pygame.image.load(path.join(img_dir, p2)).convert()
chr2_rect = chr_2.get_rect()
chr2_rect.centerx = WIDTH - 120
chr2_rect.centery = 150

t_chr1 = font.render('Player 1: '+ a, True, font_color)
t_chr1_rect = t_chr1.get_rect()
t_chr1_rect.x = 20
t_chr1_rect.centery = 30

t_chr2 = font.render('Player 2: '+ a2, True, font_color)
t_chr2_rect = t_chr1.get_rect()
t_chr2_rect.centerx = WIDTH - 170
t_chr2_rect.centery = 30

font2 = pygame.font.Font(None, 50)
font2_color = (0,255,220)
font2_background = (0,0,0)
t = font2.render("game xd. press z to start, o for character selection", True, font2_color, font2_background)
t_rect = t.get_rect()
t_rect.centerx, t_rect.centery = 500, 50

font3 = pygame.font.Font(None, 35)
font3_color = (0,255,255)
if not select_phase:
    c = 'first'
else:
    c = 'second'
t_choice = font3.render("space for changing player, 1 - NikitaDev, 2 - Lesha, current: " + c + ' z to start', True, font2_color)
t_choice_rect = t.get_rect()
t_choice_rect.centerx, t_rect.centery = 450, 30
player1_group = pygame.sprite.Group()
player1_group.add(player)
player2_group = pygame.sprite.Group()
player2_group.add(player2)
player.enemy = player2
player2.enemy = player
player.enemygroup = player2_group
player2.enemygroup = player1_group

# bullet1 = chr.TestingBullet(enemygroup=player1_group, screen=screen, speed=10, x=540)

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z and flag:
                flag = 0
            if event.key == pygame.K_o and flag:
                flag = 2
            if event.key == pygame.K_3 and flag == 2:
                if not select_phase:
                    a = 'Grisha'
                    p = 'Grisha.png'
                    player = chr.Grisha(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'Grisha'
                    p2 = 'Grisha.png'
                    player2 = chr.Grisha(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
            if event.key == pygame.K_4 and flag == 2:
                if not select_phase:
                    a = 'Bogdan'
                    p = 'Bogdan.png'
                    player = chr.Bogdan(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'Bogdan'
                    p2 = 'Bogdan.png'
                    player2 = chr.Bogdan(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
            if event.key == pygame.K_1 and flag == 2:
                if not select_phase:
                    a = 'NikitaDev'
                    p = 'gaster.png'
                    player = chr.Nikita_Dev(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'NikitaDev'
                    p2 = 'gaster.png'
                    player2 = chr.Nikita_Dev(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group

            if event.key == pygame.K_5 and flag == 2:
                if not select_phase:
                    a = 'Georg'
                    p = 'Georg.png'
                    player = chr.Georg(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)

                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)

                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'Georg'
                    p2 = 'Georg.png'
                    player2 = chr.Georg(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)

                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)

                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group



            if event.key == pygame.K_6 and flag == 2:
                if not select_phase:
                    a = 'Nikita'
                    p = 'Nikita.png'
                    player = chr.Nikita(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'Nikita'
                    p2 = 'Nikita.png'
                    player2 = chr.Nikita(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group

            if event.key == pygame.K_7 and flag == 2:
                if not select_phase:
                    a = 'Senia'
                    p = 'Senia.png'
                    player = chr.Senia(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)

                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)

                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'Senia'
                    p2 = 'Senia.png'
                    player2 = chr.Senia(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)

                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)

                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group

            if event.key == pygame.K_2 and flag == 2:
                if not select_phase:
                    a = 'Lesha'
                    p = 'lesha.png'
                    player = chr.Lesha(screen, 'blue')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
                else:
                    a2 = 'Lesha'
                    p2 = 'lesha.png'
                    player2 = chr.Lesha(screen, 'red')
                    player.enemy = player2
                    player2.enemy = player
                    player1_group = pygame.sprite.Group()
                    player1_group.add(player)
                    
                    player2_group = pygame.sprite.Group()
                    player2_group.add(player2)
                    
                    player.enemygroup = player2_group
                    player2.enemygroup = player1_group
            if event.key == pygame.K_SPACE and flag == 2:
                select_phase = not select_phase
    if flag == 2:
        chr_1 = pygame.image.load(path.join(img_dir, p)).convert()
        chr1_rect = chr_1.get_rect()
        chr1_rect.centerx = 120
        chr1_rect.centery = 150

        chr_2 = pygame.image.load(path.join(img_dir, p2)).convert()
        chr2_rect = chr_2.get_rect()
        chr2_rect.centerx = WIDTH - 120
        chr2_rect.centery = 150

        t_chr1 = font.render('Player 1: ' + a, True, font_color)
        t_chr1_rect = t_chr1.get_rect()
        t_chr1_rect.x = 20
        t_chr1_rect.centery = 30

        t_chr2 = font.render('Player 2: ' + a2, True, font_color)
        t_chr2_rect = t_chr1.get_rect()
        t_chr2_rect.right = WIDTH - 20
        t_chr2_rect.centery = 30
    # all_sprites.update()
    screen.fill(BLACK)
    if not flag:
        # 195, 225
        screen.blit(bg, bg_rect)
        screen.blit(t_chr1, t_chr1_rect)
        screen.blit(t_chr2, t_chr2_rect)

        pygame.draw.rect(screen, RED, (200, 75, 30, (500 - player.hp) // 3.3))
        pygame.draw.rect(screen, GREEN, (200, (75 + (500 - player.hp) // 3.3), 30, player.hp // 3.3))
        pygame.draw.rect(screen, RED, (770, 75, 30, (500 - player2.hp) // 3.3))
        pygame.draw.rect(screen, GREEN, (770, (75 + (500 - player2.hp) // 3.3), 30, player2.hp // 3.3))
        player.update2()
        player2.update2()
        player.update()
        player2.update()
        # print(f'canblock {player.canblock}, blockdur {player.blockdur}, dur {player.dur}')
        # print(f'canblock2 {player2.canblock}, blockdur2 {player2.blockdur}, dur2 {player2.dur}')
        # bullet1.update()
        screen.blit(chr_1, chr1_rect)
        screen.blit(chr_2, chr2_rect)
    elif flag == 1:
        screen.blit(main_menu, main_menu_rect)
        screen.blit(t, t_rect)
    elif flag == 2:
        screen.fill((255, 0, 200))
        if not select_phase:
            c = 'first'
        else:
            c = 'second'
        t_choice = font3.render("space to change player, 1 - NikitaDev, 2 - Lesha, 3 - Grisha, 4 - Bogdan, 5 - Georg, 6 - Nikita, current: " + c + ' z to start', True, font2_color)
        t_choice_rect = t.get_rect()
        t_choice_rect.centerx, t_rect.centery = 450, 30
        screen.blit(t_choice, t_choice_rect)

    pygame.display.flip()

pygame.quit()