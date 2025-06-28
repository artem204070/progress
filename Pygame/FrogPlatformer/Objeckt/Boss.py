import time
from Pygame.FrogPlatformer.Objeckt.Stone import *
from Pygame.FrogPlatformer.Objeckt.enemy import *

class Boss(Enemy):
    def __init__(self, x, y, damage, health, platform_group, stone_group, player):
        super().__init__(x, y, damage, health, 3, platform_group)
        self.stone_group = stone_group
        self.player = player
        self.shoot_cooldown = 3.0
        self.last_shot_time = time.time()

    def update(self):
        super().update()
        player_x = self.player.rect.centerx
        now = time.time()
        if now - self.last_shot_time > self.shoot_cooldown:
            self.shoot_stone(player_x, self.player.rect.centery)
            self.last_shot_time = now

    def shoot_stone(self, target_x, target_y):
        stone = Stone(self.rect.centerx, self.rect.centery, target_x, target_y)
        self.stone_group.add(stone)