import pygame
from os import path
WIDTH = 1000
HEIGHT = 650
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img_dir = path.join(path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(path.join(img_dir, 'blue1.png')).convert()
        self.blue2 = [pygame.image.load(path.join(img_dir, 'blue2_0.png')).convert(),
                      pygame.image.load(path.join(img_dir, 'blue2_1.png')).convert(),
                      pygame.image.load(path.join(img_dir, 'blue2_2.png')).convert(),
                      pygame.image.load(path.join(img_dir, 'blue2_3.png')).convert(),
                      pygame.image.load(path.join(img_dir, 'blue2_4.png')).convert(),
                      pygame.image.load(path.join(img_dir, 'blue2_5.png')).convert(),
                      pygame.image.load(path.join(img_dir, 'blue2_6.png')).convert()]
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (33, HEIGHT - 100)
        self.left = 0
        self.right = 0
        self.animcount = 0
    def update(self):
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
            self.image = pygame.image.load(path.join(img_dir, 'blue1.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect.x += self.speedx


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
img_dir = path.join(path.dirname(__file__), 'Assets')
bg = pygame.image.load(path.join(img_dir, 'image.png')).convert()
bg_rect = bg.get_rect()

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(BLACK)
    screen.blit(bg, bg_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
