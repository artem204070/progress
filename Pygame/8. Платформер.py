import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Платформер")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# характеристики персонажа
# размеры персонажа
player_width = 40
player_height = 60
# начальная позиция
player_x = WIDTH / 4
player_y = HEIGHT - player_height - 10
# скорость перемещения
player_vel_x = 0
player_vel_y = 0
move_speed = 5
jump_power = -15
gravity = 0.8
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# добовляем картинки
background_image = pygame.image.load("files/back.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

player_image = pygame.image.load("files/player.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))

player_left = pygame.transform.flip(player_image, True, False)
player_right = player_image

pass_throught = False # переменная которая разрешаеет проходить сквозь платформу
is_jumping = False

ground = pygame.Rect(0, HEIGHT - 20, WIDTH, 20)

# платформы
platforms = [
    pygame.Rect(300, 400, 200, 10),
    pygame.Rect(100, 300, 200, 10),
    pygame.Rect(400, 200, 200, 10),
    pygame.Rect(150, 100, 200, 10)
]

FPS = 60
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_rect.y += 1
                on_platform = False
                for platform in platforms:
                    if player_rect.colliderect(platform):
                        on_platform = True
                        break
                if player_rect.colliderect(ground):
                    on_platform = True
                player_rect.y -= 1
                if on_platform:
                    player_vel_y = jump_power


            if event.key == pygame.K_DOWN:
                player_rect.y += 1
                on_platform = False
                for platform in platforms:
                    if player_rect.colliderect(platform):
                        on_platform = True
                        break
                player_rect.y -= 1
                if on_platform:
                    pass_throught = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pass_throught = False


    # обрабатываем движение влево и вправо
    keys = pygame.key.get_pressed()
    player_vel_x = 0
    if keys[pygame.K_LEFT]:
        player_image = player_left
        player_vel_x = -move_speed # влево -5
    if keys[pygame.K_RIGHT]:
        player_image = player_right
        player_vel_x = move_speed # вправо 5

    player_vel_y += gravity
    # логика перемещения
    player_x += player_vel_x
    player_y += player_vel_y
    player_rect.x = player_x
    player_rect.y = player_y

    if not pass_throught:
        for platform in platforms:
            if player_rect.colliderect(platform):
                if player_vel_y > 0:
                    player_rect.bottom = platform.top
                    player_y = player_rect.y
                    player_vel_y = 0

    if player_rect.colliderect(ground):
        player_rect.bottom = ground.top
        player_y = player_rect.y
        player_vel_y = 0


    # ограничение движения влево и вправо
    if player_x <= 0:
        player_x = 0
        player_rect.x = player_x
    if player_x >= WIDTH - player_width:
        player_x = WIDTH - player_width
        player_rect.x = player_x

    screen.blit(background_image, (0, 0))
    screen.blit(player_image, (player_rect.x, player_rect.y))

    for platform in platforms:
        pygame.draw.rect(screen, (56, 23, 33), platform)
    pygame.draw.rect(screen, (0, 255, 0), ground)
    pygame.display.update()

    clock.tick(FPS)