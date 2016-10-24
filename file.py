import os

b = [x for x in os.listdir('.') if os.path.isdir(x)]

a = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py']

# print(a)
# print(b)

# c = [y for y in [x for x in os.listdir('.') if os.path.isdir(x)] if os.path.isdir(y)]
#
# def f(dir):
#     print(dir)
#     if dir == '':
#         return []
#     return [x for x in os.listdir(f(os.lisdir(dir)))]# if os.path.exists(x)]
#
# c = os.path.join(os.path.abspath('.'), 'code')
# d = os.listdir(c)
# print(d)
# print(f(c))



def myscans(dir, words):
    def finddir(fuckdir, word, dirpath = []):
        if os.path.isdir(fuckdir):
            for x in os.listdir(fuckdir):
                print(x)
                mycah = os.path.join(fuckdir, x)
                if x.find(word) != -1 and os.path.isfile(x):
                    dirpath.append(mycah)
                # if os.path.isdir(x):
                #     print('is dir:' + x)
                finddir(mycah,word)
        else:
            print('not dir:' + fuckdir)
        return dirpath
    return (finddir(dir, words))

print(myscans('.', 'i'))
# print(myscan('.', 'u'))



#
# print(os.getcwd())
# def main():
#     for root, dirs, files in os.walk('..\\'):
#         for dir in dirs:
#             print(os.path.join(root, dir))
#         for file in files:
#             print(os.path.join(root, file))
# # main()
#
# print(os.walk('.'))