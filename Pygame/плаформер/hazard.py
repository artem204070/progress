import  pygame
from const import *

class Hazard(pygame.sprite.Sprite):
    def __init__(self, x, speed, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.radius = HAZARD_RADIUS
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, RED, self.rect.center, self.radius)