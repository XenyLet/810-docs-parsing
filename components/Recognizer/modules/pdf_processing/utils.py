import numpy as np

def maxSub_non_null(a):
    max_so_far = []
    max_sum = 0
    cur = []
    for n in a:
        if n > 0:
            cur.append(n)
        else:
            cur_sum = sum(cur)
            if cur_sum > max_sum:
                max_sum = cur_sum
                max_so_far = cur
            cur = []

    return len(max([max_so_far, cur], key=sum))


def min_max(my_list):
    min_ = next((i for i, x in enumerate(my_list) if x), None)
    max_ = np.max(np.nonzero(my_list))
    return min_, max_


def custom_tuple_sorting(s, t, offset=4):
    x0, y0, _, _ = s
    x1, y1, _, _ = t
    if abs(y0 - y1) > offset:
        if y0 < y1:
            return -1
        else:
            return 1
    else:
        if x0 > x1:
            return -1

        elif x0 == x1:
            return 0

        else:
            return 1


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k
