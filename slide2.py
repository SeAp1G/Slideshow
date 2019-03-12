#!/usr/bin/env python
from subprocess import call
import os
import argparse
import shutil

def create_video(args, fname):
    args.append(fname)
    call(args)


def intersperse(lst, item):
    # Remove the slide, so we don't have 3 in a row
    if item in lst:
        lst.remove(item)

    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result


def slides(timings, f_names):
    loop_arg = []
    final_args = ['ffmpeg']
    filter_str = ''
    end_string = ''
    i = 0

    for name in f_names:
        loop_arg.extend(['-loop', '1', '-t',
                         timings[name]['slide_dur'], '-i', name])
        filter_str = filter_str + '[' + str(i) + ':v]setsar=sar=300/300' + '[v' + str(i) + '];'
        end_string = end_string + '[v' + str(i) + ']'
        i = i + 1

    final_args.extend(loop_arg)
    end_string = end_string + 'concat=n=' + str(len(f_names)) + ':v=1:a=0[v]'
    final_args.extend(['-filter_complex', filter_str + end_string])
    final_args.extend(['-map', '[v]'])

    return final_args


# find all the files in the folder that match the extension
def process_folder(folder_name, ext):
    f_names = []
    for file in os.listdir(path=str(folder_name)):
        if file.endswith(('.jpg', '.jpeg', '.png')):  # проходимся по всем файлам, и если они джипег, кидаем их в список
            f_names.append(file)

    print(f_names)
    return f_names


# Create the arguments parser
def define_args():
    parser = argparse.ArgumentParser(
        description='A slide show creator, from pictures having \
                        uniform size and format. Uses ffmpeg.')
    parser.add_argument('-f', '--folder', help='The location of the images, \
                        Final / expected.', default='./images/')
    parser.add_argument('-sd', '--slide_dur', help='Duration each slide will \
                        display for. Does nothing when reading config',
                        default='2')
    parser.add_argument('-fo', '--file_name', help='The output filename, \
                        with ext', default='slideshow.mp4')
    parser.add_argument('-e', '--extension', help='Extension for input files. \
                        Does nothing when reading config', default='.jpeg')
    return parser


def main(foldername):
    parser = define_args()
    args = parser.parse_args()
    mode = 'slideshow-from-folder'
    folder = '{}'.format(foldername)
    print('Это значение folder -  {}'.format(folder))
    print('Аргументы {}'.format(args))
    if mode == 'slideshow-from-folder':
        slide_dur = args.slide_dur
        print('Значение {} передается функции process folder'.format(folder))
        f_names = process_folder(folder, args.extension)
        timings = dict([(name, dict([('slide_dur', slide_dur)])) for name in f_names])
        args_out = slides(timings, f_names)
        print('Аргументы которые передаются непосредственно ffmpeg {}'.format(args_out))
        fname = '{}.mp4'.format(foldername)
        print('Имя файла с слайдшоу - {}'.format(fname))
        create_video(args_out, fname)


def dirs():
    filenames = os.listdir('.')  # get all files' and folders' names in the current directory
    result = []
    for filename in filenames:  # loop through all the files and folders
        if os.path.isdir(
                os.path.join(os.path.abspath("."), filename)):  # check whether the current object is a folder or not
            result.append(filename)
    result.sort()

def start(all_dirs):
    print('Система перешла в папку -- {}'.format(all_dirs))
    os.chdir(all_dirs)
    try:
        os.mkdir('slideshow')
        print('В папке - {}, создалась папка slideshow'.format(all_dirs))
    except OSError or FileExistsError:
        shutil.rmtree('slideshow')
        os.mkdir('slideshow')
        print('В папке - {}, создалась папка slideshow'.format(all_dirs))
    main(all_dirs)


index_dir = str(input('Введите путь к папке: ') or os.getcwd())
slides_num = (int(input('Сколько слайдов в папках?') or int(5)) - 1)


#==========================
#==========================
#==========================
#==========================


def copy_in_folders(path):
    files_list = []  # получаем список файлов
    folder_num = 1
    new_folder_name = 'slides {}'.format(folder_num)  # название с которого начинаются папки
    for file in os.listdir(path=str(path)):
        if file.endswith(('.jpg', '.jpeg', '.png')):  # проходимся по всем файлам, и если они джипег, кидаем их в список
            files_list.append(file)

    if len(files_list) > slides_num:
        try:
            os.mkdir('{}'.format(new_folder_name))  # пытаемся создать папку, если она есть - трем ее, и все что внутри
        except FileExistsError:
            shutil.rmtree('{}'.format(new_folder_name))
            os.mkdir('{}'.format(new_folder_name))

        for x in files_list:
            if len(os.listdir(path='{}'.format(new_folder_name))) < slides_num:
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

def delete_slides_folders(): # удаление всех папок slides (они нам не нужны после создания слайдшоу)
    subdirs = get_folders_with_slides()
    for i in subdirs:
        try:
            shutil.rmtree(i)
            print('{} - папка со слайдами удалена'.format(i[len(index_dir):]))
        except FileNotFoundError:
            pass

def rollon_print():
    subdirs = []
    folderize()
    for y in [x[0] for x in os.walk(index_dir)]:
        if y.rsplit('\\', 1)[-1].startswith('slides '):
            subdirs.append(y)
    for i in range(len(subdirs)):
        start(subdirs[i])
        os.chdir(index_dir)
    delete_some_empty_shit()
    delete_slides_folders()

rollon_print()

