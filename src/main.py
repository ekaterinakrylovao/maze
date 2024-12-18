import logging
import os
import platform

from src.maze import Maze
from src.generators.dfs import DFSGenerator
from src.generators.kruskal import KruskalGenerator
from src.pathfinders.chain import ChainPathfinder
from src.pathfinders.a_star import AStarPathfinder

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

MAZE_GENERATORS = {
    "1": ("DFS", DFSGenerator),
    "2": ("Kruskal", KruskalGenerator),
}

PATHFINDERS = {
    "1": ("Chain Algorithm", ChainPathfinder),
    "2": ("A* Algorithm", AStarPathfinder),
}


def select_option(options, prompt):
    """
    Универсальная функция для выбора опции из предложенного списка.

    :param options: Словарь доступных опций. Ключ — строка, значение — кортеж (название, класс).
    :param prompt: Сообщение, выводимое пользователю для выбора опции.
    :return: Выбранный кортеж (название, класс) или None, если выбор некорректен.
    """
    print(prompt)
    for key, (name, _) in options.items():
        print(f"{key}. {name}")

    choice = input("Выберите опцию: ")
    return options.get(choice)


def main() -> None:
    logger.info(platform.python_version())

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        generator_choice = select_option(MAZE_GENERATORS, "Выберите алгоритм генерации лабиринта:")
        if generator_choice is None:
            print("Ошибка: неверный выбор генератора. Попробуйте снова.")
            continue

        generator_name, generator_class = generator_choice

        surface_option = input("Добавить типы поверхностей (монетки и песок)? (да/нет): ").strip().lower() == "да"

        while True:
            try:
                width = int(input("Введите ширину лабиринта: "))
                height = int(input("Введите высоту лабиринта: "))

                if width < 3 or height < 3:
                    print("Ошибка: ширина и высота должны быть не меньше 3. Попробуйте снова.")
                    continue
                break
            except ValueError:
                print("Ошибка: пожалуйста, введите целое число.")

        maze = Maze(width, height, generator_class, surfaces=surface_option)
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
                maze.display()

                while True:
                    pathfinder_choice = select_option(PATHFINDERS, "Выберите алгоритм поиска пути:")
                    if pathfinder_choice is None:
                        print("Ошибка: неверный выбор алгоритма. Попробуйте снова.")
                        continue

                    _, pathfinder_class = pathfinder_choice
                    pathfinder = pathfinder_class(maze)

                    path = pathfinder.find_path()

                    if path:
                        if maze.surfaces:
                            print(f"Собрано монет: {maze.coins_collected}")
                        print(f"Найден путь с использованием {pathfinder_choice[0]}:", path)
                        break
                    else:
                        print("Путь не найден.")
                        break

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
