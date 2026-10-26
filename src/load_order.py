"""
Модуль вычисления порядка загрузки зависимостей.
Этап 4: Топологическая сортировка (алгоритм Кана).
"""

def topological_sort(graph):
    """
    Выполняет топологическую сортировку графа зависимостей.
    graph: словарь {пакет: [список его зависимостей]}.
    Возвращает список пакетов в порядке загрузки или None, если есть цикл.
    """
    dependents = {node: [] for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            if dep in dependents:
                dependents[dep].append(node)

    in_degree = {node: len(deps) for node, deps in graph.items()}

    queue = [node for node in graph if in_degree[node] == 0]
    result = []

    while queue:
        current = queue.pop(0)
        result.append(current)

        for dependent in dependents[current]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    if len(result) != len(graph):
        return None

    return result
