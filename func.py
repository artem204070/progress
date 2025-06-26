import random
import pygame

fond = False

def numbers():
    A = int(input("введите число: "))
    if A == 9999:
        fond = True
        pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Нечто')

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    else:
        print(f'ваше число: {A}')

def menu():
    while True:
        print('1. число')
        number = int(input('введите номер: '))

        if number == 1:
            numbers()
            print('введите существующий номер')

menu()