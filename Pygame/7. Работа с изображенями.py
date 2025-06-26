import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Игра с изображенями")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (239, 228, 176)

print(pygame.image.get_extended())

back_surf = pygame.image.load("files/sand.jpg")
back_surf = pygame.transform.scale(back_surf, (back_surf.get_width()//2, back_surf.get_height()//2))
# screen.blit(back_surf, (0, 0))

car_surf = pygame.image.load("files/car.bmp")
car_rect = car_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2))
car_surf.set_colorkey(WHITE)
# car_surf = Pygame.transform.flip(car_surf, False, True)
# car_surf = Pygame.transform.rotate(car_surf, 90)
# screen.blit(car_surf, car_rect)

finish_surf = pygame.image.load("files/finish.png")
# screen.blit(finish_surf, (0, 0))

# Pygame.display.update()

car_up = car_surf
car_down = pygame.transform.flip(car_surf, False, True)
car_left = pygame.transform.rotate(car_surf, 90)
car_right = pygame.transform.rotate(car_surf, -90)

car = car_up
speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    buttons = pygame.key.get_pressed()
    if buttons[pygame.K_LEFT]:
        car = car_left
        car_rect.x -= speed
        if car_rect.x < 0:
            car_rect.x = 0

    elif buttons[pygame.K_RIGHT]:
        car = car_right
        car_rect.x += speed
        if car_rect.x > WIDTH - car_rect.height:
            car_rect.x = WIDTH - car_rect.height

    elif buttons[pygame.K_UP]:
        car = car_up
        car_rect.y -= speed
        if car_rect.y < 0:
            car_rect.y = 0

    elif buttons[pygame.K_DOWN]:
        car = car_down
        car_rect.y += speed
        if car_rect.y > HEIGHT - car_rect.width:
            car_rect.y = HEIGHT - car_rect.width

    screen.blit(back_surf, (0, 0))
    screen.blit(finish_surf, (0, 0))
    screen.blit(car, car_rect)

    pygame.display.update()

    clock.tick(FPS)