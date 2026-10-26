"""
Парсер файлов Packages для Ubuntu.
Этап 2: Сбор данных о прямых зависимостях.
"""

import gzip
import re
import urllib.request


def fetch_content(repo_url, mode):
    """
    Получает текст файла Packages.
    """
    if mode == "url":
        try:
            with urllib.request.urlopen(repo_url) as response:
                data = response.read()
        except Exception as error:
            print(f"Ошибка при скачивании: {error}")
            return None
    else:
        try:
            with open(repo_url, "rb") as file:
                data = file.read()
        except Exception as error:
            print(f"Ошибка при чтении файла: {error}")
            return None

    if repo_url.endswith(".gz"):
        try:
            data = gzip.decompress(data)
        except Exception as error:
            print(f"Ошибка при распаковке gzip: {error}")
            return None

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        print("Ошибка: не удалось декодировать файл как UTF-8")
        return None


def clean_dependency(dep):
    """
    Очищает строку зависимости от версий и альтернатив.
    """
    dep = dep.split("|")[0].strip()
    dep = re.sub(r"\(.*\)", "", dep).strip()
    dep = re.sub(r"\[.*\]", "", dep).strip()
    return dep


def parse_packages(text):
    """
    Разбирает текст Packages на словарь {пакет: [зависимости]}.
    """
    packages = {}
    current_package = None
    current_deps = []

    for line in text.splitlines():
        if line.startswith("Package:"):
            if current_package:
                packages[current_package] = current_deps
            current_package = line.split(":", 1)[1].strip()
            current_deps = []
        elif line.startswith("Depends:"):
            deps_str = line.split(":", 1)[1].strip()
            for dep in deps_str.split(","):
                cleaned = clean_dependency(dep)
                if cleaned:
                    current_deps.append(cleaned)
        elif not line.strip() and current_package:
            packages[current_package] = current_deps
            current_package = None
            current_deps = []

    if current_package:
        packages[current_package] = current_deps

    return packages


def get_direct_dependencies(package_name, packages):
    """
    Возвращает список прямых зависимостей для указанного пакета.
    """
    if package_name not in packages:
        return None
    return packages[package_name]
