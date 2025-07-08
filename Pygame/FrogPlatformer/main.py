import pygame
from consts import *
from Pygame.FrogPlatformer.Objeckt.platform import *
from Pygame.FrogPlatformer.Objeckt.player import Player
from Pygame.FrogPlatformer.Module.Camera import Camera
from Pygame.FrogPlatformer.Objeckt.background import Background
from Pygame.FrogPlatformer.Objeckt.kiwi import Kiwi
from Pygame.FrogPlatformer.Objeckt.enemy import Enemy
import pytmx
from Pygame.FrogPlatformer.Levels.levels import *
from Pygame.FrogPlatformer.Objeckt.Boss import *
from Pygame.FrogPlatformer.Objeckt.FlyingEnemy import *
import json
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Русский Лягушатник")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
kiwi_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
flying_enemies = pygame.sprite.Group()


backgrounds = []
current_background = None

camera = Camera(2000)

font = pygame.font.SysFont('Arial', 30)
tmx_data = pytmx.load_pygame('Assest/Levels/BasicLevel.tmx')
# background_layer = tmx_data.get_layer_by_name("Background")
# background_surface = pygame.Surface((tmx_data.width * tmx_data.tilewidth, tmx_data.height * tmx_data.tileheight))
#
# for x, y, gid in background_layer:
#     title = tmx_data.get_tile_image_by_gid(gid)
#     if title:
#         background_surface.blit(title, (x * tmx_data.tilewidth, y * tmx_data.tileheight))
play_image = pygame.image.load("Assest/UI/play.png")
play_image = pygame.transform.scale(play_image, (100, 100))
play_rect = play_image.get_rect(center=(WIDTH // 2, 475))

kiwi_score = 0
max_kiwi_score = 0

sound_damage = pygame.mixer.Sound("sound/damage.mp3")
sound_damage.set_volume(0.2)

def save_max_score(filename='progress.txt'):
    # try:
    #     with open("score.txt", "w") as file:
    #         file.write(str(max_score))
    # except FileNotFoundError:
    #     print('создаем фаил')
    if player.health <= 0:
        data = {
            "current_level": current_levels,
            "player_health": 100,
            "kiwi_score": 0,
        }
    else:
        data = {
            "current_level": current_levels,
            # "player_x": player.world_x,
            # "player_y": player.rect.y,
            "player_health": player.health,
            "kiwi_score": kiwi_score,
        }
    with open(filename, "w") as file:
        json.dump(data, file)

def load_max_score(filename='progress.txt'):
    global current_levels, kiwi_score, player
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        current_levels = data["current_level"]
        player = load_level(levels[current_levels])
        # player.world_x = data["player_x"]
        # player.rect.y = data["player_y"]
        player.health = data["player_health"]
        kiwi_score = data["kiwi_score"]
    except Exception as e:
        print(e)
    # try:
    #     with open("score.txt", "r") as file:
    #         score = file.read()
    #         max_kiwi_score = int(score)
    # except Exception as e:
    #     print(e)


def load_level(level_data):
    global current_background
    all_sprites.empty()
    platform_group.empty()
    kiwi_group.empty()
    enemy_group.empty()
    stone_group.empty()

    bg_image = pygame.image.load(level_data["background"]).convert_alpha()
    current_background = Background(0, 0, WIDTH, HEIGHT, bg_image)


    player = Player(*level_data["player_start"], platform_group)
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
    for args in level_data["fly_enemy"]:
        flying_enemy = FlyingEnemy(*args, platform_group, stone_group, player)
        enemy_group.add(flying_enemy)
        all_sprites.add(flying_enemy)
    for args in level_data["boss"]:
        boss = Boss(*args, platform_group, stone_group, player)
        all_sprites.add(boss)
        enemy_group.add(boss)
    for args in level_data["Move_platform"]:
        move_platform = MovePlatform(*args)
        all_sprites.add(move_platform)
        platform_group.add(move_platform)


    all_sprites.add(player)

    return player


def restart_game():
    global playing
    playing = True
    save_max_score()
    load_max_score()

def is_near(sprite1, sprite2, distance):
    dx = sprite1.rect.centerx - sprite2.rect.centerx
    dy = sprite1.rect.centery - sprite2.rect.centery
    return (dx**2 + dy**2) ** 0.5 < distance

current_levels = 0
player = load_level(levels[current_levels])

running = True
playing = False
boss_encountered = False
main = True

load_max_score()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_max_score()
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                for enemy in enemy_group:
                    if is_near(player, enemy, 100):
                        sound_damage.play()
                        player.damage_enemy(enemy, True)
                for fly_enemy in flying_enemies:
                    if is_near(player, fly_enemy, 100):
                        sound_damage.play()
                        player.damage_enemy(fly_enemy, False)
        if playing == False and event.type == pygame.MOUSEBUTTONDOWN:
            if play_rect.collidepoint(event.pos):
                restart_game()

    if player.health == 0:
        playing = False
        main = False

    if all(kiwi.collected for kiwi in kiwi_group):
        current_levels += 1
        if current_levels < len(levels):
            player = load_level(levels[current_levels])
            kiwi_score = 0
        else:
            save_max_score()
            running = False

    if playing:
        all_sprites.update()
        stone_group.update()

        for kiwi in kiwi_group:
            if pygame.sprite.collide_rect(player, kiwi) and kiwi.collected == False:
                kiwi.collected = True
                kiwi_score += 1

        for enemy in enemy_group:
            if pygame.sprite.collide_rect(player, enemy):
                enemy.damage_player(player)

        for flying_enemy in flying_enemies:
            if pygame.sprite.collide_rect(player, flying_enemy):
                flying_enemy.damage_player(player)

        for stone in stone_group:
            if pygame.sprite.collide_rect(player, stone):
                if not player.invincible:
                    player.health -= stone.damage
                    stone.kill()
                    player.invincible = True

        for enemy in enemy_group:
            if isinstance(enemy, Boss) and is_near(player, enemy, 400):
                boss_encountered = True
                current_boss = enemy
                break


        offset_x, offset_y = camera.get_offset(player, WIDTH)

        screen.fill(WHITE)
        current_background.draw(screen)

        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - offset_x, sprite.rect.y - offset_y))
        for stone in stone_group:
            screen.blit(stone.image, (stone.rect.x - offset_x, stone.rect.y - offset_y))


        score_text = font.render(f'Киви: {kiwi_score}', True, BLACK)
        screen.blit(score_text, (20, 20))

        health_text = font.render(f'Здоровье: {player.health}', True, BLACK)
        screen.blit(health_text, (20, 80))

        if boss_encountered:
            boss_name_text = font.render(f"{current_boss.name}", True, RED)
            screen.blit(boss_name_text, (0, 300))

            boss_health_text = font.render(f"Здоровье {current_boss.health}", True, RED)
            screen.blit(boss_health_text, (80, 300))

    elif not playing and not main:
        screen.fill(BLACK)
        death_text = font.render(f'Вы умерли но собрали: {kiwi_score} киви!', True, RED)
        screen.blit(death_text, (250, 300))

        max_score_text = font.render(f'Ваш рекорд: {max_kiwi_score} киви!', True, BLUE)
        screen.blit(max_score_text, (250, 350))

        screen.blit(play_image, play_rect)

    elif not playing and main:
        hello_text = font.render(f'Привет', True, BLUE)
        screen.blit(hello_text, (250, 350))

        screen.blit(play_image, play_rect)

    pygame.display.update()
    clock.tick(FPS)