import io
import contextlib
import unittest

from src.maze import Maze
from src.generators.dfs import DFSGenerator


class TestMaze(unittest.TestCase):
    def setUp(self):
        """Создание экземпляра Maze перед каждым тестом."""
        self.maze = Maze(5, 5, DFSGenerator)

    def test_initialization(self):
        """Тестирование правильности инициализации лабиринта."""
        self.assertEqual(self.maze.width, 5)
        self.assertEqual(self.maze.height, 5)
        self.assertEqual(len(self.maze.grid), 5)
        self.assertEqual(len(self.maze.grid[0]), 5)

    def test_set_start_end(self):
        """Тестирование установки начальных и конечных точек."""
        self.maze.set_start_end((0, 0), (4, 4))
        self.assertEqual(self.maze.start, (0, 0))
        self.assertEqual(self.maze.end, (4, 4))

    def test_display(self):
        """Тестирование отображения лабиринта в консоли."""
        self.maze.grid[1][1] = 0  # Проход
        self.maze.grid[1][2] = 0  # Проход
        self.maze.grid[2][1] = 0  # Проход

        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):
            self.maze.display()

        output = buffer.getvalue()

        self.assertIn("██", output)

        self.assertIn("    ", output)

    def test_invalid_coordinates(self):
        """Тестирование обработки некорректных данных."""
        with self.assertRaises(ValueError):
            self.maze.set_start_end((-1, -1), (6, 6))  # Координаты выходят за пределы


if __name__ == "__main__":
    unittest.main()
