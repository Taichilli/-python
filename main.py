# Напишите функцию, которая получает на вход директорию и рекурсивно
# обходит её и все вложенные директории. Результаты обхода сохраните в
# файлы json, csv и pickle.
# ○ Для дочерних объектов указывайте родительскую директорию.
# ○ Для каждого объекта укажите файл это или директория.
# ○ Для файлов сохраните его размер в байтах, а для директорий размер
# файлов в ней с учётом всех вложенных файлов и директорий.
# Соберите из созданных на уроке и в рамках домашнего задания функций
# пакет для работы с файлами разных форматов


# Промежуточная аттестация
# Решить задания, которые не успели решить на семинаре.
# Возьмите любые 1-3 задания из прошлых домашних заданий.
# Добавьте к ним логирование ошибок и полезной информации.
# Также реализуйте возможность запуска из командной строки с передачей параметров.


import os
import json
import csv
import pickle
import logging
import argparse


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("directory_scanner.log"), logging.StreamHandler()])


def get_directory_info(path):
    result = []

    def recursive_scan(directory, parent=None):
        total_size = 0
        directory_info = {'name': os.path.basename(directory), 'path': directory, 'type': 'directory', 'parent': parent,
                          'size': 0}

        try:
            for entry in os.scandir(directory):
                if entry.is_file():
                    size = entry.stat().st_size
                    file_info = {'name': entry.name, 'path': entry.path, 'type': 'file', 'parent': directory, 'size': size}
                    result.append(file_info)
                    total_size += size
                elif entry.is_dir():
                    sub_dir_size = recursive_scan(entry.path, directory)
                    total_size += sub_dir_size
        except Exception as e:
            logging.error(f"Ошибка доступа к {directory}: {e}")
            directory_info['error'] = str(e)

        directory_info['size'] = total_size
        result.append(directory_info)
        return total_size

    recursive_scan(path)
    return result


def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении в {filename}: {e}")


def save_to_csv(data, filename):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['name', 'path', 'type', 'parent', 'size']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        logging.info(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении в {filename}: {e}")


def save_to_pickle(data, filename):
    try:
        with open(filename, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)
        logging.info(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        logging.error(f"Ошибка при сохранении в {filename}: {e}")


def main(directory_path):
    try:
        data = get_directory_info(directory_path)
        save_to_json(data, 'directory_info.json')
        save_to_csv(data, 'directory_info.csv')
        save_to_pickle(data, 'directory_info.pkl')
    except Exception as e:
        logging.error(f"Ошибка при обработке директории {directory_path}: {e}")


if __name__ == "__main__":
    setup_logging()
    parser = argparse.ArgumentParser(description="Сканировать директорию и сохранить информацию о её содержимом.")
    parser.add_argument("directory", help="Путь к директории для сканирования")
    args = parser.parse_args()

    main(args.directory)
