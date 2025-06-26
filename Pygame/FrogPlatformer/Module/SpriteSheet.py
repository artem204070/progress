import pygame

class SpriteSheet:
    def __init__(self, image):
        self.ss = image.convert_alpha() # делаем картинки без фона (прозрачные)

    def getImage(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.ss, (0, 0), (x, y, width, height))
        image.set_colorkey((0, 0, 0)) # делаем черный прозрачным

        return image