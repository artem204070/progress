import pygame
from Pygame.FrogPlatformer.Module.SpriteSheet import SpriteSheet


class Kiwi(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Создаем rect для спрайта
        self.rect = pygame.Rect(x, y, w, h)

        self.collide = True  # флаг, который указывает, что объект может сталкиваться с игроком
        self.collectable = True  # флаг, который указывает на то, что объект можно собрать
        self.collected = False  # флаг, собрали / не собрали

        self.topoffset = 18
        self.xoffset = 19

        self.sound = pygame.mixer.Sound("sound/kiwi.mp3")

        self.idle_length = 17
        kiwi_idle = SpriteSheet(pygame.image.load('Assest/Collectables/kiwi.png'))
        self.idle = [kiwi_idle.getImage(32 * x, 0, 32, 32) for x in range(self.idle_length)]
        self.idle_state = 0
        self.delay = 2  # длительность анимации
        self.current_delay = 0

        self.death_length = 6
        kiwi_death = SpriteSheet(pygame.image.load('Assest/Collectables/collected.png'))
        self.death = [kiwi_death.getImage(32 * x, 0, 32, 32) for x in range(self.death_length)]
        self.death_state = 0

        self.d_delay = 2
        self.d_current_delay = 0

        # Устанавливаем начальное изображение
        self.image = pygame.transform.scale(self.idle[0], (self.w, self.h))

    def update(self):

        # Обновляем анимацию
        if not self.collected:
            # Анимация idle
            if self.current_delay == self.delay:
                self.idle_state += 1
                self.current_delay = 0
            else:
                self.current_delay += 1


            # Обновляем изображение для отрисовки
            self.image = pygame.transform.scale(
                self.idle[self.idle_state % self.idle_length],
                (self.w, self.h)
            )
        else:
            # Анимация смерти
            self.sound.play()
            if self.death_state <= self.death_length:
                if self.d_current_delay == self.d_delay:
                    self.death_state += 1
                    self.d_current_delay = 0
                else:
                    self.d_current_delay += 1

                # Обновляем изображение для отрисовки
                self.image = pygame.transform.scale(
                    self.death[self.death_state % self.death_length],
                    (self.w, self.h)
                )
            else:
                self.kill()