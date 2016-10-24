import os


def foo1():
    print('Process (%s) start...' % os.getpid())
# only work on Unix/Linux/Mac
    pid = os.fork()
    if pid == 0:
        print('i am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
    else:
        print('i (%S) just create a child process(%s).' % (os.getpid, pid))
    return True


import time, threading

# 假定这是你的银行存款:
balance = 0

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    for i in range(100000):
        change_it(n)

# t1 = threading.Thread(target=run_thread, args=(5,))
# t2 = threading.Thread(target=run_thread, args=(8,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(balance)

balance = 0
lock = threading.Lock()

def runthread(n):
    for i in range(100000):
        # lock
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()


t1 = threading.Thread(target=runthread, args=(5,))
t2 = threading.Thread(target=runthread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)