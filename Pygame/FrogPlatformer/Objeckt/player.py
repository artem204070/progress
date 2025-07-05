import pygame
from Pygame.FrogPlatformer.Module.SpriteSheet import SpriteSheet
from Pygame.FrogPlatformer.consts import *
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platform_group):
        super().__init__()

        self.width = 45
        self.height = 64

        self.health = 100
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1.5


        self.idle_sheet = SpriteSheet(pygame.image.load("Assest/Player/player_idle.png"))
        self.run_sheet = SpriteSheet(pygame.image.load("Assest/Player/player_run.png"))
        self.jump_sheet = SpriteSheet(pygame.image.load("Assest/Player/player_jump.png"))
        self.fall_sheet = SpriteSheet(pygame.image.load("Assest/Player/player_fall.png"))

        self.idle_frames = [self.idle_sheet.getImage(32 * x, 0, 32, 32) for x in range(11)]
        self.run_frames = [self.run_sheet.getImage(32 * x, 0, 32, 32) for x in range(11)]
        self.jump_frames = [self.jump_sheet.getImage(32 * x, 0, 32, 32) for x in range(1)]
        self.fall_frames = [self.fall_sheet.getImage(32 * x, 0, 32, 32) for x in range(1)]

        self.current_frame = 0
        self.animation_delay = 5
        self.animation_counter = 0

        self.direction = 1 # 1 вправо, -1 влево

        self.max_jumps = 2
        self.jump_count = 0

        self.image = pygame.transform.scale(self.idle_frames[0], (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.space_pressed = False

        self.world_x = x
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 6
        self.gravity = 0.8
        self.jumping = False
        self.on_ground = False
        self.jumping_power = -15

        self.platform_group = platform_group
        self.old_x = x
        self.old_y = y

    def update_animation(self):
        if not self.on_ground:
            if self.vel_y < 0:
                current_image = self.jump_frames[0]
            else:
                current_image = self.fall_frames[0]
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.animation_counter += 1
                if self.animation_counter >= self.animation_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.run_frames)
                    self.animation_counter = 0
                current_image = self.run_frames[self.current_frame]
            else:
                self.animation_counter += 1
                if self.animation_counter >= self.animation_delay:
                    self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                    self.animation_counter = 0
                current_image = self.idle_frames[self.current_frame]

        if self.direction == -1:
            current_image = pygame.transform.flip(current_image, True, False)

        self.image = pygame.transform.scale(current_image, (self.width, self.height))

        if self.invincible:
            if int(time.time() * 10) % 2 == 0:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

        if self.invincible:
            if time.time() - self.invincible_timer > self.invincible_duration:
                self.invincible = False

    def update(self):
        self.old_x = self.rect.x
        self.old_y = self.rect.y

        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.world_x -= self.speed
            self.direction = -1
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.world_x += self.speed
            self.direction = 1
            moving = True

        for platform in self.platform_group:
            if self.rect.colliderect(platform.rect):
                if self.old_x < platform.rect.x:
                    self.rect.right = platform.rect.left
                    self.world_x = self.rect.x
                elif self.old_x > platform.rect.x:
                    self.rect.left = platform.rect.right
                    self.world_x = self.rect.x


        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        self.on_ground = False
        for platform in self.platform_group:
            if self.rect.colliderect(platform.rect):
                if self.old_y < platform.rect.y:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumping = False
                    self.jump_count = 0
                elif self.old_y > platform.rect.y:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0


        if keys[pygame.K_SPACE]:
            if not self.space_pressed and self.jump_count < self.max_jumps:
                self.vel_y = self.jumping_power
                self.jumping = True
                self.jump_count += 1
            self.space_pressed = True
        else:
            self.space_pressed = False


        if self.world_x < 0:
            self.world_x = 0
            self.rect.x = 0

        if self.world_x > 2000 - self.rect.width:
            self.world_x = 2000 - self.rect.width
            self.rect.x = 2000 - self.rect.width

        self.update_animation()

    def damage_enemy(self, enemy, no_target):
        enemy.health -= 1
        enemy.invincible_enemy = True
        enemy.invincible_time_enemy = time.time()

        if enemy.health == 0:
            enemy.is_death = True

        if enemy.rect.centerx < self.rect.centerx:
            enemy.vel_x = -100
        else:
            enemy.vel_x = 100
        if no_target == True:
            enemy.vel_y = -10
        else:
            pass

        enemy.death_frame = 0
        enemy.death_animation_counter = 0