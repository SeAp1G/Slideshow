# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.

import os
import shutil

index_dir = str(input('Введите путь к папке: ') or os.getcwd())


def get_dirs(path):
    subdirs = [x[0] for x in os.walk(path)]  # получаем список всех директорий в дереве каталогов
    dirs_list = []
    for file in subdirs:
        for _ in os.listdir(file):
            if os.path.isdir(file):
                dirs_list.append(file)
    dirs_list = set(dirs_list)
    dirs_list = list(dirs_list)
    return dirs_list

for i in os.listdir(index_dir):
    print(i)


def delete_slides_folders():
    subdirs = get_folders_with_slides()
    for i in subdirs:
        try:
            shutil.rmtree(i)
            print('{} - папка со слайдами удалена'.format(i[len(index_dir):]))
        except FileNotFoundError:
            pass


def get_folders_with_slides():  # получаем список всех папок со слайдами
    folder_with_slides = []
    for y in [x[0] for x in os.walk(index_dir)]:
        if y.rsplit('\\', 1)[-1].startswith('slides '):
            folder_with_slides.append(y)
    return folder_with_slides

# delete_some_empty_shit()