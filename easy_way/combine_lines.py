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


def change_horizontal_lines(detected_horizontal_lines_main):
    detected_horizontal_lines = detected_horizontal_lines_main.copy()

    for i in range(detected_horizontal_lines.shape[0] - 11):
        if (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and \
                (sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0) and \
                (sum(detected_horizontal_lines[i + 8]) != 0) and (sum(detected_horizontal_lines[i + 9]) != 0) and \
                (sum(detected_horizontal_lines[i + 10]) != 0):
            detected_horizontal_lines[i + 6] = detected_horizontal_lines[i] + \
                                               detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + \
                                               detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + \
                                               detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + \
                                               detected_horizontal_lines[i + 7] + \
                                               detected_horizontal_lines[i + 8] + \
                                               detected_horizontal_lines[i + 9] + \
                                               detected_horizontal_lines[i + 10]
            min_, max_ = min_max(detected_horizontal_lines[i + 6])
            detected_horizontal_lines[i + 6][min_:max_] = [255] * len(detected_horizontal_lines[i + 6][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 7] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 8] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 9] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 10] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and \
                (sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0) and \
                (sum(detected_horizontal_lines[i + 8]) != 0) and (sum(detected_horizontal_lines[i + 9]) != 0):
            detected_horizontal_lines[i + 6] = detected_horizontal_lines[i] + \
                                               detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + \
                                               detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + \
                                               detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + \
                                               detected_horizontal_lines[i + 7] + \
                                               detected_horizontal_lines[i + 8] + \
                                               detected_horizontal_lines[i + 9]
            min_, max_ = min_max(detected_horizontal_lines[i + 6])
            detected_horizontal_lines[i + 6][min_:max_] = [255] * len(detected_horizontal_lines[i + 6][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 7] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 8] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 9] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and \
                (sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0) and \
                (sum(detected_horizontal_lines[i + 8]) != 0):
            detected_horizontal_lines[i + 5] = detected_horizontal_lines[i] + \
                                               detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + \
                                               detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + \
                                               detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + \
                                               detected_horizontal_lines[i + 7] + \
                                               detected_horizontal_lines[i + 8]
            min_, max_ = min_max(detected_horizontal_lines[i + 5])
            detected_horizontal_lines[i + 5][min_:max_] = [255] * len(detected_horizontal_lines[i + 5][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 6] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 7] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 8] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and \
                (sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0):
            detected_horizontal_lines[i + 4] = detected_horizontal_lines[i] + \
                                               detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + \
                                               detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + \
                                               detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + \
                                               detected_horizontal_lines[i + 7]
            min_, max_ = min_max(detected_horizontal_lines[i + 4])
            detected_horizontal_lines[i + 4][min_:max_] = [255] * len(detected_horizontal_lines[i + 4][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 6] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 7] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and \
                (sum(detected_horizontal_lines[i + 6]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + \
                                           detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + \
                                           detected_horizontal_lines[i + 3] + \
                                           detected_horizontal_lines[i + 4] + \
                                           detected_horizontal_lines[i + 5] + \
                                           detected_horizontal_lines[i + 6]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 6] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + \
                                           detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + \
                                           detected_horizontal_lines[i + 3] + \
                                           detected_horizontal_lines[i + 4] + \
                                           detected_horizontal_lines[i + 5]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and \
                (sum(detected_horizontal_lines[i + 4]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + \
                                           detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + \
                                           detected_horizontal_lines[i + 3] + \
                                           detected_horizontal_lines[i + 4]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + \
                                           detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + \
                                           detected_horizontal_lines[i + 3]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and \
                (sum(detected_horizontal_lines[i + 2]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + \
                                           detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1]

            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]

    start = int(detected_horizontal_lines.shape[1] * 0.5)
    end = int(detected_horizontal_lines.shape[1] * 0.8)
    index_to_null = []

    for i in range(detected_horizontal_lines.shape[0] - 1):
        i_ = maxSub_non_null(detected_horizontal_lines[i][start:end])
        if sum(detected_horizontal_lines[i][start:end]) and (i_ < (end - start)):
            index_to_null.append(i)
            detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]

    for i in index_to_null:
        detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]
        detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
        detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]

    return detected_horizontal_lines