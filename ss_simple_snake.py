import pygame
import player
import food
import operator
import pickle


class Game_Window(object):
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((410, 410), 0, 32)
        self.clock = pygame.time.Clock()
        self.player = player.Snake(400, 400)
        self.foodpile = food.Food()

        self.font = pygame.font.SysFont('Comic Sans MS', 40)
        self.name = ''
        self.highscore = []

    def blit_grid(self):
        for x in range(40):
            pygame.draw.aaline(self.screen, (255, 255, 255), (x * 10, 0), (x * 10, 400))
        for y in range(40):
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, y * 10), (400, y * 10))

    def show_highscore(self):
        self.screen.fill((255, 255, 255))
        text = self.font.render('GAME OVER ', True, (255, 0, 0))
        textheight = 1.5 * text.get_height()
        self.screen.blit(text, (200 - text.get_width() / 2, 50))
        t2 = 'POINT : ' + str(self.player.point)
        text2 = self.font.render(t2, True, (255, 0, 0))
        self.screen.blit(text2, (200 - text2.get_width() / 2, 50 + textheight))
        i = 2
        s_highscore = sorted(self.highscore, key=operator.itemgetter(1), reverse=True)
        for score in s_highscore:
            s = self.font.render(score[0] + ': ' + str(score[1]), True, (0, 0, 0))
            self.screen.blit(s, (200 - text2.get_width() / 2, 50 + (i * textheight)))
            i = i + 1
        self.save_highscore()
        pygame.display.update()

    def save_highscore(self):
        with open('highscore.snake','w') as f:
            pickle.dump(self.highscore, f)

    def load_highscore(self):
        with open('highscore.snake','r') as f:
            self.highscore = pickle.load(f)

    def game_over(self):
        running = True
        time = 0
        while running:
            time += self.clock.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN and time > 1500:
                    running = False
            self.show_highscore()
        self.player.is_dead = False
        self.clock.tick()
        self.player.restart()
        self.foodpile.restart()

    def run(self):
        self.load_highscore()
        while True:
            if self.name == '':
                self.get_name()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.screen.fill((255, 255, 255))

            dt = self.clock.tick()
            self.player.update(dt, self.screen)
            self.foodpile.update(dt, self.screen, self.player)
            self.blit_grid()

            if self.player.is_dead:
                self.highscore.append((self.name, self.player.point))
                self.game_over()
                self.name = ''

            point = self.font.render(str(self.player.point), True, (0, 0, 0))
            self.screen.blit(point, (0, 0))
            pygame.display.update()

    def get_name (self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode
            self.screen.fill((255, 255, 255))
            text = self.font.render('ENTER NAME: ', True, (0, 0, 0))
            self.screen.blit(text, (200 - text.get_width() / 2, 200 - text.get_height()))
            t2 = str(self.name) + '_'
            text2 = self.font.render(t2, True, (0, 0, 0))
            self.screen.blit(text2, (200 - text2.get_width() / 2, 200 + text2.get_height()))

            pygame.display.update()

if __name__ == '__main__':
    app = Game_Window()
    app.run()
