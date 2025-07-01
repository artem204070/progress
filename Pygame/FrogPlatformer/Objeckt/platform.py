import pygame
from Pygame.FrogPlatformer.Module.SpriteSheet import SpriteSheet


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_w, platform_h, image_x, image_y, image_w, image_h):
        pygame.sprite.Sprite.__init__(self)
        terrain_sheet = SpriteSheet(pygame.image.load("Assest/Terrain/terrain.png"))
        single_image = terrain_sheet.getImage(image_x, image_y, image_w, image_h)
        self.image = pygame.Surface((platform_w, platform_h))

        for len_x in range(0, platform_w, image_w):
            for len_y in range(0, platform_h, image_h):
                self.image.blit(single_image, (len_x, len_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
