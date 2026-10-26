"""
Модуль визуализации графа зависимостей.
Этап 5: Генерация D2, SVG и конвертация в PNG через rsvg-convert.
"""

import subprocess


def generate_d2_code(edges):
    """
    Генерирует текст на языке D2 из списка связей.
    edges: список кортежей (родитель, потомок).
    """
    lines = ["# Граф зависимостей"]
    for parent, child in edges:
        lines.append(f'"{parent}" -> "{child}"')
    return "\n".join(lines)


def save_d2_and_render(d2_code, output_png):
    """
    Сохраняет D2-код, генерирует SVG через d2,
    а затем конвертирует SVG в PNG через rsvg-convert.
    """
    d2_file = output_png.replace(".png", ".d2")
    svg_file = output_png.replace(".png", ".svg")

    with open(d2_file, "w", encoding="utf-8") as f:
        f.write(d2_code)
    print(f"D2-код сохранён в {d2_file}")

    try:
        subprocess.run(["d2", d2_file, svg_file], check=True)
        print(f"SVG-файл сохранён в {svg_file}")
    except FileNotFoundError:
        print("Ошибка: утилита 'd2' не найдена. Установите её.")
        return
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при вызове d2: {e}")
        return

    try:
        subprocess.run(["rsvg-convert", svg_file, "-o", output_png], check=True)
        print(f"Изображение сохранено в {output_png}")
    except FileNotFoundError:
        print("Ошибка: утилита 'rsvg-convert' не найдена. Установите librsvg2-bin.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации в PNG: {e}")
