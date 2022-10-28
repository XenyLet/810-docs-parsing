import pytesseract as pyt
import numpy as np
from search_pdf import create_list_of_pdf
from lines import find_lines_tz, find_cells_tz
import matplotlib.pyplot as plt
from config import path_tesseract

def recognizing(path_to_pdf):
    img_matrix = []
    unrecognized_list = []
    # pyt.pytesseract.tesseract_cmd = path_tesseract
    print('recognizing')
    list_of_elements, specification, other, img_list_of_elems, img_specification = create_list_of_pdf(path_to_pdf)

    for path in specification:
        try:
            # img_list_of_elems = break_up_pdf_to_array_png(path, 200)
            for img in img_specification:
                im = []
                image, merge_line, merge_line_cut = find_lines_tz(img)
                bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, cells_to_predict = find_cells_tz(
                    merge_line, image, merge_line_cut)
                for row in cells_to_predict:
                    for cell in row:
                        d = []
                        ver = []
                        data = pyt.image_to_data(cell, lang='rus+eng', output_type='dict')
                        text = pyt.image_to_string(cell, lang='rus+eng', config='--psm 4')
                        for v in data['conf']:
                            if v != '-1':
                                ver.append(float(v))
                        if text[:-1]:
                            d.append(text[:-1])
                            d.append(np.mean(ver))
                            im.append(d)
                img_matrix.append(im)
        except Exception:
            unrecognized_list.append(path)
    for path in list_of_elements:
            # img_specification = break_up_pdf_to_array_png(path, 200)
            for img in img_list_of_elems:
                im = []
                image, merge_line, merge_line_cut = find_lines_tz(img)
                bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, cells_to_predict = find_cells_tz(
                    merge_line, image, merge_line_cut)
                for row in cells_to_predict:
                    for cell in row:
                        try:
                            d = []
                            ver = []  # ver -> veroyatnost' -> probability (seems like text detection probabilities)
                            data = pyt.image_to_data(cell, lang='rus+eng', output_type='dict')
                            text = pyt.image_to_string(cell, lang='rus+eng', config='--psm 4')
                            v = 1  # just quickfix to move on. TODO: fix later
                            ver.append(float(v))
                            d.append(text[:-1])
                            d.append(np.mean(ver))
                            im.append(d)
                        except Exception as exc:
                            print("ERROR:", str(exc))
                            unrecognized_list.append(path)
                img_matrix.append(im)


    elems = []
    for elem in img_matrix[0]:
        elems.append(elem[0])

    return elems, unrecognized_list
