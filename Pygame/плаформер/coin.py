import  pygame
from  const import *
import math

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, group, attached_platform=None):
        pygame.sprite.Sprite.__init__(self, group)
        self.current_display_witdh = None
        self.radius = COIN_RADIUS
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.rect = self.image.get_rect(center=(x, y))
        self.attached_platform = attached_platform
        self.anim_time = 0
        self.anim_speed = 0.15
        self.max_anim_width = self.radius * 2
        self.min_anim_width = 2

        if self.attached_platform:
            self.offset_x = self.rect.centerx - self.attached_platform.rect.centerx
            self.offset_y = self.rect.centery - self.attached_platform.rect.centery


    def update(self):
        self.anim_time += self.anim_speed
        current_width_factor = (math.sin(self.anim_time) + 1) / 2
        self.current_display_witdh = self.min_anim_width + \
                                     (self.max_anim_width - self.min_anim_width) * current_width_factor

        self.current_display_witdh = max(
            self.min_anim_width,
            min(self.current_display_witdh, self.max_anim_width)
        )

        if self.attached_platform:
            self.rect.centerx = self.attached_platform.rect.centerx + self.offset_x
            self.rect.centery = self.attached_platform.rect.centery + self.offset_y

    def draw(self, screen):
        display_rect = pygame.Rect(
            self.rect.centerx - self.current_display_witdh / 2,
            self.rect.centery - self.radius,
            self.current_display_witdh,
            self.radius * 2
        )

        pygame.draw.ellipse(screen, YELLOW, display_rect)