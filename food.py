import pygame
import random


class Food_piece(object):
    def __init__(self, pos, color=(255, 0, 0)):
        self.m_x = pos[0]
        self.m_y = pos[1]
        self.x = self.m_x * 10
        self.y = self.m_y * 10
        keuze = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        kleur = random.choice(keuze)
        if kleur == 0:
            color = (0,255,0)
        elif kleur == 2:
            color = (254, 254, 1)
        self.color = color

    def blit(self, screen):
        rect = pygame.Rect(self.x, self.y, 10, 10)
        pygame.draw.rect(screen, self.color, rect)


class Food(object):
    def __init__(self):
        self.food = list()

        self.time = 3000
        self.time_tick = 3000

    def random_pos(self, snake):
        running = True
        while running:
            x, y = random.randint(1, 39), random.randint(1, 39)
            running = False
            for t in snake.tail:
                if t.m_x == x and t.m_y == y:
                    running = True
            if x == snake.x and y == snake.y:
                running = True
            for p in self.food:
                if p.m_x == x and p.m_y == y:
                    running = True
        return x, y

    def restart(self):
        self.food = []
        self.time = 300

    def update(self, dt, screen, snake):
        self.time += dt
        if ((self.time >= self.time_tick) or len(self.food) == 0) and len(self.food) < 5:
            self.time = 0
            x, y = self.random_pos(snake)
            f_piece = Food_piece((x, y))
            self.food.append(f_piece)

        for f_piece in self.food:
            if f_piece.m_x == snake.x and f_piece.m_y == snake.y:
                if f_piece.color == (0, 255, 0):
                    snake.increase_lenght(-2, 10, screen)
                elif f_piece.color == (254, 254,1):
                    snake.increase_lenght(-5, 20, screen)
                else:
                    snake.increase_lenght(1, 5, screen)
                self.food.remove(f_piece)
            f_piece.blit(screen)
