from Pygame.FrogPlatformer.Objeckt.player import *

class Camera:
    def __init__(self, level_length):
        self.speed = 6
        self.x = self.speed
        self.y = 0
        self.pos_x = 0
        self.level_length = level_length

    def move(self, obj):
        obj.rect.x -= self.x
        if isinstance(obj, Player):
            if self.x != 0:
                self.pos_x += self.x

    def check(self, player, width, height):
        screen_x = player.world_x - self.pos_x

        if screen_x < 200:
            if self.pos_x > 0:
                self.x = -self.speed
                return True

        if screen_x > width - 200:
            if self.pos_x < self.level_length - width:
                self.x = self.speed
                return True
        self.x = 0
        return False