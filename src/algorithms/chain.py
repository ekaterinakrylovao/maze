# # algorithms/chain.py
#
# class ChainAlgorithm:
#     def __init__(self, maze):
#         self.maze = maze
#         self.width = maze.width
#         self.height = maze.height
#
#     def find_path(self, start, end):
#         start_x, start_y = start
#         end_x, end_y = end
#
#         # Проверка, что начальная и конечная точки находятся в пределах лабиринта
#         if not self.is_valid(start_x, start_y) or not self.is_valid(end_x, end_y):
#             return None
#
#         # Хранение посещённых узлов
#         visited = set()
#         path = []
#         found = self.search(start_x, start_y, end_x, end_y, visited, path)
#
#         return path if found else None
#
#     def search(self, x, y, end_x, end_y, visited, path):
#         # Если достигли конца, добавляем координаты в путь и возвращаем True
#         if (x, y) == (end_x, end_y):
#             path.append((x, y))
#             return True
#
#         # Если узел уже посещён или не проходимый, возвращаем False
#         if (x, y) in visited or not self.is_valid(x, y):
#             return False
#
#         # Отмечаем узел как посещённый
#         visited.add((x, y))
#         path.append((x, y))
#
#         # Проверка всех 4 направлений (вверх, вниз, влево, вправо)
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             if self.search(x + dx, y + dy, end_x, end_y, visited, path):
#                 return True
#
#         # Если путь не найден, убираем узел из пути
#         path.pop()
#         return False
#
#     def is_valid(self, x, y):
#         # Проверка на границы и проходимость
#         return 0 <= x < self.width and 0 <= y < self.height and self.maze.grid[y][x] == 0
