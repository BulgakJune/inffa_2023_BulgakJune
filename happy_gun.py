import math
from random import choice
import random as rnd
import pygame


FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


##КЛАСС МЯЧЕЙ МЯЧЕЙ МЯЧЕЙ##
class Ball:
    def __init__(self, screen: pygame.Surface, x, y): #screen: pygame.Surface проверяет тип объекта на вход
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали"""     
        
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.g = 0.6
        self.color = choice(GAME_COLORS)
        self.live = 1
        self.time = 130

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.g
        self.x += self.vx
        self.y -= self.vy
        if self.y > 570:
            self.y = 569
            self.vy=-self.vy
        if self.x > 780:
            self.vx=-self.vx    
    
    def notdeath(self):
        while self.time > 0:
            self.time -= 1
            return True
            pygame.display.update()
       
    def draw(self): #ДОБАВИТЬ ВРЕМЯ ЖИЗНИ ПУЛИ!!! #upd: добавили
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False."""
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 <= self.r + obj.r:  # Условие сближения центров
            # шарика и цели на расстояние, меньшее суммы их радиусов
            return True
        else:
            return False
                
    def smert(self):
        self.x = -30
        self.y = 0
        self.vx = -50
        self.vy = 0
     
##КЛАСС РУЖЕЙ РУЖЕЙ РУЖЕЙ##
class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.lengh=45
        self.wid=5
        self.color = GREY
        

    def fire2_start(self, event=''):
        self.f2_on = 1 #следит за мышкой если 0 (состояние покоя) и находится в состоянии выстрела если 1
        while  self.f2_on==1 and self.lengh < 70:
            self.lengh = self.lengh + 0.0001
        
    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.        """

        global balls, bullet #global остаётся в памяти до конца работы пограммы, массив balls
        bullet += 1
        new_ball = Ball(self.screen, xa, ya)
        new_ball.r += 5
        self.an = math.atan2(event.pos[1]-new_ball.y, event.pos[0]-new_ball.x) #pos массив координат, угол выстрела
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10
        

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20)) #pos массив координат, угол выстрела
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, [40, 450], [40 + self.lengh * math.cos(self.an), 450 + self.lengh * math.sin(self.an)], self.wid)
          
        global xa, ya
        xa = 40 + self.lengh * math.cos(self.an)
        ya = 450 + self.lengh * math.sin(self.an)
        
    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    
        

class Target:
    def __init__(self, screen):
        self.screen = screen
        self.points = 0
        self.live = 1 #1 если жива 0 если не жива
        self.x = 300
        self.y = 200
        self.r = 30
        self.vx = 10
        self.vy = 7
        self.color = RED   
       
    def move(self):
        self.x += self.vx
        self.y -= self.vy
        if self.y > 570:
            self.y = 569
            self.vy=-self.vy
        if self.x > 780:
            self.x = 779
            self.vx=-self.vx
        if self.y < 50:
            self.y = 51
            self.vy=-self.vy
        if self.x < 200:
            self.x = 201
            self.vx=-self.vx
        # именно благодаря этой функции файл называется happy gun, а не просто gun :)

    def count(self, screen, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = rnd.randint(600, 740)
        self.y = rnd.randint(300, 550)
        self.r = rnd.randint(10, 50)
        self.color = rnd.choice(GAME_COLORS)
        self.vx = rnd.randint(5, 42)
        self.vy = rnd.randint(5, 42)
        self.move()

    def hit(self, points=1):
        for b in balls:
            if b.hittest(self): #(объект).hittest(self (не пишется), объект (target, в классе target пишется как self))
                self.points += points
                b.smert()
                
    def draw(self):
        if self.live:
            pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r)
        screen.blit(screen, (25, 25))
        self.count(screen, str(self.points), 18, 20, 20)
        # перестанет отрисовываться когда умрёт? 
        # upd: перестало



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    target.move()
    for b in balls:
        if b.notdeath():
            b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target)==True:
            target.hit()
            target.new_target()
    gun.power_up()

pygame.quit()
