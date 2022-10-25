import functools
import itertools

import cv2
import numpy as np

from modules.utils import min_max, maxSub_non_null, custom_tuple_sorting


def change_horizontal_lines(detected_horizontal_lines_main):
    detected_horizontal_lines = detected_horizontal_lines_main.copy()

    for i in range(detected_horizontal_lines.shape[0] - 11):
        if (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and (
                sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0) and (
                sum(detected_horizontal_lines[i + 8]) != 0) and (sum(detected_horizontal_lines[i + 9]) != 0) and (
                sum(detected_horizontal_lines[i + 10]) != 0):
            detected_horizontal_lines[i + 6] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + detected_horizontal_lines[i + 7] + \
                                               detected_horizontal_lines[i + 8] + detected_horizontal_lines[i + 9] + \
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

        if (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and (
                sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0) and (
                sum(detected_horizontal_lines[i + 8]) != 0) and (sum(detected_horizontal_lines[i + 9]) != 0):
            detected_horizontal_lines[i + 6] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + detected_horizontal_lines[i + 7] + \
                                               detected_horizontal_lines[i + 8] + detected_horizontal_lines[i + 9]
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

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and (
                sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0) and (
                sum(detected_horizontal_lines[i + 8]) != 0):
            detected_horizontal_lines[i + 5] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + detected_horizontal_lines[i + 7] + \
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

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and (
                sum(detected_horizontal_lines[i + 6]) != 0) and (sum(detected_horizontal_lines[i + 7]) != 0):
            detected_horizontal_lines[i + 4] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                               detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                               detected_horizontal_lines[i + 4] + detected_horizontal_lines[i + 5] + \
                                               detected_horizontal_lines[i + 6] + detected_horizontal_lines[i + 7]
            min_, max_ = min_max(detected_horizontal_lines[i + 4])
            detected_horizontal_lines[i + 4][min_:max_] = [255] * len(detected_horizontal_lines[i + 4][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 6] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 7] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0) and (
                sum(detected_horizontal_lines[i + 6]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                           detected_horizontal_lines[i + 4] + detected_horizontal_lines[i + 5] + \
                                           detected_horizontal_lines[i + 6]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 6] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0) and (sum(detected_horizontal_lines[i + 5]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                           detected_horizontal_lines[i + 4] + detected_horizontal_lines[i + 5]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 5] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0) and (
                sum(detected_horizontal_lines[i + 4]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3] + \
                                           detected_horizontal_lines[i + 4]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 4] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0) and (sum(detected_horizontal_lines[i + 3]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
                                           detected_horizontal_lines[i + 2] + detected_horizontal_lines[i + 3]
            min_, max_ = min_max(detected_horizontal_lines[i])
            detected_horizontal_lines[i][min_:max_] = [255] * len(detected_horizontal_lines[i][min_:max_])

            detected_horizontal_lines[i + 1] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 2] = [0] * detected_horizontal_lines.shape[1]
            detected_horizontal_lines[i + 3] = [0] * detected_horizontal_lines.shape[1]

        elif (sum(detected_horizontal_lines[i]) != 0) and (sum(detected_horizontal_lines[i + 1]) != 0) and (
                sum(detected_horizontal_lines[i + 2]) != 0):
            detected_horizontal_lines[i] = detected_horizontal_lines[i] + detected_horizontal_lines[i + 1] + \
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


def skew_correction(image_name):
    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
    coords = np.column_stack(np.where(img_bin == 255))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    elif angle == 90:
        angle = 0

    elif 45 < angle < 90:
        angle = 90 - angle

    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def find_main_lines(image, type):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)
    limg = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(gray, kernel, iterations=1)
    _, img_bin = cv2.threshold(erosion, 128, 255, cv2.THRESH_BINARY_INV)
    if type == 'h':
        structuring_element = np.ones((1, 75), np.uint8)
    elif type == 'v':
        structuring_element = np.ones((75, 1), np.uint8)
    erode_image = cv2.erode(img_bin, structuring_element, iterations=1)
    dilate_image = cv2.dilate(erode_image, structuring_element, iterations=1)

    return dilate_image



def merge_lines(horizontal_lines, vertical_lines):
    structuring_element = np.ones((3, 3), np.uint8)
    merge_image = horizontal_lines + vertical_lines
    merge_image = cv2.dilate(merge_image, structuring_element, iterations=2)
    return merge_image


def sort_contours(cnts, method):
    bounding_boxes = [cv2.boundingRect(c) for c in cnts]
    if method == "top-to-right":
        bounding_boxes.sort(key=functools.cmp_to_key(lambda s, t: custom_tuple_sorting(s, t, 4)))

    elif method == "left-to-right":
        bounding_boxes.sort(key=lambda tup: tup[0])

    return bounding_boxes


def find_cell_contours(frame_image, crop_image):
    white_pixels = np.where(frame_image == 255)
    y = white_pixels[0]
    x = white_pixels[1]
    for i in range(len(y)):
        crop_image[y[i]][x[i]] = 255
    return crop_image


def find_digit_coordinates(image):
    cnts, _ = cv2.findContours(
        image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    bounding_boxes = sort_contours(cnts, method="left-to-right")[1:]
    all_contours = []
    for i in range(0, len(bounding_boxes)):
        x, y, w, h = bounding_boxes[i][0], bounding_boxes[i][1], bounding_boxes[i][2], bounding_boxes[i][3]
        if True:
            digit_coordinates = [x, y, x + w, y + h]
            all_contours.append(digit_coordinates)
    return all_contours


def crop_digit(image, x0, y0, x1, y1):
    img_crop = image[y0 - 2:y1 + 2, x0 - 2:x1 + 2]
    res_crop_img = cv2.resize(img_crop, (28, 28))
    prediction_digit = predicting(res_crop_img)
    return prediction_digit


def detect_contour_in_contours(all_contours):
    for rec1, rec2 in itertools.permutations(all_contours, 2):
        if rec2[0] >= rec1[0] and rec2[1] >= rec1[1] and rec2[2] <= rec1[2] and rec2[3] <= rec1[3]:
            in_rec = [rec2[0], rec2[1], rec2[2], rec2[3]]
            all_contours.remove(in_rec)
    return all_contours


def image_binarization_2(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)
    return img_bin
