import pygame
from os import path
from PIL import Image as image
import chr
from chr import time
#import io
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
#chr.Lesha(screen, 'blue')
#player2 = chr.Lesha(screen, 'red')
# dummy = chr.Dummy(screen)

flag = 1
select_phase = 1
starting_screen = pygame.image.load(path.join(img_dir, 'starting_screen.png')).convert()
starting_screen_rect = starting_screen.get_rect()
main_menu = pygame.image.load(path.join(img_dir, 'main_menu.png')).convert()
main_menu_rect = main_menu.get_rect()
main_menu_rect.x, main_menu_rect.y = 1000, 0
bg = pygame.image.load(path.join(img_dir, 'image.png')).convert()
bg_rect = bg.get_rect()
font = pygame.font.Font(None, 40)
font_color = (0, 160, 145)
font_2 = pygame.font.Font(None, 40)
font_2_color = (255, 10, 100)

font_menu = pygame.font.Font(None, 32)
font_menu_color = (255, 153, 0)
t_main_menu = font_menu.render('Player ' + str(select_phase) + ', choose the character. Arrows to navigate, "O" to show description', True, font_menu_color)
t_main_menu_rect = t_main_menu.get_rect()
t_main_menu_rect.x, t_main_menu_rect.y = 1060, -50


font2 = pygame.font.Font(None, 50)
font2_color = (0,200,150)
t = font2.render("game xd. press z to proceed(OMG Z??????)", True, font2_color)
t_rect = t.get_rect()
t_rect.centerx, t_rect.centery = 500, -10
'''
player1_group = pygame.sprite.Group()
player1_group.add(player)
player2_group = pygame.sprite.Group()
player2_group.add(player2)
player.enemy = player2
player2.enemy = player
player.enemygroup = player2_group
player2.enemygroup = player1_group
'''
font_desc = pygame.font.Font(None, 25)
font_desc_color = (0, 255, 240)

curchr = 1
chrs = ['', 'NikitaDev', 'Lesha', 'Grisha', 'Bogdan', 'Georg', 'Nikita', 'Senia', 'Kostya', 'Vadim']
classes = ['', chr.Player, chr.Lesha, chr.Grisha, chr.Bogdan, chr.Georg, chr.Nikita, chr.Senia, chr.Kostya, chr.Vadim]
imgs = ['', 'Nikita.png', 'lesha.png', 'Grisha.png', 'Bogdan.png', 'Georg.png', 'Nikita.png', 'Senia.png', 'Kostya.png', 'Vadim.png']

font3 = pygame.font.Font(None, 30)
font3_color = (0, 204, 0)
t_chr = font.render('< '+chrs[curchr]+' >', True, font3_color)
t_chr_rect = t_chr.get_rect()
t_chr_rect.centerx = 450
t_chr_rect.y = 350

select_cd = 1
# bullet1 = chr.TestingBullet(enemygroup=player1_group, screen=screen, speed=10, x=540)

