
# coding: utf-8
import datetime
import time

start = datetime.datetime.now()

import cv2

import warnings

warnings.filterwarnings("ignore")

from common.image import split_pdf_to_images
from common.utils import get_absolute_coords

from components.Recognizer.modules.pdf_processing.image import sort_contours, merge_lines, change_horizontal_lines, \
    find_main_lines, delete_vert_line


def find_lines_tz(image):  # третий пункт тз = распознавание линий
    image_with_counters = image.copy()
    detected_horizontal_lines = find_main_lines(image, 'h')
    detected_vertical_lines = find_main_lines(image, 'v')
    detected_horizontal_lines = change_horizontal_lines(detected_horizontal_lines)
    merge_line = merge_lines(detected_horizontal_lines, detected_vertical_lines)
    merge_line_cut = merge_lines(detected_horizontal_lines, delete_vert_line(detected_vertical_lines))
    for i in range(image_with_counters.shape[0]):
        for j in range(image_with_counters.shape[1]):
            if merge_line_cut[i, j] == 255:
                image_with_counters[i, j, 0] = 255
                image_with_counters[i, j, 1] = 111
                image_with_counters[i, j, 2] = 111
    return image, merge_line, merge_line_cut


def find_cells_tz(merge_line, image, merge_line_cut):  # нахождение и выделение ячеек = тз пункт 4 + 5
    united_image = merge_line.copy()
    united_image_cut = merge_line_cut.copy()
    contours, hierarchy = cv2.findContours(united_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours_cut, hierarchy_cut = cv2.findContours(united_image_cut, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    bounding_boxes = sort_contours(contours, "top-to-right")
    bounding_boxes_cut = sort_contours(contours_cut, "top-to-right")
    image_with_cells = image.copy()
    max_cell_w = -1
    max_cell_s = 0
    import random as rd
    cnt = 0
    for cell in bounding_boxes:
        rgb = [rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)]
        x, y, w, h = cell[0], cell[1], cell[2], cell[3]
        if (max_cell_s < w * h) and (cnt != 0):
            max_cell_s = w * h
            max_cell_coords_s = [x, y, w, h]
        if (max_cell_w < w) and (cnt != 0):
            max_cell_w = w
            max_cell_coords_w = [x, y, w, h]
        image_with_cells[y:y + h, x:x + w, 0] = rgb[0]
        image_with_cells[y:y + h, x:x + w, 1] = rgb[1]
        image_with_cells[y:y + h, x:x + w, 2] = rgb[2]
        cnt += 1

    image_name = image[max_cell_coords_s[1]:max_cell_coords_s[1] + max_cell_coords_s[3],
                 max_cell_coords_s[0]:max_cell_coords_s[0] + max_cell_coords_s[2]].copy()
    longest_image = image[max_cell_coords_w[1]:max_cell_coords_w[1] + max_cell_coords_w[3],
                    max_cell_coords_w[0]:max_cell_coords_w[0] + max_cell_coords_w[2]].copy()
    image_with_cells_to_predict = image.copy()
    bounding_boxes_to_predict = []
    cnt = 0
    for cell in bounding_boxes_cut:
        rgb = [rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255)]
        x, y, w, h = cell[0], cell[1], cell[2], cell[3]
        if y < (max_cell_coords_w[1]) and (cnt != 0):
            bounding_boxes_to_predict.append(cell)
            image_with_cells_to_predict[y:y + h, x:x + w, 0] = rgb[0]
            image_with_cells_to_predict[y:y + h, x:x + w, 1] = rgb[1]
            image_with_cells_to_predict[y:y + h, x:x + w, 2] = rgb[2]
        cnt += 1
    counter = 0
    img_arr = [[], [], [], [], [], [], []]
    bounding_boxes_to_predict_by_row = [[], [], [], [], [], [], []]
    for i in range(len(bounding_boxes_to_predict)):
        x, y, w, h = bounding_boxes_to_predict[i][0], \
                     bounding_boxes_to_predict[i][1], \
                     bounding_boxes_to_predict[i][2], \
                     bounding_boxes_to_predict[i][3]
        img_arr[counter % 7].append(image[y - 1:y + h + 1, x - 1:x + w + 1])
        bounding_boxes_to_predict_by_row[counter % 7].append(bounding_boxes_to_predict[i])
        counter += 1
    return bounding_boxes, image_name, longest_image, bounding_boxes_to_predict_by_row, img_arr

def run(pdf_filename, text_recognizer):
    # recognition_result = {
    #     "text": "abc",
    #     "conf": 0.1,
    #     "bbox": [y_min, x_min, h, w]
    # }

    results = []
    pages = split_pdf_to_images(pdf_filename, 200)
    for page in pages:
        image, merge_line, merge_line_cut = find_lines_tz(page)
        bounding_boxes_on_image, image_name, longest_image, bounding_boxes_to_predict, img_arr = find_cells_tz(merge_line, image, merge_line_cut)

        print("preprocessing", time.time())

        for col in range(len(img_arr[0])):
            for row in range(len(img_arr) - 1, -1, -1):
                predicted_text, confidence, bbox_in_cell = text_recognizer.read_text(
                    img_arr[row][col]
                )

                if len(predicted_text.strip()) == 0:
                    continue

                bbox = get_absolute_coords(
                    absolute_root_coords=bounding_boxes_to_predict[row][col],
                    relative_from_root_coords=bbox_in_cell
                )

                int_bbox = [int(c) for c in bbox]

                results.append(
                    {
                        "text": predicted_text,
                        "conf": confidence,
                        "bbox": bbox
                    }
                )
                # temporary break
                break
            # temporary break
            break
        # temporary break
        break

    return results



