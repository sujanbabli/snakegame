import pygame
from pygame.locals import *
import time
import random

GRID_SIZE = 40

class Fruit:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.image = pygame.image.load("apple.jpg").convert()
        self.x = 120
        self.y = 120

    def render(self):
        self.display_surface.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def relocate(self):
        self.x = random.randint(1, 24) * GRID_SIZE
        self.y = random.randint(1, 19) * GRID_SIZE

class Serpent:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.image = pygame.image.load("snake.jpg").convert()
        self.direction = 'down'
        self.size = 1
        self.x = [40]
        self.y = [40]

    def alter_direction(self, new_direction):
        self.direction = new_direction

    def move(self):
        for i in range(self.size - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        directions = {'left': (-GRID_SIZE, 0), 'right': (GRID_SIZE, 0), 'up': (0, -GRID_SIZE), 'down': (0, GRID_SIZE)}
        dx, dy = directions.get(self.direction, (0, 0))
        self.x[0] += dx
        self.y[0] += dy

        self.render()

    def render(self):
        for i in range(self.size):
            self.display_surface.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def enlarge(self):
        self.size += 1
        self.x.append(-1)
        self.y.append(-1)

class ArcadeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Serpent and Fruit Game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.serpent = Serpent(self.surface)
        self.serpent.render()
        self.fruit = Fruit(self.surface)
        self.fruit.render()

    def play_background_music(self):
        pygame.mixer.music.load('music.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        sound = pygame.mixer.Sound(f"{sound_name}.mp3")
        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.serpent = Serpent(self.surface)
        self.fruit = Fruit(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        return x1 >= x2 and x1 < x2 + GRID_SIZE and y1 >= y2 and y1 < y2 + GRID_SIZE

    def is_out_of_bounds(self):
        return self.serpent.x[0] >= 1000 or self.serpent.x[0] < 0 or self.serpent.y[0] >= 800 or self.serpent.y[0] < 0

    def render_background(self):
        bg = pygame.image.load("background4.jpg")
        self.surface.blit(bg, (0, 0))

    def play_game(self):
        self.render_background()
        self.serpent.move()
        self.fruit.render()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.serpent.x[0], self.serpent.y[0], self.fruit.x, self.fruit.y):
            self.play_sound("boom")
            self.serpent.enlarge()
            self.fruit.relocate()

        if self.is_out_of_bounds():
            self.play_sound('collison')
            raise "Out Of Bounds"

        for i in range(3, self.serpent.size):
            if self.is_collision(self.serpent.x[0], self.serpent.y[0], self.serpent.x[i], self.serpent.y[i]):
                self.play_sound('collison')
                raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.serpent.size}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Oops! You lost with a score of {self.serpent.size}.", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to try again or Escape to quit.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        directions = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}
                        self.serpent.alter_direction(directions.get(event.key, 'down'))

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play_game()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(.25)

if __name__ == '__main__':
    arcade_game = ArcadeGame()
    arcade_game.run()
