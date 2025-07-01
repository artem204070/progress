import pygame
import time
from Pygame.FrogPlatformer.Objeckt.enemy import *
import pygame
from Pygame.FrogPlatformer.Objeckt.Stone import *

class FlyingEnemy(Enemy):
    def __init__(self, x, y, damage, health, platform_group, bullet_group, player):
        super().__init__(x, y, damage, health, 4, platform_group)
        self.flying_speed = 3
        self.fly_direction = 1
        self.stone_group = bullet_group
        self.player = player
        self.shoot_cooldown = 3.0
        self.last_shot_time = time.time()
        self.original_y = y
        self.fly_height = 150
        self.graviti = 0


    def update(self):
        self.vel_y -= 1

        if self.rect.y < self.original_y - self.fly_height:
            self.fly_direction = 1
        elif self.rect.y > self.original_y + self.fly_height:
            self.fly_direction = -1

        self.rect.x += self.speed * self.direction

        if time.time() - self.move_time_start > self.move_duration:
            self.direction *= -1
            self.move_time_start = time.time()

        look_ahead = self.rect.x + self.speed * self.direction * 2
        look_rect = pygame.Rect(look_ahead, self.rect.y, self.width, self.height)

        for platform in self.platform_group:
            if look_rect.colliderect(platform.rect):
                self.direction *= -1
                self.move_time_start = time.time()
                break

        if time.time() - self.last_shot_time > self.shoot_cooldown:
            self.shoot_stone(self.player.rect.centerx, self.player.rect.centery)
            self.last_shot_time = time.time()

    def shoot_stone(self, target_x, target_y):
        stone = Stone(self.rect.centerx, self.rect.centery, target_x, target_y, damage=10)
        self.stone_group.add(stone)