from src.pathfinders.base import Pathfinder


class ChainPathfinder(Pathfinder):
    """
    Класс для реализации алгоритма поиска пути с использованием алгоритма цепей.

    Наследует от базового класса Pathfinder и реализует метод поиска пути
    для нахождения маршрута от начальной точки до конечной в заданном лабиринте.

    Методы:
        find_path(): Находит путь от начальной до конечной точки с помощью
                     алгоритма цепей.
        _chain_algorithm(position, path): Рекурсивный метод для выполнения
                                          алгоритма цепей.
    """
    def find_path(self):
        path = []
        if self._chain_algorithm(self.maze.start, path):
            return path
        return None

    def _chain_algorithm(self, position, path):
        if position == self.maze.end:
            path.append(position)
            self.display(path, current=None)
            return True

        x, y = position
        if position in path or self.maze.grid[y][x] in [1, 3]:  # Избегаем стен и песка
            return False

        # Сбор монет
        if self.maze.grid[y][x] == 2:
            self.maze.coins_collected += 1
            self.maze.grid[y][x] = 0  # Обнуляем клетку после сбора монеты

        path.append(position)
        self.display(path, position)

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_position = (x + dx, y + dy)
            if 0 <= next_position[0] < self.maze.width and 0 <= next_position[1] < self.maze.height:
                if self._chain_algorithm(next_position, path):
                    return True

        path.pop()
        if path:
            self.display(path, path[-1])
        return False
