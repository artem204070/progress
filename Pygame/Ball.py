import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, speed, filename, score, type, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect(center=(x, 0))
        self.speed = speed
        self.score = score
        self.type = type
        self.add(group)

    def update(self, height):
        if self.rect.y < height - 20:
            self.rect.y += self.speed
        else:
            self.kill()
