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

class MovePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_w, platform_h, image_x, image_y, image_w, image_h, move_x, move_y, move_distance, move_speed):
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

        self.original_x = x
        self.original_y = y
        self.move_x = move_x
        self.move_y = move_y
        self.move_distance = move_distance
        self.move_speed = move_speed
        self.current_distance = 0

    def update(self):
        if self.move_distance > 0:
            dx = self.move_x * self.move_speed
            dy = self.move_y * self.move_speed

            self.rect.x += dx
            self.rect.y += dy

            self.current_distance += abs(dx) + abs(dy)

            if self.current_distance >= self.move_distance:
                self.move_x *= -1
                self.move_y *= -1
                self.current_distance = 0