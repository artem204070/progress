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
        super().update()

        if time.time() - self.last_shot_time > self.shoot_cooldown:
            self.shoot_stone(self.player.rect.centerx, self.player.rect.centery)
            self.last_shot_time = time.time()

    def shoot_stone(self, target_x, target_y):
        stone = Stone(self.rect.centerx, self.rect.centery, target_x, target_y, damage=10)
        self.stone_group.add(stone)