import pygame
import sys
import random
import time
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Фруктовая гонка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Шрифты
title_font = pygame.font.SysFont('Arial', 50)
menu_font = pygame.font.SysFont('Arial', 30)
game_font = pygame.font.SysFont('Arial', 40)

# Языки
LANGUAGES = {
    'en': {
        'title': "Fruit Race",
        'play': "Play",
        'settings': "Settings",
        'language': "Language",
        'difficulty': "Select Difficulty",
        'easy': "Easy",
        'medium': "Medium",
        'hard': "Hard",
        'player_score': "Player: {}",
        'bot_score': "Bot: {}",
        'find': "Find: {}",
        'win': "You Win!",
        'lose': "You Lose!",
        'restart': "Press R to restart"
    },
    'ru': {
        'title': "Фруктовая гонка",
        'play': "Играть",
        'settings': "Настройки",
        'language': "Язык",
        'difficulty': "Выберите сложность",
        'easy': "Легко",
        'medium': "Средне",
        'hard': "Сложно",
        'player_score': "Игрок: {}",
        'bot_score': "Бот: {}",
        'find': "Найди: {}",
        'win': "Вы победили!",
        'lose': "Вы проиграли!",
        'restart': "Нажмите R для рестарта"
    }
}

current_lang = 'ru'

# Фрукты
FRUITS = {
    'apple': {'color': RED, 'name': {'en': 'apple', 'ru': 'яблоко'}},
    'banana': {'color': (255, 255, 0), 'name': {'en': 'banana', 'ru': 'банан'}},
    'orange': {'color': (255, 165, 0), 'name': {'en': 'orange', 'ru': 'апельсин'}},
    'grape': {'color': (128, 0, 128), 'name': {'en': 'grape', 'ru': 'виноград'}},
    'pear': {'color': (0, 255, 0), 'name': {'en': 'pear', 'ru': 'груша'}}
}


class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        text_surf = menu_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False


