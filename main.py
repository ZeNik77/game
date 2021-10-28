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
        self.image = pygame.image.load(path.join(img_dir, 'sprite2.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speedx = 2.5
    def update(self):
        self.rect.x += self.speedx
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speedx = -1 * self.speedx


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
