import pygame
from pygame import USEREVENT
from Ball import Ball
from random import randint
pygame.init()

WIDTH = 800
HEIGHT = 600



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Спрайт")


telega = pygame.image.load("image/telega.png")
telega_rect = telega.get_rect(center=(575, HEIGHT - 60))
speed = 20

game_score = 0

score = pygame.image.load('image/score_fon.png')
font = pygame.font.SysFont('arial', 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

hear_count = 1

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
    },
    {
        'path': 'image/ball_tiger.png',
        'score': -30,
        'type': 'bad'
    }

]


balls = pygame.sprite.Group() # группа спрайтов

high_score = 0
def create_ball(group):
    index = randint(0, len(balls_images) - 1) # от 0 до 3
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
    global game_score, hear_count, max_result
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

def load_score():
    global high_score
    try:
        with open("Score.txt", "r") as r:
            score_file = r.read()
            if score:
                high_score = int(score_file)
            else:
                high_score = 0
    except Exception as e:
        print(f"ошибка при загрузке: {e}")
        high_score = 0
def create(score):
    try:
        with open('Score.txt', 'w') as f:
            f.write(str(score))
    except Exception as e:
        print(f'ошибка с сохранением: {e}')



clock = pygame.time.Clock()
FPS = 60
pygame.time.set_timer(pygame.USEREVENT, 2000) # событие создания меча каждые 2 сек

load_score()
playing = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT: # событие которое мы зоздем сами
            create_ball(balls)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and playing == False:
                playing = True
                hear_count = 3
                game_score = 0

        elif playing == False:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False



    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        telega_rect.x -= speed
        if telega_rect.x < 0:
            telega_rect.x = 0
    elif keys[pygame.K_RIGHT]:
        telega_rect.x += speed
        if telega_rect.x > WIDTH - telega_rect.width:
            telega_rect.x = WIDTH - telega_rect.width

    if hear_count == 0:
        if game_score > high_score:
            create(game_score)
        playing = False

    # отрисовка персонажа
    screen.fill(BLACK)
    screen.blit(back_ground, (0, 0))

    if playing:
        balls.draw(screen)
        balls.update(HEIGHT)

        screen.blit(telega, (telega_rect.x, telega_rect.y))
        screen.blit(score, (0, 0))

        score_text = font.render(str(game_score), 1, (255, 255, 0))
        screen.blit(score_text, (20, 10))

        hear_text = font.render(f"жизни: {hear_count}", 1, (0, 0, 0))
        screen.blit(hear_text, (20, 80))

        mas_score = font.render(f'Рекорд: {high_score}', 1, (0, 0, 0))
        screen.blit(mas_score, (2, 150))


    else:

        final_text = font.render("Игра завершена", 1, RED)
        high_text = font.render(f"Наилутший результат: {high_score}", 1, (0, 0, 0))
        score_text = font.render(f"Текущий результат: {game_score}", 1, (0, 0, 0))
        text1 = font.render(f'Нажмите R для перезапуска', 1, (0, 0, 0))
        screen.blit(text1, (200, 500))
        screen.blit(final_text, (200, 200))
        screen.blit(high_text, (200, 300))
        screen.blit(score_text, (200, 400))

    pygame.display.update()

    clock.tick(FPS)
    collTelegaBall()




    # логика падения
    #if ball1.rect.y < HEIGHT - 20:
       # ball1.rect.y += speed
#else:
        #ball1.rect.y = 0