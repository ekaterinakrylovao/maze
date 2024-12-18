import unittest
from src.maze import Maze
from src.generators.dfs import DFSGenerator


class TestDFSGenerator(unittest.TestCase):
    def setUp(self):
        """Создание экземпляра Maze и генератора перед каждым тестом."""
        self.maze = Maze(5, 5, DFSGenerator)

    def test_generate(self):
        """Тестирование корректной генерации лабиринта."""
        self.maze.generate()
        self.assertEqual(self.maze.grid[0][0], 0)  # Начальная точка


if __name__ == "__main__":
    unittest.main()
