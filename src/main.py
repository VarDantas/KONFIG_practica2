"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Этап 2: Сбор данных о прямых зависимостях.
"""

import argparse
import sys

from parser import fetch_content, parse_packages, get_direct_dependencies


def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей"
    )
    parser.add_argument("--package", required=True,
                        help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True,
                        help="URL-адрес репозитория или путь к файлу")
    parser.add_argument("--mode", choices=["url", "file"], default="url",
                        help="Режим работы с репозиторием")
    parser.add_argument("--output", default="graph.png",
                        help="Имя сгенерированного файла с изображением")
    parser.add_argument("--depth", type=int, default=3,
                        help="Максимальная глубина анализа зависимостей")
    return parser.parse_args()


def validate_args(args):
    """Проверяет параметры на корректность."""
    if args.depth <= 0:
        print(f"Ошибка: глубина анализа должна быть больше 0")
        sys.exit(1)
    return True


def print_config(args):
    """Выводит параметры в формате ключ: значение."""
    print("Параметры запуска")
    print(f"package: {args.package}")
    print(f"repo: {args.repo}")
    print(f"mode: {args.mode}")
    print(f"output: {args.output}")
    print(f"depth: {args.depth}")


def main():
    """Главная функция."""
    args = parse_args()

    if not validate_args(args):
        sys.exit(1)

    print_config(args)

    print("\nЗагрузка данных о пакетах...")
    content = fetch_content(args.repo, args.mode)
    if content is None:
        print("Не удалось загрузить данные.")
        sys.exit(1)

    print("Разбор данных...")
    packages = parse_packages(content)

    print(f"\nПрямые зависимости для пакета '{args.package}':")
    deps = get_direct_dependencies(args.package, packages)

    if deps is None:
        print(f"Пакет '{args.package}' не найден в репозитории.")
        sys.exit(1)

    if not deps:
        print("(нет зависимостей)")
    else:
        for dep in deps:
            print(f"- {dep}")


if __name__ == "__main__":
    main()
