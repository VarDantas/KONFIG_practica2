"""
Инструмент визуализации графа зависимостей.
Этап 3: Построение графа (BFS с рекурсией).
"""

import argparse
import sys

from parser import fetch_content, parse_packages, get_direct_dependencies
from graph import build_graph, load_test_graph
from load_order import topological_sort
from viz import generate_d2_code, save_d2_and_render

def parse_args():
    """Разбирает аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Инструмент визуализации графа зависимостей")
    parser.add_argument("--package", required=True, help="Имя анализируемого пакета")
    parser.add_argument("--repo", required=True, help="URL-адрес или путь к файлу")
    parser.add_argument("--mode", choices=["url", "file"], default="url", help="Режим работы")
    parser.add_argument("--output", default="graph.png", help="Имя файла для картинки")
    parser.add_argument("--depth", type=int, default=3, help="Максимальная глубина")
    return parser.parse_args()


def validate_args(args):
    """Проверяет параметры."""
    if args.depth <= 0:
        print("Ошибка: глубина должна быть больше 0")
        sys.exit(1)
    return True


def print_config(args):
    """Выводит параметры."""
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

    print("\nЗагрузка данных...")
    if args.mode == "file":
        print("Режим тестирования: чтение графа из файла.")
        packages = load_test_graph(args.repo)
        if packages is None:
            sys.exit(1)
    else:
        print("Загрузка из репозитория...")
        content = fetch_content(args.repo, args.mode)
        if content is None:
            sys.exit(1)
        packages = parse_packages(content)

    print(f"\nСтроим граф для пакета '{args.package}' с глубиной {args.depth}...")
    edges = build_graph(args.package, packages, args.depth)

    if not edges:
        print("Граф пуст. Возможно, пакет не найден или у него нет зависимостей.")
        return

    print("\nПорядок загрузки")
    load_order = topological_sort(packages)
    if load_order is None:
        print("В графе обнаружен цикл! Порядок загрузки определить невозможно.")
    else:
        for i, pkg in enumerate(load_order, 1):
            print(f"{i}. {pkg}")
    
    print("\nРезультат (список зависимостей):")
    for parent, child in edges:
        print(f"{parent} -> {child}")

    print("\nВизуализация")
    d2_code = generate_d2_code(edges)
    save_d2_and_render(d2_code, args.output)

if __name__ == "__main__":
    main()
