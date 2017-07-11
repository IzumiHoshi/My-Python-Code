"""
this is a program for eSpace add motion.
"""

import os


def get_file_list(file_list = None):
    if file_list is None:
        file_list = []
    for x in os.listdir('.'):
        if os.path.isfile(x):
            ext = x[-3:].lower()
            if ext == "gif" or ext == "jpg" or ext == "png":
                file_list.append(x)


def write_file(file_list):
    f = open('Motion.ini', 'w')
    i = 1
    for x in file_list:
        a = "[%(name)a]\nfile = %(age)s\nhint =  \n" % {'name': i, 'age': x}
        f.write(a)
        i += 1


if __name__ == '__main__':
    files = []
    get_file_list(files)
    write_file(files)
