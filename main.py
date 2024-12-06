import pygame
import random
import sys
import math
WIDTH = 1200
HEIGHT = 800
FPS = 30
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
pygame.display.set_caption("Мыльные пузыри")
clock = pygame.time.Clock()
velocity_x = 6
velocity_y = 2
class Gra_obj:
    def __init__(self, posx, posy, color):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.typ_obj = ''
    def fly(self):
        self.posy -= random.randint(0, velocity_y)
        self.posx += random.randint(0,velocity_x * 2) - velocity_x

class Gra_rect(Gra_obj):
    def __init__(self, posx, posy, color, h, w):
        super().__init__( posx, posy, color)
        self.h = h
        self.w = w
    def draw_obj(self, screen):
        rect = pygame.Rect(self.posx, self.posy, self.w, self.h)
        pygame.draw.rect(screen, self.color, rect, 0)
    def rect_obj(self):
        return pygame.Rect(self.posx, self.posy, self.w,self.h)

class Gra_cir(Gra_obj):
    def __init__(self,posx, posy, color, r):
         super().__init__( posx, posy, color)
         self.r = r

    def draw_obj(self, screen):
         pygame.draw.circle(screen, self.color, (self.posx, self.posy),self.r, 0)
    def rect_obj(self):
        return pygame.Rect(self.posx-self.r, self.posy-self.r, self.r*2,self.r*2)


#объекты игры
borders = []
balls = []
border_w = 4
rect = Gra_rect
b1 = rect(0,0,BLUE,border_w,WIDTH)
borders.append(b1)
b1 = rect(0,0,BLUE,HEIGHT,border_w)
borders.append(b1)
b1 = rect(0,HEIGHT-border_w,BLUE,border_w,WIDTH)
borders.append(b1)
b1 = rect(WIDTH-border_w,0,BLUE,HEIGHT, border_w)
borders.append(b1)

ball_obj = Gra_cir
ball_status = 'wait'
ball_x = 0
ball_y = 0
ball_r = 0
#ball_new = ball_obj(0,0,BLACK,0)

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка мыши
                if ball_status == 'wait':
                    ball_status = 'radius'
                    ball_x, ball_y = pygame.mouse.get_pos()
                    ball_color = ( random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    ball_new = ball_obj(ball_x, ball_y,ball_color,0)

        if event.type == pygame.MOUSEBUTTONUP:
            if ball_status == 'radius':
                ball_status = 'wait'
                balls.append(ball_new)
        if event.type == pygame.MOUSEMOTION:
            if ball_status == 'radius':
                ball_xe, ball_ye = pygame.mouse.get_pos()
                ball_r = math.isqrt((ball_xe - ball_x) ** 2 + (ball_ye - ball_y) ** 2)
                ball_new.r = ball_r

# вывод границ
    screen.fill(BLACK)
    for border in borders:
        border.draw_obj(screen)
# вывод пузырей
    if ball_status == 'radius':
        ball_new.draw_obj(screen)
# проверка границ экрана
    for border in borders:
        for ball in balls:
            if border.rect_obj().colliderect(ball.rect_obj()):
                balls.remove(ball)
# проверка столкновения пузырей
    test = True
    while test:
        test = False
        for i in  range(len(balls)):
            if not test:
                for j in range(i+1,len(balls)):
                    if balls[i].rect_obj().colliderect(balls[j].rect_obj()):
                        balls.remove(balls[j])
                        balls.remove(balls[i])
                        test = True
                        break


    for ball in balls:
        ball.draw_obj(screen)
        ball.fly()
# Обновление экрана
    pygame.display.flip()
pygame.quit()
sys.exit()