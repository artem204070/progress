import pygame
from const import *

class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, start_val, end_val, move_axis, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_axis = move_axis
        self.start_val = start_val
        self.end_vel = end_val
        self.speed = 3
        self.direction = 1
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.current_vel_x = 0
        self.current_vel_y = 0


    def update(self):
        prev_x = self.rect.x
        prev_y = self.rect.y

        if self.move_axis == 'x':
            self.rect.x += self.speed * self.direction
            if self.direction == 1 and self.rect.x >= self.end_vel:
                self.rect.x = self.end_vel
                self.direction = -1
            elif self.direction == -1 and self.rect.x <= self.start_val:
                self.rect.x = self.start_val
                self.direction = 1
            self.current_vel_x = self.rect.x - prev_x
            self.current_vel_y = 0
        elif self.move_axis == 'y':
            self.rect.y += self.speed * self.direction
            if self.direction == 1 and self.rect.y >= self.end_vel:
                self.rect.y = self.end_vel
                self.direction = -1
            elif self.direction == -1 and self.rect.y <= self.start_val:
                self.rect.y = self.start_val
                self.direction = 1
            self.current_vel_y = self.rect.y - prev_y
            self.current_vel_x = 0

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, self.rect)