class Fruit:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.radius = 30
        self.color = FRUITS[name]['color']

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius, 2)

    def is_clicked(self, pos):
        distance = ((pos[0] - self.x) ** 2 + (pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.radius


class Game:
    def __init__(self):
        self.state = "menu"  # menu, settings, difficulty, game, result
        self.difficulty = "medium"  # easy, medium, hard
        self.player_score = 0
        self.bot_score = 0
        self.round_time = 0
        self.current_target = None
        self.fruits = []
        self.bot_reaction_time = 1.5  # Базовое время реакции бота
        self.setup_menu()

    def setup_menu(self):
        self.play_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50,
                                  LANGUAGES[current_lang]['play'])
        self.settings_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50,
                                      LANGUAGES[current_lang]['settings'])

    def setup_settings(self):
        self.language_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50,
                                      LANGUAGES[current_lang]['language'])
        self.back_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50,
                                  "Back" if current_lang == 'en' else "Назад")

    def setup_difficulty(self):
        self.easy_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 90, 200, 50,
                                  LANGUAGES[current_lang]['easy'])
        self.medium_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 50,
                                    LANGUAGES[current_lang]['medium'])
        self.hard_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50,
                                  LANGUAGES[current_lang]['hard'])

    def setup_game(self):
        self.player_score = 0
        self.bot_score = 0
        self.generate_fruits()
        self.choose_target()
        self.round_start_time = time.time()

        # Настройка сложности
        if self.difficulty == "easy":
            self.bot_reaction_time = 2.0
        elif self.difficulty == "medium":
            self.bot_reaction_time = 1.5
        else:  # hard
            self.bot_reaction_time = 1.0

    def generate_fruits(self):
        self.fruits = []
        positions = []

        for name in FRUITS:
            while True:
                x = random.randint(50, WIDTH - 50)
                y = random.randint(150, HEIGHT - 50)

                # Проверка на минимальное расстояние между фруктами
                valid_position = True
                for px, py in positions:
                    if ((x - px) ** 2 + (y - py) ** 2) ** 0.5 < 80:
                        valid_position = False
                        break

                if valid_position:
                    positions.append((x, y))
                    self.fruits.append(Fruit(name, x, y))
                    break

    def choose_target(self):
        self.current_target = random.choice(list(FRUITS.keys()))
        self.target_display_time = time.time()

    def bot_turn(self):
        # Бот "ищет" фрукт
        if time.time() - self.target_display_time > self.bot_reaction_time:
            for fruit in self.fruits:
                if fruit.name == self.current_target:
                    self.bot_score += 1
                    self.generate_fruits()
                    self.choose_target()
                    self.round_start_time = time.time()
                    break

    def check_win(self):
        if self.player_score >= 5:
            self.state = "result"
            self.result = "win"
        elif self.bot_score >= 5:
            self.state = "result"
            self.result = "lose"

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu":
                self.play_button.check_hover(mouse_pos)
                self.settings_button.check_hover(mouse_pos)

                if self.play_button.is_clicked(mouse_pos, event):
                    self.state = "difficulty"
                    self.setup_difficulty()
                elif self.settings_button.is_clicked(mouse_pos, event):
                    self.state = "settings"
                    self.setup_settings()

            elif self.state == "settings":
                self.language_button.check_hover(mouse_pos)
                self.back_button.check_hover(mouse_pos)

                if self.language_button.is_clicked(mouse_pos, event):
                    global current_lang
                    current_lang = 'en' if current_lang == 'ru' else 'ru'
                    self.setup_menu()
                    self.setup_settings()
                elif self.back_button.is_clicked(mouse_pos, event):
                    self.state = "menu"
                    self.setup_menu()

            elif self.state == "difficulty":
                self.easy_button.check_hover(mouse_pos)
                self.medium_button.check_hover(mouse_pos)
                self.hard_button.check_hover(mouse_pos)

                if self.easy_button.is_clicked(mouse_pos, event):
                    self.difficulty = "easy"
                    self.state = "game"
                    self.setup_game()
                elif self.medium_button.is_clicked(mouse_pos, event):
                    self.difficulty = "medium"
                    self.state = "game"
                    self.setup_game()
                elif self.hard_button.is_clicked(mouse_pos, event):
                    self.difficulty = "hard"
                    self.state = "game"
                    self.setup_game()

            elif self.state == "game":
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for fruit in self.fruits:
                        if fruit.is_clicked(mouse_pos):
                            if fruit.name == self.current_target:
                                self.player_score += 1
                                self.generate_fruits()
                                self.choose_target()
                                self.round_start_time = time.time()
                                self.check_win()
                            break

            elif self.state == "result":
                if event.type == KEYDOWN and event.key == K_r:
                    self.state = "menu"
                    self.setup_menu()

    def update(self):
        if self.state == "game":
            self.bot_turn()
            self.check_win()

    def draw(self):
        screen.fill(WHITE)

        if self.state == "menu":
            title = title_font.render(LANGUAGES[current_lang]['title'], True, BLACK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

            self.play_button.draw(screen)
            self.settings_button.draw(screen)

        elif self.state == "settings":
            title = title_font.render(LANGUAGES[current_lang]['settings'], True, BLACK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

            self.language_button.draw(screen)
            self.back_button.draw(screen)

        elif self.state == "difficulty":
            title = title_font.render(LANGUAGES[current_lang]['difficulty'], True, BLACK)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

            self.easy_button.draw(screen)
            self.medium_button.draw(screen)
            self.hard_button.draw(screen)

        elif self.state == "game":
            # Отрисовка счета
            player_text = game_font.render(
                LANGUAGES[current_lang]['player_score'].format(self.player_score), True, BLACK)
            bot_text = game_font.render(
                LANGUAGES[current_lang]['bot_score'].format(self.bot_score), True, BLACK)
            screen.blit(player_text, (50, 50))
            screen.blit(bot_text, (WIDTH - 150, 50))

            # Отрисовка цели
            target_text = game_font.render(
                LANGUAGES[current_lang]['find'].format(FRUITS[self.current_target]['name'][current_lang]),
                True, BLACK)
            screen.blit(target_text, (WIDTH // 2 - target_text.get_width() // 2, 50))

            # Отрисовка фруктов
            for fruit in self.fruits:
                fruit.draw(screen)

        elif self.state == "result":
            if self.result == "win":
                result_text = title_font.render(LANGUAGES[current_lang]['win'], True, GREEN)
            else:
                result_text = title_font.render(LANGUAGES[current_lang]['lose'], True, RED)

            screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 - 50))

            restart_text = menu_font.render(LANGUAGES[current_lang]['restart'], True, BLACK)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()


def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)


if __name__ == "__main__":
    main()