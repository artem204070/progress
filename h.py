from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from math import degrees, atan2
import socket
import threading
import json
import pickle

app = Ursina()

# ========== НАСТРОЙКИ СЕРВЕРА ==========
SERVER = False  # Поставьте True для запуска сервера
HOST = 'localhost'
PORT = 5555

if SERVER:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

# ========== НАСТРОЙКИ МИРА ==========
GROUND_SIZE = 200
TREE_COUNT = 50
STONE_COUNT = 30
ANIMAL_COUNT = 15
BUILDING_PIECES = ['wall', 'foundation', 'doorway']
RESOURCES = ['wood', 'stone', 'metal', 'cloth', 'food', 'water']

# ========== СИСТЕМА ДНЯ И НОЧИ ==========
DAY_LENGTH = 120
current_time = 0
is_day = True
fog_density = 0


# ========== КЛАСС ЖИВОТНЫХ ==========
class Animal(Entity):
    def __init__(self, position=(0, 0, 0), animal_type='deer'):
        super().__init__(
            model=animal_type,
            position=position,
            collider='box',
            scale=(1, 1, 1),
            texture='white_cube'
        )

        self.animal_type = animal_type
        self.health = 100
        self.speed = 2 if animal_type == 'deer' else 3
        self.direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        self.last_direction_change = time.time()
        self.state = 'wandering'

        if animal_type == 'deer':
            self.color = color.orange
            self.scale = (1.5, 1.5, 1.5)
        elif animal_type == 'wolf':
            self.color = color.gray
            self.scale = (1.2, 1.2, 1.5)
            self.damage = 10

    def update(self):
        if self.state == 'wandering':
            if time.time() - self.last_direction_change > 5:
                self.direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
                self.last_direction_change = time.time()

            if distance(self.position, player.position) < 10:
                self.state = 'fleeing'
                self.direction = (self.position - player.position).normalized()

        elif self.state == 'fleeing':
            if distance(self.position, player.position) > 20:
                self.state = 'wandering'

        if self.animal_type == 'wolf' and distance(self.position, player.position) < 3:
            self.state = 'attacking'
            self.direction = (player.position - self.position).normalized()
            if time.time() % 1 < 0.1:
                player.health -= self.damage

        self.position += self.direction * self.speed * time.dt
        self.rotation_y = degrees(atan2(-self.direction.x, -self.direction.z))

        if abs(self.x) > GROUND_SIZE / 2 or abs(self.z) > GROUND_SIZE / 2:
            self.direction = Vec3(-self.direction.x, 0, -self.direction.z)


# ========== КЛАСС РЕСУРСОВ ==========
class Resource(Entity):
    def __init__(self, position=(0, 0, 0), resource_type='tree'):
        y_pos = 0
        scale = (1, 1, 1)

        if resource_type == 'tree':
            y_pos = 1
            scale = (0.8, 2, 0.8)
        elif resource_type == 'stone':
            scale = (1.5, 0.7, 1.5)

        super().__init__(
            position=position + (0, y_pos, 0),
            model='cube',
            collider='box',
            scale=scale,
            texture='white_cube'
        )

        self.resource_type = resource_type
        self.health = 100
        self.respawn_time = 300 if resource_type == 'tree' else 600
        self.max_health = 100

        if resource_type == 'tree':
            self.color = color.brown
            Entity(
                parent=self,
                model='sphere',
                color=color.green,
                scale=(2, 1.5, 2),
                y=1.5
            )
        elif resource_type == 'stone':
            self.color = color.gray


# ========== КЛАСС ОРУЖИЯ ==========
class Weapon(Entity):
    def __init__(self, weapon_type='spear'):
        super().__init__(
            parent=camera,
            model='cube',
            position=(0.5, -0.5, 1),
            scale=(0.1, 0.1, 0.3),
            color=color.gray,
            texture='white_cube'
        )

        self.weapon_type = weapon_type
        self.damage = 25 if weapon_type == 'spear' else 50
        self.range = 2 if weapon_type == 'spear' else 4
        self.cooldown = 0.5
        self.last_attack = 0

        if weapon_type == 'spear':
            self.model = 'cube'
            self.scale = (0.1, 0.1, 0.5)
            self.color = color.brown
        elif weapon_type == 'bow':
            self.model = 'cube'
            self.scale = (0.2, 0.1, 0.1)
            self.color = color.brown

    def attack(self):
        if time.time() - self.last_attack < self.cooldown:
            return False

        self.last_attack = time.time()
        self.position = (0.5, -0.5, 0.8)
        invoke(setattr, self, 'position', (0.5, -0.5, 1), delay=0.1)

        if mouse.hovered_entity:
            if isinstance(mouse.hovered_entity, Animal):
                mouse.hovered_entity.health -= self.damage
                return True
            elif isinstance(mouse.hovered_entity, Resource):
                mouse.hovered_entity.health -= self.damage
                return True

        return False


