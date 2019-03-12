# Задача-1:
# Напишите скрипт, создающий директории dir_1 - dir_9 в папке,
# из которой запущен данный скрипт.
# И второй скрипт, удаляющий эти папки.

import os
import shutil

index_dir = str(input('Введите путь к папке: ') or os.getcwd())


def copy_in_folders(path):
    files_list = []  # получаем список файлов
    folder_num = 1
    new_folder_name = 'slides {}'.format(folder_num)  # название с которого начинаются папки
    for file in os.listdir(path=str(path)):
        if file.endswith(('.jpg', '.jpeg')):  # проходимся по всем файлам, и если они джипег, кидаем их в список
            files_list.append(file)

    if len(files_list) > 5:
        try:
            os.mkdir('{}'.format(new_folder_name))  # пытаемся создать папку, если она есть - трем ее, и все что внутри
        except FileExistsError:
            shutil.rmtree('{}'.format(new_folder_name))
            os.mkdir('{}'.format(new_folder_name))

        for x in files_list:
            if len(os.listdir(path='{}'.format(new_folder_name))) < 5:
                shutil.copyfile(str(x), str('{}/{}').format(str(new_folder_name), str(x)))
            else:
                folder_num += 1
                new_folder_name = 'slides {}'.format(folder_num)
                print(
                    'В папке {} --- cоздана новая папка картинками - {}'.format(path[len(index_dir):], new_folder_name))
                try:
                    os.mkdir('{}'.format(new_folder_name))
                except FileExistsError:
                    shutil.rmtree('{}'.format(new_folder_name))
                    os.mkdir('{}'.format(new_folder_name))
    else:
        print('Тут картинок нет - {}'.format(path[len(index_dir):]))


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


def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)


def delete_some_empty_shit():
    subdirs = [x[0] for x in os.walk(index_dir)]
    for i in subdirs:
        try:
            del_empty_dirs(i)
            # print('{} - пустая папка, удалена'.format(i[len(index_dir):]))
        except FileNotFoundError:
            pass


def folderize():
    for i in get_dirs(index_dir):
        try:
            os.chdir(i)
            copy_in_folders(i)
            os.chdir(index_dir)
        except FileNotFoundError:
            pass
    delete_some_empty_shit()


def get_folders_with_slides():  # получаем список всех папок со слайдами
    folder_with_slides = []
    for y in [x[0] for x in os.walk(index_dir)]:
        if y.rsplit('\\', 1)[-1].startswith('slides '):
            folder_with_slides.append(y)
    return folder_with_slides

