"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Этап 1: Минимальный прототип с конфигурацией (CLI).
"""

import argparse
import sys


def parse_args():
    """
    Разбирает аргументы командной строки.
    Возвращает объект с параметрами.
    """
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей"
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="URL-адрес репозитория или путь к файлу"
    )
    parser.add_argument(
        "--mode",
        choices=["url", "file"],
        default="url",
        help="Режим работы с репозиторием (url или file)"
    )
    parser.add_argument(
        "--output",
        default="graph.png",
        help="Имя сгенерированного файла с изображением"
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Максимальная глубина анализа зависимостей"
    )
    return parser.parse_args()


def validate_args(args):
    """
    Проверяет параметры на корректность.
    Возвращает True, если всё в порядке, иначе завершает программу.
    """
    if args.depth <= 0:
        print(f"Ошибка: глубина анализа должна быть больше 0 (указано: {args.depth})")
        sys.exit(1)

    if args.mode == "file" and not args.repo.endswith((".txt", ".json")):
        pass

    return True

def print_config(args):
    """
    Выводит все настраиваемые параметры в формате ключ: значение.
    """
    print("Параметры запуска")
    print(f"package: {args.package}")
    print(f"repo: {args.repo}")
    print(f"mode: {args.mode}")
    print(f"output: {args.output}")
    print(f"depth: {args.depth}")


def main():
    """
    Главная функция.
    """
    args = parse_args()
    
    if not validate_args(args):
        sys.exit(1)

    print_config(args)
    
    print("\nЭтап 1 успешно выполнен. Параметры корректны.")


if __name__ == "__main__":
    main()
