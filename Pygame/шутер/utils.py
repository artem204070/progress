import pygame
from consts import *


def draw_crosshair(screen, mouse_pos):
    pygame.draw.line(screen, CROSSHAIR_COLOR, (mouse_pos[0] - CROSSHAIR_LINE_LENGTH - CROSSHAIR_GAP, mouse_pos[1]),
                     (mouse_pos[0] - CROSSHAIR_GAP, mouse_pos[1]), 2)
    pygame.draw.line(screen, CROSSHAIR_COLOR, (mouse_pos[0] + CROSSHAIR_GAP, mouse_pos[1]),
                     (mouse_pos[0] + CROSSHAIR_LINE_LENGTH + CROSSHAIR_GAP, mouse_pos[1]), 2)
    pygame.draw.line(screen, CROSSHAIR_COLOR, (mouse_pos[0], mouse_pos[1] - CROSSHAIR_LINE_LENGTH - CROSSHAIR_GAP),
                     (mouse_pos[0], mouse_pos[1] - CROSSHAIR_GAP), 2)
    pygame.draw.line(screen, CROSSHAIR_COLOR, (mouse_pos[0], mouse_pos[1] + CROSSHAIR_GAP),
                     (mouse_pos[0], mouse_pos[1] + CROSSHAIR_LINE_LENGTH + CROSSHAIR_GAP), 2)
def save_haigt_score(save2):
    try:
        with open('save.txt', 'w') as file:
            file.write(str(save2))
    except FileNotFoundError:
        print('создаем фаил потому что ты не создал!')

def load():
    try:
        with open("save.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return  0