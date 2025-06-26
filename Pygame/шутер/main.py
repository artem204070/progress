import pygame
from utils import *
from consts import *
from circle import Circle
from exsplosion import *
from gift import Gift
import random

pygame.init()
pygame.mixer.init()

shot_sound = pygame.mixer.Sound('./Sound/shot.wav') # загрузка звука
font = pygame.font.SysFont('constantia', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)

clock = pygame.time.Clock()

circles = pygame.sprite.Group()
exsplosion = pygame.sprite.Group()

pygame.time.set_timer(pygame.USEREVENT, CIRCLE_SPAWN_INTERVAL)


score = 0
ammo = 5
max_ammo = 10
reload_delay = 500
last_shot_time = 0
save_score = load()

pygame.mouse.set_visible(False)
playning = True
running = True



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > save_score:
                save_haigt_score(score)
            running = False
        elif event.type == pygame.USEREVENT:
            if playning:
                if len(circles) < MAX_CIRCLES:
                    circle = Circle()
                    gift = Gift()
                    circles.add(circle)
                    A = random.randint(1, 3)
                    if A == 2:
                        circles.add(gift)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playning:
                if event.button == 1:
                    now_time = pygame.time.get_ticks() # получаем настоящие время

                    if now_time - last_shot_time >= reload_delay and ammo > 0:
                        last_shot_time = now_time
                        mouse = pygame.mouse.get_pos()

                        hit = False

                    for circle in circles:
                        if circle.rect.collidepoint(mouse):
                            score += 1
                            explosion = Explosion(circle.rect.center, circle.color)
                            exsplosion.add(explosion)
                            shot_sound.play()
                            circle.kill()
                            hit = True
                            if ammo < max_ammo:
                                ammo += 1
                            break
                        if gift.rect.collidepoint(mouse):
                            score += 1
                            explosion = Explosion(circle.rect.center, circle.color)
                            exsplosion.add(explosion)
                            shot_sound.play()
                            gift.kill()
                            hit = True
                            if ammo < max_ammo:
                                ammo += 3
                            break

                    if not hit:
                        ammo -= 1

    mouse_pos = pygame.mouse.get_pos()

    if ammo == 0:
        playning = False

    if playning:
        screen.fill(BLACK)
        circles.update()
        exsplosion.update()
        circles.draw(screen)
        exsplosion.draw(screen)

        score_text = font.render(f'Вы уничтожили: {str(score)} шаров', 4, RED)
        screen.blit(score_text, (0, 0))

        ammo_text = font.render(f'Пули {ammo}/{max_ammo}', True, RED)
        screen.blit(ammo_text, (0, 40))

        save_text = font.render(f'Наилучший результат: {str(save_score)}', 4, RED)
        screen.blit(save_text, (0, 80))
    else:
        text = font.render("Игра окончена!", 4, RED)
        screen.blit(text, (400, 300))

        save_text1 = font.render(f'Наилучший результат: {str(save_score)}', 4, RED)
        screen.blit(save_text1, (400, 380))


    draw_crosshair(screen, mouse_pos)
    pygame.display.update()

    screen.fill(BLACK)

    clock.tick(FPS)
