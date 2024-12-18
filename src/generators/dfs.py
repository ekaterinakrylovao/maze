import random

from src.generators.base import Generator


class DFSGenerator(Generator):
    """
    Алгоритм генерации лабиринта с помощью поиска в глубину (DFS).

    :param maze: Экземпляр класса Maze.
    """
    def __init__(self, maze):
        super().__init__(maze)
        self.visited = [[False for _ in range(self.maze.width)] for _ in range(self.maze.height)]

    def generate(self):
        """Запуск генерации лабиринта с помощью DFS."""
        start_x, start_y = 0, 0
        self._dfs(start_x, start_y)
        self.maze.generate_surfaces()  # Генерация монеток и песка

    def _dfs(self, x, y):
        """
        Рекурсивная функция для выполнения обхода в глубину.

        :param x: Координата X текущей ячейки.
        :param y: Координата Y текущей ячейки.
        """
        self.visited[y][x] = True
        self.maze.grid[y][x] = 0

        self.maze.display(current=(x, y))

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2

            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and not self.visited[ny][nx]:
                self.maze.grid[y + dy][x + dx] = 0
                self._dfs(nx, ny)
