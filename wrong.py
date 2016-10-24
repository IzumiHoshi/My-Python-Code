def foo(s):
    n = int(s)
    if n == 0:
        raise ValueError('invalid value: {}'.format(s))
    return 10 / n

def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError!')
       # raise


bar()