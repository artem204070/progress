import pygame
from pygame import USEREVENT
import json
from Ball import Ball
from random import randint
import os

pygame.init()

WIDTH = 800
HEIGHT = 600

# Файл для сохранения рекорда
SCORE_FILE = "highscore.json"


def load_highscore():
    """Загружает рекорд из файла"""
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('highscore', 0)
        except:
            return 0
    return 0


def save_highscore(score):
    """Сохраняет рекорд в файл"""
    with open(SCORE_FILE, 'w') as f:
        json.dump({'highscore': score}, f)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Спрайт")

telega = pygame.image.load("image/telega.png")
telega_rect = telega.get_rect(center=(575, HEIGHT - 60))
speed = 20

game_score = 0
high_score = load_highscore()  # Загружаем рекорд при старте

score = pygame.image.load('image/score_fon.png')
font = pygame.font.SysFont('arial', 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

hear_count = 3

back_ground = pygame.image.load('image/back1.jpg')
balls_images = [
    {
        'path': 'image/ball_panda.png',
        'score': 50,
        'type': 'good'
    },
    {
        'path': 'image/ball_bear.png',
        'score': 100,
        'type': 'good'
    },
    {
        'path': 'image/ball_fox.png',
        'score': 75,
        'type': 'good'
    },
    {
        'path': 'image/ball_kitten.png',
        'score': -50,
        'type': 'bad'
    }
]

balls = pygame.sprite.Group()


def create_ball(group):
    index = randint(0, len(balls_images) - 1)
    x = randint(50, WIDTH - 50)
    speed = randint(1, 4)
    ball = Ball(
        x,
        speed,
        balls_images[index]["path"],
        balls_images[index]["score"],
        balls_images[index]["type"],
        group)
    return ball


def collTelegaBall():
    global game_score, hear_count
    for ball in balls:
        if ball.type == 'good':
            if telega_rect.collidepoint(ball.rect.center):
                game_score += ball.score
                ball.kill()
        elif ball.type == 'bad':
            if telega_rect.collidepoint(ball.rect.center):
                game_score += ball.score
                hear_count -= 1
                ball.kill()


clock = pygame.time.Clock()
FPS = 60
pygame.time.set_timer(pygame.USEREVENT, 2000)

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT and not game_over:
            create_ball(balls)
        elif event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:  # Перезапуск игры по нажатию R
                game_over = False
                hear_count = 3
                game_score = 0
                balls.empty()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            telega_rect.x -= speed
            if telega_rect.x < 0:
                telega_rect.x = 0
        elif keys[pygame.K_RIGHT]:
            telega_rect.x += speed
            if telega_rect.x > WIDTH - telega_rect.width:
                telega_rect.x = WIDTH - telega_rect.width

    screen.fill(BLACK)
    screen.blit(back_ground, (0, 0))

    balls.draw(screen)
    if not game_over:
        balls.update(HEIGHT)

    screen.blit(telega, (telega_rect.x, telega_rect.y))
    screen.blit(score, (0, 0))

    # Отображение текущего счета
    score_text = font.render(f"Счет: {game_score}", 1, (255, 255, 0))
    screen.blit(score_text, (20, 10))

    # Отображение рекорда
    highscore_text = font.render(f"Рекорд: {high_score}", 1, (255, 255, 255))
    screen.blit(highscore_text, (20, 50))

    # Отображение жизней
    hear_text = font.render(f"Жизни: {hear_count}", 1, (255, 255, 255))
    screen.blit(hear_text, (20, 90))

    if not game_over:
        collTelegaBall()
        if hear_count <= 0:
            game_over = True
            # Обновляем рекорд если текущий счет больше
            if game_score > high_score:
                high_score = game_score
                save_highscore(high_score)  # Сохраняем новый рекорд

    if game_over:
        # Отображение экрана Game Over
        game_over_text = font.render("GAME OVER! Нажмите R для рестарта", 1, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))

    pygame.display.update()
    clock.tick(FPS)
