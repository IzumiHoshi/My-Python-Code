import urllib2 as myurl
from bs4 import BeautifulSoup as BS
from bs4 import Tag
import os
from download_img import get_file_size


def grab_bs(soup=Tag):
    oo = int(soup.find(class_='tucao-like-container').span.string)
    xx = int(soup.find(class_='tucao-unlike-container').span.string)
    # print('oo [%d] xx [%d]' % (oo, xx))
    if oo < xx or oo < 60:
        return ''
    imgs = soup.find_all(class_='view_img_link')
    if imgs is None:
        print('wrong')
        return ''
    filename = soup.attrs['id']
    lines = ''
    i = 1
    for img in imgs:
        url = img.attrs['href'][2:]
        if imgs.__len__() == 1:
            line = '%s.%s http://%s\n' % (filename, url[-3:], url)
        else:
            line = '%s_%02d.%s http://%s\n' % (filename, i, url[-3:], url)
        # print line
        lines += line
        i += 1

    return lines


def tag_has_id(tag):
    return tag.name == 'li' and tag.has_attr('id') and tag.attrs['id'].find('comment-') != -1


def grab_by_bs(file):
    f = open(file, 'rb')
    html = BS(f, 'html.parser')
    print(html.prettify())


def pull_url(in_name, out_name):
    i = open(in_name, 'r')
    o = open(out_name, 'a')
    soup = BS(i, 'lxml')
    li = soup.find(tag_has_id)

    grab_bs(li)
    text = ''
    for a in li.next_siblings:
        if isinstance(a, Tag) is not True:
            continue
        text += grab_bs(a)
    o.write(text)
    o.close()
    i.close()


def grab_jandan_pic():
    # for i in range(1, 100):
    #     name = 'url' + str(i) + '.txt'
    #     w = open(name, 'w')
    #     url = 'http://jandan.net/ooxx/page-' + str(i)
    #     res = myurl.urlopen(url)
    #     w.write(res.read())
    #     w.close()

    for i in range(1, 100):
        name = 'url' + str(i) + '.txt'
        pull_url(name, 'url.txt')


def img_down(filename, imgurl, check=True):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        'Cookie': 'AspxAutoDetectCookieSupport=1',
    }
    print 'downloading: ' + filename
    if check is True and os.path.exists(filename):
        size = get_file_size(filename)
        print '%s already exists. size = %s' % (filename, size)
        if size > 20 or size < 5.5:
            return
        print 'remove %s, re-download.' % filename
        os.remove(filename)

    request = myurl.Request(imgurl, None, header)
    response = myurl.urlopen(request)
    data = response.read()
    f = open(filename, 'wb')
    f.write(data)
    f.close()


def test():
    f = open('url_json.txt', 'r')
    for line in f.readlines():
        space = line.find(' ')
        url = line[space:]
        name = line[:space]
        img_down(name, url)


if __name__ == '__main__':
    os.chdir('ooxx')
    # grab_jandan_pic()
    test()
    # grab_by_bs('c.html')
