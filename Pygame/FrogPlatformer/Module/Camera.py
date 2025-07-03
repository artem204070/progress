class Camera:
    def __init__(self, level_length):
        self.level_length = level_length

    def get_offset(self, player, screen_width):
        offset_x = player.world_x - screen_width // 2 + player.rect.width // 2
        offset_x = max(0, min(offset_x, self.level_length - screen_width))
        return offset_x, 0