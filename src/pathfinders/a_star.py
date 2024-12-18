import heapq

from src.pathfinders.base import Pathfinder


class AStarPathfinder(Pathfinder):
    """
    Класс для реализации алгоритма A* для поиска пути в лабиринте.

    Наследует от базового класса Pathfinder и реализует метод поиска пути
    от начальной до конечной точки с использованием алгоритма A*.
    """

    def find_path(self):
        """
        Находит путь от начальной до конечной точки, используя алгоритм A*.

        :return: Список координат, представляющий найденный путь, или None,
                 если путь не найден.
        """
        start = self.maze.start
        end = self.maze.end
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, end)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end:
                path = self.reconstruct_path(came_from, current)
                self.maze.display(path)
                return path

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)

                if 0 <= neighbor[0] < self.maze.width and 0 <= neighbor[1] < self.maze.height:
                    if self.maze.grid[neighbor[1]][neighbor[0]] in [1, 3]:  # Пропуск стен и песка
                        continue

                    # Сбор монет
                    if self.maze.grid[neighbor[1]][neighbor[0]] == 2:
                        self.maze.coins_collected += 1
                        self.maze.grid[neighbor[1]][neighbor[0]] = 0  # Обнуляем клетку после сбора монеты

                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)

                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))

            self.display(self.reconstruct_path(came_from, current), current)

        return None

    @staticmethod
    def heuristic(a, b):
        """
        Вычисляет эвристическую оценку расстояния между двумя точками.

        :param a: Координаты первой точки (x, y).
        :param b: Координаты второй точки (x, y).
        :return: Эвристическая оценка (манхэттенское расстояние) между
                 точками a и b.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def reconstruct_path(came_from, current):
        """
        Восстанавливает полный путь из начальной точки до конечной.

        :param came_from: Словарь, содержащий информацию о предыдущих
                          координатах для каждой точки пути.
        :param current: Текущие координаты (x, y) конечной точки.
        :return: Список координат, представляющий полный путь от начальной
                 до конечной точки.
        """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path
