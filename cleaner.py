import re
import os


def clean(file):
    """
    Удаляет кавычки из заголовка и переносы из ячейки и заполняет ячейки со значением None пустой строкой
    :param file: путь к файлу
    :return: чистый файл в папке clean_files
    """

    if not os.path.exists('./clean_files/'):
        os.makedirs('./clean_files/')
    g = open('./clean_files/' + file, 'w', encoding='utf-8')
    with open(file, 'r', encoding='utf-8') as f:
        print('Чищу {}\n'.format(file))
        first = f.readline()
        first = re.sub('"', '', first)
        g.write(first)
        for line in f.readlines():
            line1 = re.sub(',#,#', ',#" ",#', line)
            line2 = line1.strip('\n')
            if line2.endswith('"'):
                g.write(line1)
            else:
                g.write(line2)
    g.close()
    with open('./clean_files/' + file, 'r', encoding='utf-8') as f:
        f = f.readlines()
    with open('./clean_files/' + file, 'w', encoding='utf-8') as g:
        for line in f:
            line = line.strip('\n')
            cells = line.split(',#')
            cells = [i.strip('"') for i in cells]
            line = ',#'.join(cells)
            g.write(line + '\n')


def cleaner():
    """
    Запускает clean для всех файлов формата csv в папке
    :return:
    """
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    for csv in files:
        clean(csv)

cleaner()
