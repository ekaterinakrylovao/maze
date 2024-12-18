import io
import contextlib
import unittest

from src.maze import Maze
from src.generators.kruskal import KruskalGenerator


class TestKruskalGenerator(unittest.TestCase):
    def setUp(self):
        """Инициализация тестов"""
        self.maze = Maze(5, 5, KruskalGenerator)

    def test_generate_maze(self):
        """Проверка корректности генерации лабиринта"""
        self.maze.generate()

        passages = sum(row.count(0) for row in self.maze.grid)
        self.assertGreater(passages, 0)

    def test_display_maze(self):
        """Тестирование отображения лабиринта"""
        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):
            self.maze.display()

        output = buffer.getvalue()

        self.assertNotEqual(output.strip(), "")

    def test_invalid_maze_size(self):
        """Проверка устойчивости к неправильным входным данным"""
        with self.assertRaises(ValueError):
            Maze(1, 1, KruskalGenerator)

    def test_find_union(self):
        """Проверка функций find_set и union"""
        generator = KruskalGenerator(self.maze)
        generator.sets[0][0] = (0, 0)
        generator.sets[1][1] = (1, 1)

        generator.union(0, 0, 1, 1)

        self.assertEqual(generator.find_set(0, 0), generator.find_set(1, 1))


if __name__ == "__main__":
    unittest.main()