# ========== КЛАСС СТРОИТЕЛЬНЫХ ЭЛЕМЕНТОВ ==========
class BuildingPiece(Entity):
    def __init__(self, position=(0, 0, 0), piece_type='wall', material='wood'):
        super().__init__(
            model=piece_type,
            position=position,
            collider='box',
            scale=1,
            texture='white_cube'
        )

        self.piece_type = piece_type
        self.material = material
        self.health = {
            'wood': 100,
            'stone': 200,
            'metal': 300
        }.get(material, 100)

        if material == 'wood':
            self.color = color.brown
        elif material == 'stone':
            self.color = color.gray
        elif material == 'metal':
            self.color = color.white


# ========== СЕТЕВОЙ КЛАСС ==========
class NetworkPlayer(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            model='cube',
            position=position,
            scale=(1, 2, 1),
            color=color.blue,
            collider='box'
        )
        self.username = "Player"
        self.health = 100
        self.last_update = time.time()


# ========== ИНИЦИАЛИЗАЦИЯ МИРА ==========
def generate_world():
    ground = Entity(
        model='plane',
        scale=(GROUND_SIZE, 1, GROUND_SIZE),
        texture='grass',
        texture_scale=(GROUND_SIZE / 10, GROUND_SIZE / 10),
        collider='box'
    )

    resources = []
    for _ in range(TREE_COUNT):
        x = random.uniform(-GROUND_SIZE / 2 + 10, GROUND_SIZE / 2 - 10)
        z = random.uniform(-GROUND_SIZE / 2 + 10, GROUND_SIZE / 2 - 10)
        resources.append(Resource(position=(x, 0, z), resource_type='tree'))

    for _ in range(STONE_COUNT):
        x = random.uniform(-GROUND_SIZE / 2 + 10, GROUND_SIZE / 2 - 10)
        z = random.uniform(-GROUND_SIZE / 2 + 10, GROUND_SIZE / 2 - 10)
        resources.append(Resource(position=(x, 0, z), resource_type='stone'))

    animals = []
    for _ in range(ANIMAL_COUNT):
        x = random.uniform(-GROUND_SIZE / 2 + 20, GROUND_SIZE / 2 - 20)
        z = random.uniform(-GROUND_SIZE / 2 + 20, GROUND_SIZE / 2 - 20)
        animal_type = random.choice(['deer', 'wolf'])
        animals.append(Animal(position=(x, 0, z), animal_type=animal_type))

    return ground, resources, animals


ground, resources, animals = generate_world()
building_pieces = []
network_players = {}


# ========== ИГРОК ==========
class RustPlayer(FirstPersonController):
    def __init__(self):
        super().__init__(
            model='cube',
            speed=5,
            jump_height=1,
            collider='box'
        )

        self.cursor.visible = False
        self.health = 100
        self.max_health = 100
        self.hunger = 100
        self.thirst = 100
        self.inventory = {res: 0 for res in RESOURCES}
        self.equipped_weapon = None
        self.equipped_building = None
        self.building_mode = False
        self.building_material = 'wood'

        # Стартовые ресурсы
        self.inventory['wood'] = 50
        self.inventory['stone'] = 20
        self.equip_weapon('spear')

        # Сетевая часть
        self.client_socket = None
        self.username = "Player1"
        self.connect_to_server()

    def connect_to_server(self):
        if SERVER: return

        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((HOST, PORT))
            threading.Thread(target=self.receive_data, daemon=True).start()
            print("Подключено к серверу")
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def receive_data(self):
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data: break

                data = pickle.loads(data)
                self.handle_network_data(data)
            except:
                break

    def handle_network_data(self, data):
        if data['type'] == 'player_update':
            if data['username'] != self.username:
                if data['username'] not in network_players:
                    network_players[data['username']] = NetworkPlayer()

                network_players[data['username']].position = data['position']
                network_players[data['username']].health = data['health']

    def send_data(self, data):
        if self.client_socket:
            try:
                self.client_socket.send(pickle.dumps(data))
            except:
                print("Ошибка отправки данных")

    def equip_weapon(self, weapon_type):
        if self.equipped_weapon:
            destroy(self.equipped_weapon)

        self.equipped_weapon = Weapon(weapon_type)
        self.building_mode = False

    def toggle_building_mode(self):
        self.building_mode = not self.building_mode
        if self.building_mode and self.equipped_weapon:
            self.equipped_weapon.enabled = False
        elif not self.building_mode and self.equipped_weapon:
            self.equipped_weapon.enabled = True

    def update(self):
        super().update()

        # Отправка данных на сервер
        if self.client_socket and time.time() - getattr(self, 'last_network_update', 0) > 0.1:
            self.send_data({
                'type': 'player_update',
                'username': self.username,
                'position': self.position,
                'health': self.health
            })
            self.last_network_update = time.time()


