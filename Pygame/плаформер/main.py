import pygame
import random
from const import *
from  player import Player
from coin import Coin
from hazard import *
from move_pplatform import MovingPlatform
pygame.init()

font = pygame.font.SysFont('constantia', 30)
# print(Pygame.font.get_fonts())

screen = pygame.display.set_mode((WITDH, HEIGHT))
pygame.display.set_caption("Платформер")

ground = pygame.Rect(0, HEIGHT - 20, WITDH, 20)
ball_group = pygame.sprite.Group()
MovingPlatform_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
platforms = [
    pygame.Rect(300, 450, 200, 10),
    pygame.Rect(75, 370, 200, 10),
    pygame.Rect(400, 280, 200, 10),
    pygame.Rect(65, 180, 200, 10)
]

MovingPlatform(150, 150, 100, 20, 150, 350, 'x', MovingPlatform_group)
MovingPlatform(150, 150, 100, 15, 150, 350, 'y', MovingPlatform_group)

all_platforms = platforms + [ground] + [mp.rect for mp in MovingPlatform_group]# набор всех платформ
all_platforms_from_coin_spawn = platforms + [ground] + list(MovingPlatform_group)

current_hazard_min_speed = INITIAL_HAZARD_MIN_SPEED
current_hazard_max_speed = INITIAL_HAZARD_MAX_SPEED
current_hazard_spawn_interval = INITIAL_HAZARD_SPAWN_INTERVAL
last_difficulty_score_threshold = 0
high_score = 0

def spawn_coin():
    if len(coins_group) >= MAX_COIN:
        return

    choice_platform = random.choice(all_platforms_from_coin_spawn)

    attachet_platform = None
    if isinstance(choice_platform, pygame.Rect):
        choice_platform_rect = choice_platform
    else:
        choice_platform_rect = choice_platform.rect
        attachet_platform = choice_platform

    min_x = choice_platform_rect.left + COIN_RADIUS
    max_x = choice_platform_rect.right - COIN_RADIUS

    if min_x > max_x:
        coin_x = choice_platform_rect.centerx
    else:
        coin_x = random.randint(min_x, max_x)
    coin_y = choice_platform_rect.top - COIN_RADIUS

    Coin(coin_x, coin_y, coins_group, attachet_platform)

def create_bolls():
    x = random.randint(50, WITDH - 50)
    speed = random.randint(HAZARD_MIN_SPEED, HAZARD_MAX_SPEED)
    balls = Hazard(x, speed, ball_group)

def reset_game():
    global score, lives, playing, player, coins_group, ball_group
    score = 0
    lives = 3
    playing = True
    player = Player(WITDH / 4, HEIGHT - PLAYER_HEIGHT - 20)
    coins_group.empty()
    ball_group.empty()

    MovingPlatform(150, 150, 100, 20, 150, 350, 'x', MovingPlatform_group)
    MovingPlatform(150, 150, 100, 15, 150, 350, 'y', MovingPlatform_group)
    all_platforms = platforms + [ground] + [mp.rect for mp in MovingPlatform_group]  # набор всех платформ
    all_platforms_from_coin_spawn = platforms + [ground] + list(MovingPlatform_group)

    current_hazard_min_speed = INITIAL_HAZARD_MIN_SPEED
    current_hazard_max_speed = INITIAL_HAZARD_MAX_SPEED
    current_hazard_spawn_interval = 2000
    last_difficulty_score_threshold = 0

def save(hight_save):
    try:
        with open('high_score.txt', 'w') as file:
            file.write(str(hight_save))
    except FileNotFoundError:
        print('создаем фаил потому что ты не создал!')

def update_difficulty():
    global last_difficulty_score_threshold, current_hazard_max_speed, current_hazard_min_speed, current_hazard_spawn_interval

    if score >= last_difficulty_score_threshold + DIFFICULTY_SCORE_STEP:
        last_difficulty_score_threshold = DIFFICULTY_SCORE_STEP

        current_hazard_min_speed += min(current_hazard_min_speed + HAZARD_SPEED_INCREMENT, MAX_HAZARD_SPEED_LIMIT)
        current_hazard_max_speed += min(current_hazard_min_speed + HAZARD_SPEED_INCREMENT, MAX_HAZARD_SPEED_LIMIT)

        current_hazard_spawn_interval -= HAZARD_SPAWN_DECREMENT

        pygame.time.set_timer(pygame.USEREVENT, current_hazard_spawn_interval)
        print('скорость увеличилась')

def load():
    global high_score
    try:
        with open("high_score.txt", "r") as r:
            score_file = r.read()
            high_score = int(score_file)
        print(high_score)
    except Exception as e:
        print(f"ошибка при загрузке: {e}")
        high_score = 0

player = Player(WITDH / 4, HEIGHT - PLAYER_HEIGHT - 20) # обьект игрока

score = 0 # количество очков
lives = 3 # жизни

clock = pygame.time.Clock()
playing = True # флаг для запуска или экрана game over
running = True # флаг для игрового цикла
pygame.time.set_timer(pygame.USEREVENT, current_hazard_spawn_interval)
pygame.time.set_timer(COIN_EVENT, COIN_SPAWN_TIME)

load()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if playing:
                if event.key == pygame.K_SPACE:
                    player.jump(all_platforms)
            else:
                if event.key == pygame.K_r:
                   reset_game()


        elif event.type == pygame.USEREVENT and playing:
            create_bolls()

        elif event.type == COIN_EVENT:
            spawn_coin()

    if playing:
        player.update(all_platforms)
        coins_group.update()
        ball_group.update()
        MovingPlatform_group.update()

        update_difficulty()

        if not player.is_hit:
            hit_list = pygame.sprite.spritecollide(player, ball_group, True)
            if hit_list:
                lives -= 1
                player.is_hit = True
                player.hit_timer = player.hit_duration

        if lives <= 0:
            playing = False
            if score > high_score:
                high_score = score
                save(high_score)

        screen.fill(BLACK)
        for platform in platforms:
            pygame.draw.rect(screen, BROWN, platform)

        for movingPlatform in MovingPlatform_group:
            movingPlatform.draw(screen)

        pygame.draw.rect(screen, (0, 255, 0), ground)
        score_text = font.render(f'Монеты: {str(score)}', 1, YELLOW)
        lives_text = font.render(f'Жизни: {str(lives)}', 1, YELLOW)
        screen.blit(score_text, (20, 10))
        screen.blit(lives_text, (20, 70))

        player.draw(screen)
        for coin in coins_group:
            coin.draw(screen)

        for ball in ball_group:
            ball.draw(screen)

        collected_coin = pygame.sprite.spritecollide(player, coins_group, True)
        score += len(collected_coin)

    else:
        score_dead_text = font.render(f'Вы собрали: {str(score)} монет', 1, WHITE)
        dead_text = font.render('Вы умерли', 1, WHITE)
        restart_text = font.render('Нажмите r для перезапуска', 1, WHITE)
        max_score = font.render(f'Ваш рекорд {high_score}!', 1, WHITE)
        screen.blit(dead_text, (300, 300))
        screen.blit(score_dead_text, (300, 250))
        screen.blit(restart_text, (300, 350))
        screen.blit(max_score, (300, 400))

    pygame.display.update()
    clock.tick(FPS)