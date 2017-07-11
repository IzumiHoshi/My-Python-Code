import os


class Deal:
    def __init__(self):
        self.path = os.getcwd()
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self, path):
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path

    def saveImg(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"
        f = open(file_name, "w+")
        f.write(content.encode('utf-8'))

    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension


def format_size(size):
    # convert byte to kb
    try:
        size = float(size)
        kb = size / 1024
    except:
        print("wrong input")
        return "Error"
    return kb
    # if kb >= 1024:
    #     M = kb / 1024
    #     if M >= 1024:
    #         G = M / 1024
    #         return "%fG" % (G)
    #     else:
    #         return "%fM" % (M)
    # else:
    #     return "%fkb" % (kb)


def get_file_size(path):
    # get_file_size
    try:
        size = os.path.getsize(path)
        return format_size(size)
    except Exception as err:
        print(err)


def get_folder_size(path):
    # get_folder_size
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return format_size(sumsize)
    except Exception as err:
        print(err)
