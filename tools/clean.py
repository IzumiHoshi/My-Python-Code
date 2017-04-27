import os

rubish = ['.obj', '.pdb', '.ilk',
 '.pch', '.res', '.tlog', '.idb',
  '.ipch', '.suo', '.sdf', '.lastbuildstate']


def myscans(dir, words=[]):
    def finddir(fuckdir, word=[], dirpath=[]):     
        for x in os.listdir(fuckdir):
            mycah = os.path.join(fuckdir, x)
            ret = os.path.isdir(mycah)
            print("\t%s is dir : %s" % (x, ret))
            if ret:
                print('walk into :%s' % mycah)
                finddir(mycah, word, dirpath)
            else:
                ext = os.path.splitext(x)[1]
                for w in word:
                    if ext == w:
                        print(x)
                        dirpath.append(mycah)
                        try:
                            os.remove(mycah)
                        except WindowsError:
                            print("delete dir")
                            finddir(mycah, word, dirpath)
                            os.removedirs(mycah)
                        finally:
                            print('finally')
                            break
                       
        return dirpath
    print('scan into :%s' % dir)
    return (finddir(dir, words))


if __name__ == '__main__':
    print(myscans('.', rubish))

