import pygame
class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=7):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        dx = target_x - x
        dy = target_y - y
        dist = (dx**2 + dy**2) ** 0.5
        self.vx = speed * dx / dist
        self.vy = speed * dy / dist

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)