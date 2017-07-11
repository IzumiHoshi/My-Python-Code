class Screen(object):
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    @height.deleter
    def height(self):
        del self._height

    @property
    def resolution(self):
        return self._height * self._width


class Student(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Student Object (name:%s)' % self.name

        # __repr__ = __str__


class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1  # 初始化两个计数器a，b

    def __iter__(self):
        return self  # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b  # 计算下一个值
        if self.a > 100000:  # 退出循环的条件
            raise StopIteration();
        return self.a  # 返回下一个值

class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __call__(self, user):
        return Chain('%s/%s' %(self._path, user))

    def __str__(self):
        return self._path

    __repr__ = __str__


print(Chain().status.user('fuck').timeline.list)


        # print(s)


        # test:
        # s = Screen()
        # s.width = 1024
        # s.height = 768
        # print(s.resolution)
        # s.height
        # print(s.resolution)
        # assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution
        # print(dir(s))
