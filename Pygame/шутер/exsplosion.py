import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, color):
        pygame.sprite.Sprite.__init__(self)
        self.frames = 15
        self.current_frames = 0
        self.max_radius = 50
        self.color = color
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2))
        self.rect = self.image.get_rect(center=center)
        self.radius = 1

    def update(self):
        self.image.fill((0, 0, 0, 0))
        if self.current_frames < self.frames:
            alpha = int(255 * (1 - self.current_frames / self.frames))
            pygame.draw.circle(
                self.image,
                (*self.color[:3], alpha),
                (self.max_radius, self.max_radius),
                self.radius,
            )
            self.radius += self.max_radius // self.frames
            self.current_frames += 1
        else:
            self.kill()