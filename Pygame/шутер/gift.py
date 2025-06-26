import pygame
from consts import *
import random

pink = (255,181,197)
class Gift(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.radius = random.randint(CIRCLE_RADIUS_MIN, CIRCLE_RADIUS_MAX)
        self.color = random.choice([pink])
        self.is_moving = random.choice([True, False, True])

        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

        if self.is_moving:
            self.dx = random.randint(CIRCLE_SPEED_MIN, CIRCLE_SPEED_MAX) * random.choice([-1, 1])
            self.dy = random.randint(CIRCLE_SPEED_MIN, CIRCLE_SPEED_MAX) * random.choice([-1, 1])
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        if self.is_moving:
            self.rect.x += self.dx
            self.rect.y += self.dy

            if self.rect.left <= 0:
                self.rect.left = 0
                self.dx = abs(self.dx)
            elif self.rect.right >= WIDTH:
                self.rect.right = WIDTH
                self.dx = abs(self.dx) * (-1)

            if self.rect.top <= 0:
                self.rect.top = 0
                self.dy = abs(self.dy)
            elif self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.dy = abs(self.dy) * (-1)