player = RustPlayer()

# ========== СИСТЕМА КРАФТА ==========
crafting_recipes = {
    'spear': {'wood': 50, 'stone': 20},
    'bow': {'wood': 100, 'cloth': 10},
    'arrow': {'wood': 10, 'stone': 5},
    'wood_wall': {'wood': 100},
    'stone_wall': {'wood': 50, 'stone': 100},
    'metal_wall': {'wood': 50, 'stone': 50, 'metal': 100},
    'campfire': {'wood': 200},
    'small_box': {'wood': 150}
}


# ========== UI ИНТЕРФЕЙС ==========
class GameUI:
    def __init__(self):
        # Основные показатели
        self.health_bar = Entity(
            model='quad',
            scale=(0.2, 0.03),
            position=(-0.85, 0.45),
            color=color.red,
            parent=camera.ui
        )

        self.hunger_bar = Entity(
            model='quad',
            scale=(0.2, 0.03),
            position=(-0.85, 0.40),
            color=color.orange,
            parent=camera.ui
        )

        self.thirst_bar = Entity(
            model='quad',
            scale=(0.2, 0.03),
            position=(-0.85, 0.35),
            color=color.blue,
            parent=camera.ui
        )

        # Текст
        self.health_text = Text(
            text='HP: 100',
            position=(-0.75, 0.45),
            scale=1.2,
            parent=camera.ui
        )

        self.hunger_text = Text(
            text='Голод: 100',
            position=(-0.75, 0.40),
            scale=1.2,
            parent=camera.ui
        )

        self.thirst_text = Text(
            text='Жажда: 100',
            position=(-0.75, 0.35),
            scale=1.2,
            parent=camera.ui
        )

        # Инвентарь
        self.inventory_text = Text(
            text='Инвентарь:',
            position=(0.7, 0.45),
            scale=1.2,
            parent=camera.ui
        )

        # Время суток
        self.time_text = Text(
            text='День',
            position=(0, 0.45),
            scale=1.5,
            parent=camera.ui
        )

        # Прицел
        self.crosshair = Entity(
            model='quad',
            color=color.white,
            scale=(0.01, 0.1),
            parent=camera.ui
        )

        self.crosshair2 = Entity(
            model='quad',
            color=color.white,
            scale=(0.1, 0.01),
            parent=camera.ui
        )

    def update(self):
        # Обновление показателей
        self.health_text.text = f'HP: {player.health}'
        self.hunger_text.text = f'Голод: {int(player.hunger)}'
        self.thirst_text.text = f'Жажда: {int(player.thirst)}'

        self.health_bar.scale_x = 0.2 * (player.health / player.max_health)
        self.hunger_bar.scale_x = 0.2 * (player.hunger / 100)
        self.thirst_bar.scale_x = 0.2 * (player.thirst / 100)

        # Обновление инвентаря
        inv_text = 'Инвентарь:\n'
        for item, count in player.inventory.items():
            if count > 0:
                inv_text += f'{item}: {count}\n'
        self.inventory_text.text = inv_text

        # Время суток
        self.time_text.text = 'День' if is_day else 'Ночь'
        self.time_text.color = color.white if is_day else color.light_gray


ui = GameUI()


