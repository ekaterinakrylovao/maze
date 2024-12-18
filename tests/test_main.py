from src.main import main
from unittest.mock import patch


def test_main() -> None:
    with patch("builtins.input", side_effect=[
        "1",  # Выбор алгоритма генерации (DFS)
        "нет",  # Не добавлять поверхности
        "5",  # Ширина лабиринта
        "5",  # Высота лабиринта
        "0,0",  # Координаты начала
        "4,4",  # Координаты конца
        "1",  # Выбор алгоритма поиска пути (Chain Algorithm)
        "нет",  # Не продолжать работу с лабиринтом
        "нет"  # Не создавать новый лабиринт
    ]):
        main()
