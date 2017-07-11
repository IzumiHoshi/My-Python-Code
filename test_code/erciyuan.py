import math


def quadratic(a, b, c):
    temp = math.sqrt((b * b - 4 * a * c) / 4 * a * a)
    x1 = -(b / 2 * a) - temp
    x2 = -(b / 2 * a) + temp
    return x1, x2


print(quadratic(1, 2, 1))