# ========== ОСНОВНОЙ ЦИКЛ ИГРЫ ==========
def update():
    global current_time, is_day, fog_density

    # Система дня и ночи
    current_time += time.dt
    if current_time > DAY_LENGTH:
        current_time = 0
        is_day = not is_day

    # Обновление тумана
    if is_day:
        fog_density = max(0, fog_density - 0.1 * time.dt)
    else:
        fog_density = min(0.05, fog_density + 0.1 * time.dt)

    # Обновление UI
    ui.update()

    # Голод и жажда
    player.hunger = max(0, player.hunger - 0.02 * time.dt)
    player.thirst = max(0, player.thirst - 0.03 * time.dt)

    # Урон от голода/жажды
    if player.hunger <= 0 or player.thirst <= 0:
        player.health = max(0, player.health - 0.5 * time.dt)

    # Смерть игрока
    if player.health <= 0:
        print("Вы умерли!")
        player.position = (0, 0, 0)
        player.health = 50
        player.hunger = 50
        player.thirst = 50

    # Проверка здоровья ресурсов
    for resource in resources[:]:
        if resource.health <= 0:
            if resource.resource_type == 'tree':
                player.inventory['wood'] += random.randint(10, 20)
            elif resource.resource_type == 'stone':
                player.inventory['stone'] += random.randint(5, 10)

            resources.remove(resource)
            destroy(resource)

    # Проверка здоровья животных
    for animal in animals[:]:
        if animal.health <= 0:
            player.inventory['food'] += 10 if animal.animal_type == 'deer' else 5
            animals.remove(animal)
            destroy(animal)


def input(key):
    # Управление оружием (ЛКМ)
    if key == 'left mouse down' and player.equipped_weapon and not player.building_mode:
        player.equipped_weapon.attack()

    # Строительство (ПКМ)
    elif key == 'right mouse down' and player.building_mode and player.equipped_building:
        if mouse.hovered_entity:
            new_pos = mouse.hovered_entity.position + mouse.normal

            # Проверка на возможность строительства
            can_build = True
            for e in scene.entities:
                if hasattr(e, 'position') and distance(e.position, new_pos) < 0.5:
                    can_build = False
                    break

            if can_build and new_pos.y >= 0:
                recipe_key = f'{player.building_material}_{player.equipped_building}'
                if recipe_key in crafting_recipes:
                    recipe = crafting_recipes[recipe_key]
                    if all(player.inventory.get(res, 0) >= amount for res, amount in recipe.items()):
                        for res, amount in recipe.items():
                            player.inventory[res] -= amount

                        new_piece = BuildingPiece(
                            position=new_pos,
                            piece_type=player.equipped_building,
                            material=player.building_material
                        )
                        building_pieces.append(new_piece)

    # Переключение режима строительства (B)
    elif key == 'b':
        player.toggle_building_mode()

    # Крафт предметов (1-5)
    elif key in ('1', '2', '3', '4', '5'):
        items = list(crafting_recipes.keys())
        if int(key) - 1 < len(items):
            item = items[int(key) - 1]
            if all(player.inventory.get(res, 0) >= amount for res, amount in crafting_recipes[item].items()):
                for res, amount in crafting_recipes[item].items():
                    player.inventory[res] -= amount

                if item in ('spear', 'bow'):
                    player.equip_weapon(item)
                elif item.endswith(('wall', 'foundation', 'doorway')):
                    player.equipped_building = item.split('_')[1]
                    player.building_material = item.split('_')[0]
                    player.toggle_building_mode()

    # Поедание пищи (E)
    elif key == 'e' and player.inventory['food'] > 0:
        player.inventory['food'] -= 1
        player.hunger = min(100, player.hunger + 30)

    # Питье воды (Q)
    elif key == 'q' and player.inventory['water'] > 0:
        player.inventory['water'] -= 1
        player.thirst = min(100, player.thirst + 50)

    # Выход (ESC)
    elif key == 'escape':
        app.userExit()


# ========== ЗАПУСК ИГРЫ ==========
# Освещение
DirectionalLight(color=color.white, direction=(1, -1, 1))
AmbientLight(color=color.rgba(200, 200, 200, 0.2))

# Небо
Sky(texture='sky_sunset')

# Серверный поток
if SERVER:
    def handle_client(client_socket, addr):
        print(f"Подключен клиент {addr}")
        try:
            while True:
                data = client_socket.recv(4096)
                if not data: break

                # Обработка данных от клиента
                data = pickle.loads(data)

                # Рассылка данных всем клиентам
                for client in clients:
                    client.send(pickle.dumps(data))

        finally:
            client_socket.close()
            print(f"Клиент {addr} отключен")


    clients = []


    def accept_connections():
        while True:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()


    threading.Thread(target=accept_connections, daemon=True).start()

# Запуск
app.run()