# Цикл игры
'''
                if not select_phase:
                    if not select_phase:
                        a = 'NikitaDev'
                        p = 'Nikita.png'
                        player = chr.Player(screen, 'blue')
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
                        p2 = 'Nikita.png'
                        player2 = chr.Player(screen, 'red')
                        player.enemy = player2
                        player2.enemy = player
                        player1_group = pygame.sprite.Group()
                        player1_group.add(player)

                        player2_group = pygame.sprite.Group()
                        player2_group.add(player2)

                        player.enemygroup = player2_group
                        player2.enemygroup = player1_group
                        
                        
            font_desc_color = (0, 255, 240)
            t_chrDesc = font_desc.render(player.chr + '        ' + player.chr_desc, True, font_desc_color)
            t_ab1Desc = font_desc.render(player.ability1_name + '        ' + player.ability1_desc, True, font_desc_color)
            t_ab2Desc = font_desc.render(player.ability2_name + '        ' + player.ability2_desc, True, font_desc_color)
            if player.ability3_name != '':
                t_ab3Desc = font_desc.render(player.ability3_name + '        ' + player.ability3_desc, True, font_desc_color)
            else:
                t_ab3Desc = font_desc.render('', True, font_desc_color)
'''
running = True
while running:
    # print(flag, select_phase)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z and flag == 1:
                flag = 2
                break
            if event.key == pygame.K_RIGHT and flag == 2:
                curchr += 1
                if curchr > len(chrs) - 1:
                    curchr = 1
                t_chr = font.render('< '+chrs[curchr]+' >', True, font3_color)
                t_chr_rect = t_chr.get_rect()
                t_chr_rect.centerx = 450
                t_chr_rect.y = 350
            if event.key == pygame.K_LEFT and flag == 2:
                curchr -= 1
                if curchr < 1:
                    curchr = len(chrs) - 1
                t_chr = font.render('< ' + chrs[curchr] + ' >', True, font3_color)
                t_chr_rect = t_chr.get_rect()
                t_chr_rect.centerx = 450
                t_chr_rect.y = 350
            if event.key == pygame.K_z and flag == 2 and select_phase == 1:
                a = chrs[curchr]
                p = imgs[curchr]
                player = classes[curchr](screen, 'blue')
                select_phase = 2
                curchr = 1
                t_main_menu = font_menu.render('Player ' + str(select_phase) + ', choose the character. Arrows to navigate, "O" to show description', True, font_menu_color)

                break
            if event.key == pygame.K_z and flag == 2 and select_phase == 2:
                a2 = chrs[curchr]
                p2 = imgs[curchr]
                player2 = classes[curchr](screen, 'red')
                player.enemy = player2
                player2.enemy = player
                player1_group = pygame.sprite.Group()
                player1_group.add(player)

                player2_group = pygame.sprite.Group()
                player2_group.add(player2)

                player.enemygroup = player2_group
                player2.enemygroup = player1_group
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

                t_chr2 = font_2.render('Player 2: ' + a2, True, font_2_color)
                t_chr2_rect = t_chr2.get_rect()
                t_chr2_rect.centerx = WIDTH - 170
                t_chr2_rect.centery = 30

                flag = 0
            if event.key == pygame.K_o and flag == 2:
                flag = 3
                chr_1 = pygame.image.load(path.join(img_dir, imgs[curchr])).convert()
                chr1_rect = chr_1.get_rect()
                chr1_rect.x = 10
                chr1_rect.y = 10
                xd = classes[curchr](screen, 'blue')
                chr_desc = font_desc.render(xd.chr_desc, True, font_desc_color)
                chr_desc_rect = chr_desc.get_rect()
                ab1_desc = font_desc.render(xd.ability1_desc, True, font_desc_color)
                ab1_desc_rect = ab1_desc.get_rect()
                ab2_desc = font_desc.render(xd.ability2_desc, True, font_desc_color)
                ab2_desc_rect = ab2_desc.get_rect()
                ab3_desc = font_desc.render(xd.ability3_desc, True, font_desc_color)
                ab3_desc_rect = ab3_desc.get_rect()
                ab1_name = font_desc.render(xd.ability1_name, True, font_desc_color)
                ab1_name_rect = ab1_name.get_rect()
                ab2_name = font_desc.render(xd.ability2_name, True, font_desc_color)
                ab2_name_rect = ab2_name.get_rect()
                ab3_name = font_desc.render(xd.ability3_name, True, font_desc_color)
                ab3_name_rect = ab3_name.get_rect()

                chr_desc_rect.x, chr_desc_rect.y = 50, 170-180

                ab1_desc_rect.x, ab1_desc_rect.y = 150-180, 340
                ab1_name_rect.x, ab1_name_rect.y = 10-180, 340

                ab2_desc_rect.x, ab2_desc_rect.y = 150+180, 410
                ab2_name_rect.x, ab2_name_rect.y = 10+180, 410

                ab3_desc_rect.x, ab3_desc_rect.y = 150-180, 480
                ab3_name_rect.x, ab3_name_rect.y = 10-180, 480


            if event.key == pygame.K_x and flag == 3:
                flag = 2

    if not flag:
        # 195, 225
        screen.blit(bg, bg_rect)
        screen.blit(t_chr1, t_chr1_rect)
        screen.blit(t_chr2, t_chr2_rect)

        pygame.draw.rect(screen, RED, (200, 75, 30, (1000 - player.hp) // 3.3 // 2))
        pygame.draw.rect(screen, GREEN, (200, (75 + (1000 - player.hp) // 3.3 // 2), 30, player.hp // 3.3 // 2))
        pygame.draw.rect(screen, RED, (770, 75, 30, (1000 - player2.hp) // 3.3 // 2))
        pygame.draw.rect(screen, GREEN, (770, (75 + (1000 - player2.hp) // 3.3 // 2), 30, player2.hp // 3.3 // 2))

        player.update2()
        player2.update2()
        player.update()
        player2.update()
        player.draw()
        player2.draw()

        time = chr.time
        if time == 1:
            pil_string_image = pygame.image.tostring(player.image, "RGBA", False)
            pil_image = image.frombytes('RGBA', (85, 100), bytes(pil_string_image))
            pixels = pil_image.load()
            x, y = pil_image.size
            for i in range(x):
                for j in range(y):
                    lol = sum(pixels[i, j])
                    if lol != 255 * 3:
                        pixels[i, j] = *[lol // 3 - 1 if lol > 0 else lol], *[lol // 3 - 1 if lol > 0 else lol], *[
                            lol // 3 - 1 if lol > 0 else lol]
                    else:
                        pixels[i, j] = 200, 200, 200
                        # pixels[i, j] = lol // 3, lol // 3, lol // 3

            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()

            py_image = pygame.image.fromstring(data, size, mode)
            py_image.set_colorkey((200, 200, 200))
            screen.blit(py_image, player.rect)
        if time == 2:
            pil_string_image = pygame.image.tostring(player2.image, "RGBA", False)
            pil_image = image.frombytes('RGBA', (85, 100), bytes(pil_string_image))
            pixels = pil_image.load()
            x, y = pil_image.size
            for i in range(x):
                for j in range(y):
                    lol = sum(pixels[i, j])
                    if lol != 255 * 3:
                        pixels[i, j] = *[lol // 3 - 15 if lol > 16 else lol], *[lol // 3 - 15 if lol > 16 else lol], *[lol // 3 - 15 if lol > 16 else lol]
                        #pixels[i, j] = lol // 3, lol // 3, lol // 3
                    else:
                        pixels[i, j] = 200, 200, 200

            mode = pil_image.mode
            size = pil_image.size
            data = pil_image.tobytes()

            py_image = pygame.image.fromstring(data, size, mode)
            py_image.set_colorkey((200, 200, 200))
            screen.blit(py_image, player2.rect)

        # print(f'canblock {player.canblock}, blockdur {player.blockdur}, dur {player.dur}')
        # print(f'canblock2 {player2.canblock}, blockdur2 {player2.blockdur}, dur2 {player2.dur}')
        # bullet1.update()
        screen.blit(chr_1, chr1_rect)
        screen.blit(chr_2, chr2_rect)
    if flag == 1:
        screen.blit(starting_screen, starting_screen_rect)
        screen.blit(t, t_rect)
        if t_rect.y < 50:
            t_rect.y += 5
    elif flag == 2:
        screen.blit(main_menu, main_menu_rect)
        screen.blit(t_main_menu, t_main_menu_rect)
        if starting_screen_rect.x >= -1000:
            screen.blit(starting_screen, starting_screen_rect)
            screen.blit(t, t_rect)
            starting_screen_rect.x -= 20
            t_rect.x -= 20
            main_menu_rect.x -= 20
            t_main_menu_rect.x -= 20
        else:
            if t_main_menu_rect.y < 30:
                t_main_menu_rect.y += 5
            screen.blit(t_chr, t_chr_rect)
    elif flag == 3:
        screen.fill(BLACK)
        screen.blit(chr_1, chr1_rect)
        screen.blit(chr_desc, chr_desc_rect)
        screen.blit(ab1_desc, ab1_desc_rect)
        screen.blit(ab2_desc, ab2_desc_rect)
        screen.blit(ab3_desc, ab3_desc_rect)
        screen.blit(ab1_name, ab1_name_rect)
        screen.blit(ab2_name, ab2_name_rect)
        screen.blit(ab3_name, ab3_name_rect)
        if chr_desc_rect.y < 170:
            chr_desc_rect.y += 3
            ab1_desc_rect.x += 3
            ab1_name_rect.x += 3
            ab2_desc_rect.x -= 3
            ab2_name_rect.x -= 3
            ab3_desc_rect.x += 3
            ab3_name_rect.x += 3



    pygame.display.update()


pygame.quit()