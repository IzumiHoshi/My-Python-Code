import os
import shutil
from download_img import get_file_size
from PIL import Image
from grab_html import img_down
import json


def move_file(name, size):
    if size == 1:
        shutil.move(name, 'small\\' + name)
    elif size == 2:
        shutil.move(name, 'middle\\' + name)
    elif size == 3:
        shutil.move(name, 'large\\' + name)
    elif size == 0:
        shutil.move(name, 'gif\\' + name)


def sort_pic():
    os.chdir('ooxx')
    lists = os.listdir('.')
    for name in lists:
        if name[-4:] == '.gif':
            move_file(name, 0)
        if name[-4:] != '.jpg':
            continue
        size = get_file_size(name)
        print 'size = %d' % size
        if 0.01 > size - 5.24 > -0.01:
            print('remove useless file.')
            os.remove(name)
            continue
        img = Image.open(name)
        img_size = img.size
        min_size = min(img_size)
        if min_size > 1000:
            move_file(name, 3)
        elif min_size > 500:
            move_file(name, 2)
        else:
            move_file(name, 1)


def redownload():
    urls = open('url_json.txt', 'r')
    u_dict = json.load(urls)
    os.chdir('Redownload')
    lists = os.listdir('.')
    for name in lists:
        url = u_dict.get(name)
        if url is None:
            continue
        img_down(name, url, check=False)


if __name__ == '__main__':
    redownload()
    # urls = open('ooxx/url.txt', 'r')
    # u_dict = {}
    # for line in urls.readlines():
    #     space = line.find(' ')
    #     # url = line[space + 1:-1]
    #     url = line[space:].strip()
    #     name = line[:space]
    #     u_dict[name] = url
    # j = json.dumps(u_dict, indent=1)
    # f = open('url_json.txt', 'w')
    # f.write(j)
    # f.close()
    # parser = my_html_parser()
    # parser.feed('''<html>
    # <head></head>
    # <body>
    # <!-- test html parser -->
    #     <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
    # </body></html>''')
