"""
Модуль построения графа зависимостей.
Этап 3: BFS с рекурсией, учет глубины и циклов.
"""


def recursive_bfs(node, graph, depth, max_depth, visited, result):
    """
    Рекурсивный обход графа в ширину (BFS).
    node: текущий пакет.
    graph: словарь зависимостей.
    depth: текущий уровень.
    max_depth: максимальная глубина.
    visited: множество посещённых узлов.
    result: список для сохранения пар (от кого, кому).
    """
    if depth > max_depth:
        return

    if node in visited:
        return

    visited.add(node)
    dependencies = graph.get(node, [])

    for dep in dependencies:
        result.append((node, dep))
        recursive_bfs(dep, graph, depth + 1, max_depth, visited, result)


def build_graph(root_package, packages_dict, max_depth):
    """
    Строит граф зависимостей, начиная с root_package.
    Возвращает список кортежей (пакет, зависимость).
    """
    visited = set()
    result = []
    recursive_bfs(root_package, packages_dict, 1, max_depth, visited, result)
    return result


def load_test_graph(file_path):
    """
    Загружает граф из тестового файла.
    """
    graph = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if ":" in line:
                    pkg, deps_str = line.split(":", 1)
                    pkg = pkg.strip()
                    deps = [d.strip() for d in deps_str.split(",") if d.strip()]
                    graph[pkg] = deps
        return graph
    except FileNotFoundError:
        print(f"Ошибка: тестовый файл {file_path} не найден")
        return None
