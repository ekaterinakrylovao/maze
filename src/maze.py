import random
import time
import os


class Maze:
    """
    Класс для представления лабиринта.

    :param width: Ширина лабиринта.
    :param height: Высота лабиринта.
    :param generator: Класс генератора лабиринта.
    """

    # Добавляем поверхностные типы: 0 - проход, 1 - стена, 2 - монетка, 3 - песок
    def __init__(self, width, height, generator=None, surfaces=False):
        if width < 3 or height < 3:
            raise ValueError("Ширина и высота лабиринта должны быть не меньше 3.")
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.surfaces = surfaces
        self.coins_collected = 0  # Счётчик собранных монет
        if generator:
            self.generator = generator(self)
        else:
            self.generator = None
        self.start = None
        self.end = None

    def generate(self):
        """Запуск генерации лабиринта с помощью выбранного алгоритма."""
        self.generator.generate()

    def generate_surfaces(self):
        """Генерация монеток и песка, если surfaces=True."""
        if not self.surfaces:
            return
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 0:
                    if random.random() < 0.1:  # 10% шанс монетки
                        self.grid[y][x] = 2
                    elif random.random() < 0.05:  # 5% шанс песка
                        self.grid[y][x] = 3

    def display(self, path=None, current=None):
        """
        Отображение лабиринта в консоли с возможностью визуализации пути и текущей позиции.

        :param path: Список координат пути, если такой путь был найден.
        :param current: Текущие координаты для визуализации перемещения.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) == self.start:
                    print("🚀  ", end='')
                elif (x, y) == self.end:
                    print("🏁  ", end='')
                elif current and (x, y) == current:
                    print("👣  ", end='')
                elif path and (x, y) in path:
                    print("🌟  ", end='')
                else:
                    cell = self.grid[y][x]
                    print({
                              1: "██  ",  # стена
                              0: "    ",  # проход
                              2: "💰  ",  # монетка
                              3: "🌵  "  # песок
                          }.get(cell, "??  "), end='')  # добавлено отображение монеток и песка
            print()
        time.sleep(0.2)

    def set_start_end(self, start, end):
        """
        Установка начальной и конечной точек в лабиринте для обхода.

        :param start: Координаты начальной точки.
        :param end: Координаты конечной точки.
        :raises ValueError: Если координаты выходят за пределы лабиринта.
        """
        if not (0 <= start[0] < self.width and 0 <= start[1] < self.height):
            raise ValueError("Начальные координаты выходят за пределы лабиринта")
        if not (0 <= end[0] < self.width and 0 <= end[1] < self.height):
            raise ValueError("Конечные координаты выходят за пределы лабиринта")

        self.start = start
        self.end = end

    # Метод для сброса количества монет (если понадобится обнулить)
    def reset_coins(self):
        self.coins_collected = 0
