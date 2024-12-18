import unittest
from src.maze import Maze
from src.pathfinders.chain import ChainPathfinder


class TestChainPathfinder(unittest.TestCase):
    def setUp(self):
        # Заданный лабиринт с открытыми и закрытыми клетками
        self.grid = [
            [0, 0, 1, 0, 0],
            [1, 0, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0]
        ]

    def test_chain_pathfinder(self):
        maze = Maze(width=5, height=5, generator=None)
        maze.grid = self.grid
        maze.set_start_end((0, 0), (4, 4))
        pathfinder = ChainPathfinder(maze)

        # Проверка, что путь найден и правильный
        path = pathfinder.find_path()
        self.assertIsNotNone(path, "Путь не найден ChainPathfinder")
        self.assertEqual(path[0], (0, 0), "Неправильная начальная точка")
        self.assertEqual(path[-1], (4, 4), "Неправильная конечная точка")

        # Отображение лабиринта с визуализацией пути
        maze.display(path, current=path[-1])


if __name__ == '__main__':
    unittest.main()
