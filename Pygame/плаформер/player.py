import pygame
from const import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.vel_x = 0
        self.move_speed = MOVE_SPEED
        self.jump_power = JUMP_POWER
        self.gravity = GRAVITY

        self.is_hit = False
        self.hit_timer = HIT_TIMER
        self.hit_duration = HIT_DURATION

    def update(self, platforms):
        # оброботка кнопок и движения влево в право
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_a]:
            self.vel_x = -self.move_speed

        if keys[pygame.K_d]:
            self.vel_x = self.move_speed

        self.rect.x += self.vel_x

        # обрабатываем столковение с платформой слева справо
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_x > 0:
                    self.rect.right = platform.left
                elif self.vel_x < 0:
                    self.rect.left = platform.right

        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # задаем столкновени с платформой снизу и сверху
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = platform.bottom
                    self.vel_y = 0
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WITDH:
            self.rect.right = WITDH

        if self.is_hit:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.is_hit = False

    def jump(self, platforms):
        self.rect.y += 2
        can_jump = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                can_jump = True
                break
        self.rect.y -= 2
        if can_jump:
            self.vel_y += self.jump_power
    def draw(self, surface):
        color = RED if self.is_hit else BLUE
        pygame.draw.rect(surface, color, self.rect)