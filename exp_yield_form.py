def inner():
    coef = 1
    total = 0
    while True:
        input_val = yield total
        if input_val == None:
            total = total+1
        else:
            total = total + coef * input_val
        # return total
        # except SwitchSign:
        #     coef = -(coef)
        # except BreakOut:
        #     return total

def outer1():
    print("before inner, i do this")
    i_gen = inner()
    input_val = 1
    ret_val = i_gen.__next__
    while True:
        try:
            input_val = yield ret_val
            ret_val = i_gen.send(input_val)
        except StopIteration:
            break
        except Exception as err:
            try:
                ret_val = i_gen.throw(err)
            except StopIteration:
                break
    print('after inner(), i do that')

def outer2():
    print("before inner, i do this")
    yield from inner()
    print('after inner(), i do that')


# for i in inner():
#     print(i)

# for i in outer1():
#     print(i)

# for i in outer2():
#     print(i)

def h():
    print('Wen Chuan')
    m = yield 5  # Fighting!
    print('m = %s' % m)
    d = yield 12
    print('We are together! [%s]' % d)
c = h()

try:
    print(c.__next__())  #相当于c.send(None)
    print(c.__next__())  #相当于c.send(None)
    print(c.send('Fighting!'))  #(yield 5)表达式被赋予了'Fighting!'
except StopIteration:
    print("fuck")