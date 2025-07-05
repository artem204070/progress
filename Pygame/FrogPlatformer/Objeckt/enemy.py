import pygame
import time
from Pygame.FrogPlatformer.Module.SpriteSheet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, health, type, platform_group):
        pygame.sprite.Sprite.__init__(self)

        self.invincible_enemy = False
        self.invincible_time_enemy = 0
        self.invincible_duration_enemy = 1.5

        self.width = 60
        self.height = 60
        if type == 1:
            self.run_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Pink_Monster_run.png"))
            self.run_frames = [self.run_sheet.getImage(32 * x, 0, 32, 32) for x in range(6)]
            self.death_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Pink_Monster_Death_8.png"))
            self.death_frames = [self.death_sheet.getImage(32 * x, 0, 32, 32) for x in range(8)]
        elif type == 2:
            self.run_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Owlet_Monster_Run_6.png"))
            self.run_frames = [self.run_sheet.getImage(32 * x, 0, 32, 32) for x in range(6)]
            self.death_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Owlet_Monster_Death_8.png"))
            self.death_frames = [self.death_sheet.getImage(32 * x, 0, 32, 32) for x in range(8)]
        elif type == 3:
            self.width = 90
            self.height = 90
            self.run_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Dude_Monster_Run_6.png"))
            self.run_frames = [self.run_sheet.getImage(32 * x, 0, 32, 32) for x in range(6)]
            self.death_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Dude_Monster_Death_8.png"))
            self.death_frames = [self.death_sheet.getImage(32 * x, 0, 32, 32) for x in range(8)]
        elif type == 4:
            self.width = 128
            self.height = 128
            self.run_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Run.png"))
            self.run_frames = [self.run_sheet.getImage(128 * x, 0, 128, 128) for x in range(7)]
            self.death_sheet = SpriteSheet(pygame.image.load("Assest/Enemy/Dead.png"))
            self.death_frames = [self.death_sheet.getImage(128 * x, 0, 128, 128) for x in range(5)]

        self.health = health

        self.death_frame = 0
        self.death_animation_delay = 5
        self.death_animation_counter = 0

        self.current_frame = 0
        self.animation_delay = 5
        self.animation_counter = 0
        self.direction = 1

        self.image = pygame.transform.scale(self.run_frames[0], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.sound = pygame.mixer.Sound("sound/take_damage.mp3")

        self.speed = 3
        self.damage = damage
        self.move_time_start = time.time()
        self.move_duration = 3
        self.platform_group = platform_group
        self.vel_y = 0
        self.graviti = 0.8
        self.on_ground = False

        self.is_death = False


    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter >= self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.run_frames)
            self.animation_counter = 0

        current_image = self.run_frames[self.current_frame]

        if self.direction == -1:
            current_image = pygame.transform.flip(current_image, True, False)

        self.image = pygame.transform.scale(current_image, (self.width, self.height))

        if self.invincible_enemy:
            if int(time.time() * 10) % 2 == 0:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.vel_y += self.graviti
        self.rect.y += int(self.vel_y)

        self.on_ground = False
        for platform in self.platform_group:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        self.rect.x += int(self.speed * self.direction)

        if time.time() - self.move_time_start > self.move_duration:
            self.direction *= -1
            self.move_time_start = time.time()

        if self.on_ground:
            look_ahead_x = self.rect.x + int(self.speed * self.direction)
            look_ahead_rect = pygame.Rect(look_ahead_x, self.rect.bottom + 1, self.width, 1)
            found_platform = False
            for platform in self.platform_group:
                if look_ahead_rect.colliderect(platform.rect):
                    found_platform = True
                    break

            if not found_platform:
                self.direction *= -1
                self.move_time_start = time.time()

        if self.is_death:
            self.speed = 0
            self.death_animation_counter += 1
            if self.death_animation_counter >= self.death_animation_delay:
                self.death_frame += 1
                self.death_animation_counter = 0
                if self.death_frame >= len(self.death_frames):
                    self.kill()
            if self.death_frame < len(self.death_frames):
                self.image = pygame.transform.scale(self.death_frames[self.death_frame], (self.width, self.height))
            return

        if self.invincible_enemy:
            if time.time() - self.invincible_time_enemy > self.invincible_duration_enemy:
                self.invincible_enemy = False

        self.update_animation()

    def damage_player(self, player):
        if not player.invincible:
            self.sound.play()
            player.health -= self.damage
            player.invincible = True
            player.invincible_timer = time.time()

            if player.rect.centerx < self.rect.centerx:
                player.vel_x = -100
            else:
                player.vel_x = 100

            player.vel_y = -10
            player.jumping = True

        if player.health <= 0:
            player.health = 0