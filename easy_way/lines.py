import cv2
import numpy as np
import itertools
import functools
from combine_lines import change_horizontal_lines


def find_main_lines(image, type):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
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

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def delete_vert_line(det_vert_line):
    """
    Принимает: массив вертикальных линий
    Возвращает: массив вертикальных линий с зануленными боковыми линиями
    """
    detected_vertical_lines_1 = np.rot90(det_vert_line, k=-1)
    d = {}
    for i in range(len(detected_vertical_lines_1[:,:10])):
        d[i] = detected_vertical_lines_1[i].sum() / 255
    d_1 = {}
    total = 0
    k = 0
    for key, value in d.items():
        if value == 0:
            if total > 0:
                d_1[key-k] = total
            total = 0
            k = 0
        if value != 0:
            total += value
            k += 1
    max_1 = max(d_1.values())
    max_2 = 0
    for key, value in d_1.items():
        if value > max_2 and value < max_1:
            max_2 = value
    i1 = get_key(d_1, max_1)
    i2 = get_key(d_1, max_2)
    if i1 > i2:
        i2, i1 = i1, i2
    for key, value in d.items():
        if key < i1:
            d[key] = 0
    for key, value in d.items():
        if value == 0:
            detected_vertical_lines_1[key] = 0
    return np.rot90(detected_vertical_lines_1)


def padding(img_to_predict):
    l = max(img_to_predict.shape)
    im_bg = np.ones((l, l))
    im_bg = im_bg * 255
    im_bg[:img_to_predict.shape[0], :img_to_predict.shape[1]] = img_to_predict
    return im_bg


def get_horlines_coor(detected_horizontal_lines):
    hor_lines_coor = []
    x1 = -1
    x2 = -1
    y1 = -1
    y2 = -1
    flag = False
    for i in range(len(detected_horizontal_lines)):
        flag = False
        for j in range(len(detected_horizontal_lines[i])):
            if (detected_horizontal_lines[i][j] == 255) and (not flag):
                x1 = j
                y1 = i
                flag = True
            if (detected_horizontal_lines[i][j] == 0) and flag:
                x2 = j
                y2 = i
                hor_lines_coor.append([x1, y1, x2, y2])
                break
    return hor_lines_coor


def get_vertlines_coor(detected_vertical_lines):
    ver_lines_coor = []
    x1 = -1
    x2 = -1
    y1 = -1
    y2 = -1
    cnt = 0
    max_cnt = len(detected_vertical_lines[0])
    flag = False
    for i in range(max_cnt):
        flag = False
        for j in range(len(detected_vertical_lines)):
            if (detected_vertical_lines[j][i] == 255) & (not flag):
                x1 = i
                y1 = j
                flag = True
            if (detected_vertical_lines[j][i] == 0) & flag:
                x2 = i
                y2 = j
                ver_lines_coor.append([x1, y1, x2, y2])
                break
    return ver_lines_coor


def find_lines_tz(image):  # третий пункт тз = распознавание линий

    image_with_counters = image.copy()
    detected_horizontal_lines = find_main_lines(image, 'h')
    detected_vertical_lines = find_main_lines(image, 'v')

    detected_horizontal_lines = change_horizontal_lines(detected_horizontal_lines)

    merge_line = merge_lines(detected_horizontal_lines, detected_vertical_lines)

    merge_line_cut = merge_lines(detected_horizontal_lines, delete_vert_line(detected_vertical_lines))

    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # Morphological operation to detect verticle lines from an image
    dilated_merge_line_cut = cv2.dilate(merge_line_cut, kernel, iterations=3)

    # hor_lines_coor = get_horlines_coor(detected_horizontal_lines)
    # ver_lines_coor = get_vertlines_coor(detected_vertical_lines)

    for i in range(image_with_counters.shape[0]):
        for j in range(image_with_counters.shape[1]):
            if merge_line_cut[i, j] == 255:
                image_with_counters[i, j, 0] = 255
                image_with_counters[i, j, 1] = 111
                image_with_counters[i, j, 2] = 111

    return image, merge_line, dilated_merge_line_cut

def find_cells_tz(merge_line, image, merge_line_cut): #нахождение и выделение ячеек = тз пункт 4 + 5
    united_image = merge_line.copy()
    united_image_cut = merge_line_cut.copy()
    contours, hierarchy = cv2.findContours(united_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours_cut, hierarchy_cut = cv2.findContours(united_image_cut, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    #find_coordinates_of_rows(image, united_image, contours)
    bounding_boxes = sort_contours(contours, "top-to-right")
    bounding_boxes_cut = sort_contours(contours_cut, "top-to-right")
    image_with_cells = image.copy()
    max_cell_w = -1
    max_cell_s = 0
    import random as rd
    cnt = 0
    for cell in bounding_boxes:
        rgb = [rd.randint(0,255),rd.randint(0,255),rd.randint(0,255)]
        x, y, w, h = cell[0], cell[1], cell[2], cell[3]
        if (max_cell_s < w*h) and (cnt != 0):
            max_cell_s = w*h
            max_cell_coords_s = [x, y, w, h]
        if (max_cell_w < w) and (cnt != 0):
            max_cell_w = w
            max_cell_coords_w = [x, y, w, h]
        image_with_cells[y:y+h,x:x+w,0] = rgb[0]
        image_with_cells[y:y+h,x:x+w,1] = rgb[1]
        image_with_cells[y:y+h,x:x+w,2] = rgb[2]
        cnt += 1

    image_name = image[max_cell_coords_s[1]:max_cell_coords_s[1]+max_cell_coords_s[3],max_cell_coords_s[0]:max_cell_coords_s[0]+max_cell_coords_s[2]].copy()
    longest_image = image[max_cell_coords_w[1]:max_cell_coords_w[1]+max_cell_coords_w[3],max_cell_coords_w[0]:max_cell_coords_w[0]+max_cell_coords_w[2]].copy()
    image_with_cells_to_predict = image.copy()
    bounding_boxes_to_predict = []
    cnt = 0
    for cell in bounding_boxes_cut:
        rgb = [rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)]
        x, y, w, h = cell[0], cell[1], cell[2], cell[3]
        if y<(max_cell_coords_w[1]) and (cnt != 0):
            bounding_boxes_to_predict.append(cell)
            image_with_cells_to_predict[y:y+h, x:x+w, 0] = rgb[0]
            image_with_cells_to_predict[y:y+h, x:x+w, 1] = rgb[1]
            image_with_cells_to_predict[y:y+h, x:x+w, 2] = rgb[2]
        cnt += 1

    counter = 0
    img_arr = [[], [], [], [], [], [], []]
    for i in range(len(bounding_boxes_to_predict)):
        x, y, w, h = bounding_boxes_to_predict[i][0], bounding_boxes_to_predict[i][1], bounding_boxes_to_predict[i][2], bounding_boxes_to_predict[i][3]
        img_arr[counter % 7].append(image[y-1:y+h+1, x-1:x+w+1])
        counter += 1
    return bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, img_arr