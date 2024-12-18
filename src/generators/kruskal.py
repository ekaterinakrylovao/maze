import random

from src.generators.base import Generator


class KruskalGenerator(Generator):
    def __init__(self, maze):
        super().__init__(maze)
        self.edges = []
        self.sets = [[(x, y) for x in range(self.maze.width)] for y in range(self.maze.height)]

    def generate(self):
        self.initialize_edges()
        if not self.edges:
            return
        random.shuffle(self.edges)
        for edge in self.edges:
            (x1, y1), (x2, y2) = edge
            if self.find_set(x1, y1) != self.find_set(x2, y2):
                self.union(x1, y1, x2, y2)
                self.maze.grid[(y1 + y2) // 2][(x1 + x2) // 2] = 0
                self.maze.grid[y1][x1] = 0
                self.maze.grid[y2][x2] = 0
                self.maze.display(current=(x1, y1))
        self.maze.generate_surfaces()  # Генерация монеток и песка

    def initialize_edges(self):
        for y in range(0, self.maze.height, 2):
            for x in range(0, self.maze.width, 2):
                if x + 2 < self.maze.width:
                    self.edges.append(((x, y), (x + 2, y)))
                if y + 2 < self.maze.height:
                    self.edges.append(((x, y), (x, y + 2)))

    def find_set(self, x, y):
        if self.sets[y][x] == (x, y):
            return x, y
        else:
            root = self.find_set(*self.sets[y][x])
            self.sets[y][x] = root
            return root

    def union(self, x1, y1, x2, y2):
        root1 = self.find_set(x1, y1)
        root2 = self.find_set(x2, y2)
        if root1 != root2:
            self.sets[root2[1]][root2[0]] = root1
