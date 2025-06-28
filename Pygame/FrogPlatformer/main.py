import pygame
from consts import *
from Pygame.FrogPlatformer.Objeckt.platform import Platform
from Pygame.FrogPlatformer.Objeckt.player import Player
from  Pygame.FrogPlatformer.Module.Camera import Camera
from  Pygame.FrogPlatformer.Objeckt.background import Background
from  Pygame.FrogPlatformer.Objeckt.kiwi import Kiwi
from Pygame.FrogPlatformer.Objeckt.enemy import Enemy
import pytmx
from Pygame.FrogPlatformer.Levels.levels import *
from Pygame.FrogPlatformer.Objeckt.Boss import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Русский Лягушатник")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
kiwi_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

camera = Camera(2000)

font = pygame.font.SysFont('Arial', 30)
stone_group = pygame.sprite.Group()
tmx_data = pytmx.load_pygame('Assest/Levels/BasicLevel.tmx')
background_layer = tmx_data.get_layer_by_name("Background")
background_surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight))

for x, y, gid in background_layer:
    title = tmx_data.get_tile_image_by_gid(gid)
    if title:
        background_surface.blit(title, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

kiwi_score = 0

def load_level(level_data):
    all_sprites.empty()
    platform_group.empty()
    kiwi_group.empty()
    enemy_group.empty()

    for args in level_data["platforms"]:
        platform = Platform(*args)
        platform_group.add(platform)
        all_sprites.add(platform)
    for args in level_data["kiwis"]:
        kiwi = Kiwi(*args)
        kiwi_group.add(kiwi)
        all_sprites.add(kiwi)
    for args in level_data["enemies"]:
        enemy = Enemy(*args, platform_group)
        enemy_group.add(enemy)
        all_sprites.add(enemy)



    player = Player(*level_data["player_start"], platform_group)
    all_sprites.add(player)

    return player



current_levels = 0
player = load_level(levels[current_levels])

boss = Boss(0, 0, 25, 7, platform_group, stone_group, player)

running = True
playing = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for enemy in enemy_group:
                    if pygame.sprite.collide_rect(player, enemy):
                        player.damage_enemy(enemy)

    if player.health == 0:
        playing = False

    if all(kiwi.collected for kiwi in kiwi_group):
        current_levels += 1
        if current_levels < len(levels):
            player = load_level(levels[current_levels])
            kiwi_score = 0
        else:
            running = False


    if playing:
        all_sprites.update()
        stone_group.update()

        if camera.check(player, WIDTH, HEIGHT):
            for sprite in all_sprites:
                camera.move(sprite)

        for kiwi in kiwi_group:
            if pygame.sprite.collide_rect(player, kiwi) and kiwi.collected == False:
                kiwi.collected = True
                kiwi_score += 1

        for enemy in enemy_group:
            if pygame.sprite.collide_rect(player, enemy):
                enemy.damage_player(player)

        screen.fill(WHITE)
        screen.blit(background_surface, (0, 0))
        all_sprites.draw(screen)

        score_text = font.render(f'Киви: {kiwi_score}', True, BLACK)
        screen.blit(score_text, (20, 20))

        health_text = font.render(f'Здоровье: {player.health}', True, BLACK)
        screen.blit(health_text, (20, 80))

    else:
        screen.fill(BLACK)
        death_text = font.render(f'Вы умерли но собрали: {kiwi_score} киви!', True, RED)
        screen.blit(death_text, (250, 300))


    pygame.display.update()
    clock.tick(FPS)