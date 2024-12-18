# import heapq
#
#
# class Pathfinder:
#     def __init__(self, maze):
#         self.maze = maze
#
#     def find_path(self):
#         path = []
#         if self._chain_algorithm(self.maze.start, path):
#             return path
#         return None
#
#     def _chain_algorithm(self, position, path):
#         if position == self.maze.end:
#             return True
#
#         x, y = position
#         if position in path or self.maze.grid[y][x] == 1:
#             return False  # Возвращаемся, если уже были здесь или стена
#
#         path.append(position)  # Добавляем текущую позицию в путь
#         self.maze.display(path, position)  # Визуализируем текущую позицию
#
#         # Пробуем двигаться в 4 направлениях
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             next_position = (x + dx, y + dy)
#             if 0 <= next_position[0] < self.maze.width and 0 <= next_position[1] < self.maze.height:
#                 if self._chain_algorithm(next_position, path):
#                     return True
#
#         # Отрисовываем текущую позицию, чтобы показать "ножки" при возвращении к предыдущей позиции
#         self.maze.display(path, position)
#
#         path.pop()  # Убираем из пути, если тупик
#         if path:  # Проверяем, если есть предыдущие позиции
#             self.maze.display(path, path[-1])  # Визуализируем путь с последней позицией
#         return False
#
# class AStarPathfinder(Pathfinder):
#     def __init__(self, maze):
#         super().__init__(maze)
#
#     def find_path(self):
#         start = self.maze.start
#         end = self.maze.end
#         open_set = []
#         heapq.heappush(open_set, (0, start))  # (приоритет, позиция)
#         came_from = {}
#         g_score = {start: 0}  # Стоимость пути от начала до текущей позиции
#         f_score = {start: self.heuristic(start, end)}  # Оценка стоимости пути
#
#         while open_set:
#             current = heapq.heappop(open_set)[1]  # Позиция с наименьшей оценкой f_score
#
#             if current == end:
#                 return self.reconstruct_path(came_from, current)
#
#             x, y = current
#
#             # Пробуем двигаться в 4 направлениях
#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 neighbor = (x + dx, y + dy)
#
#                 if 0 <= neighbor[0] < self.maze.width and 0 <= neighbor[1] < self.maze.height:
#                     if self.maze.grid[neighbor[1]][neighbor[0]] == 1:  # Если это стена
#                         continue
#
#                     # Расчет стоимости пути
#                     tentative_g_score = g_score[current] + 1  # Предполагаем, что все движения стоят 1
#
#                     if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
#                         # Этот путь до соседа лучше
#                         came_from[neighbor] = current
#                         g_score[neighbor] = tentative_g_score
#                         f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, end)
#
#                         if neighbor not in [i[1] for i in open_set]:  # Если сосед не в открытом списке
#                             heapq.heappush(open_set, (f_score[neighbor], neighbor))
#
#             self.maze.display(self.reconstruct_path(came_from, current), current)
#
#         return None  # Путь не найден
#
#     def heuristic(self, a, b):
#         # Используем манхэттенское расстояние как эвристику
#         return abs(a[0] - b[0]) + abs(a[1] - b[1])
#
#     def reconstruct_path(self, came_from, current):
#         total_path = [current]
#         while current in came_from:
#             current = came_from[current]
#             total_path.append(current)
#         total_path.reverse()  # Обратим порядок для правильного пути
#         return total_path
from src.maze import Maze
from src.generators.dfs import DFSGenerator
from src.generators.kruskal import KruskalGenerator
from src.pathfinders.chain import ChainPathfinder
from src.pathfinders.a_star import AStarPathfinder


MAZE_GENERATORS = {
    "1": ("DFS", DFSGenerator),
    "2": ("Kruskal", KruskalGenerator),
}

PATHFINDERS = {
    "1": ("Chain Algorithm", ChainPathfinder),
    "2": ("A* Algorithm", AStarPathfinder),
}


def select_option(options, prompt):
    """Универсальная функция для выбора опции из списка."""
    print(prompt)
    for key, (name, _) in options.items():
        print(f"{key}. {name}")

    choice = input("Выберите опцию: ")
    return options.get(choice)


def main():
    while True:
        generator_choice = select_option(MAZE_GENERATORS, "Выберите алгоритм генерации лабиринта:")
        if generator_choice is None:
            print("Ошибка: неверный выбор генератора. Попробуйте снова.")
            continue

        generator_name, generator_class = generator_choice
        width = int(input("Введите ширину лабиринта: "))
        height = int(input("Введите высоту лабиринта: "))

        maze = Maze(width, height, generator_class)
        maze.generate()
        maze.display()

        while True:

            available_cells = [(x, y) for y in range(height) for x in range(width) if maze.grid[y][x] == 0]
            print("Доступные пустые ячейки (x, y):", available_cells)

            start = input("Введите координаты начала (x,y): ")
            end = input("Введите координаты конца (x,y): ")

            try:
                start_x, start_y = map(int, start.split(","))
                end_x, end_y = map(int, end.split(","))

                if (start_x, start_y) not in available_cells or (end_x, end_y) not in available_cells:
                    print("Ошибка: Убедитесь, что координаты находятся среди доступных пустых ячеек.")
                    continue

                maze.set_start_end((start_x, start_y), (end_x, end_y))

                pathfinder_choice = select_option(PATHFINDERS, "Выберите алгоритм поиска пути:")
                if pathfinder_choice is None:
                    print("Ошибка: неверный выбор алгоритма. Попробуйте снова.")
                    continue

                _, pathfinder_class = pathfinder_choice
                pathfinder = pathfinder_class(maze)

                path = pathfinder.find_path()

                if path:
                    print(f"Найден путь с использованием {pathfinder_choice[0]}:", path)
                else:
                    print("Путь не найден.")

                continue_choice = input("Хотите продолжить работу с этим лабиринтом? (да/нет): ").lower()
                if continue_choice != 'да':
                    break

                maze.display()

            except ValueError:
                print("Ошибка: Введите корректные координаты в формате x,y.")

        new_maze_choice = input("Хотите создать новый лабиринт? (да/нет): ").lower()
        if new_maze_choice != 'да':
            print("Завершение работы.")
            break


if __name__ == "__main__":
    main()
