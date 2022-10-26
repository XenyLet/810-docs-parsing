
# coding: utf-8
import datetime
start = datetime.datetime.now()

# In[1]:
import pytesseract as pyt
import pandas as pd
import cv2
from pdf2image import convert_from_path

import numpy as np
import warnings

import cfg

warnings.filterwarnings("ignore")

from components.Recognizer.modules.pdf_processing.printer import create_report
from components.Recognizer.modules.pdf_processing.utils import get_key
from components.Recognizer.modules.pdf_processing.fileio import search_pdf_in_folder, read_json_file
from components.Recognizer.modules.pdf_processing.image import sort_contours, merge_lines, change_horizontal_lines, find_main_lines


# Функция для второго пункта(Разделяем документ на картинки, того же разрешения (dpi) что и исходный документ)
def break_up_pdf_to_array_png(path_to_pdf, dpi):
    array_png = []
    pages = convert_from_path(path_to_pdf, dpi,
                              #poppler_path=cfg.POPPLER_PATH
                              )
    for page, i in zip(pages, range(len(pages))):
        pix = np.array(page)
        array_png.append(pix[30:-30, 30:-30])
    return array_png



def delete_vert_line(det_vert_line):
    """
    Принимает: массив вертикальных линий
    Возвращает: массив вертикальных линий с зануленными боковыми линиями
    """
    detected_vertical_lines_1 = np.rot90(det_vert_line, k=-1)
    d = {}
    for i in range(len(detected_vertical_lines_1[:, :10])):
        d[i] = detected_vertical_lines_1[i].sum() / 255
    d_1 = {}
    total = 0
    k = 0
    for key, value in d.items():
        if value == 0:
            if total > 0:
                d_1[key - k] = total
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
    # itog_l = l + (28 - l%28)
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
    # image = cv2.imread(path)
    # kernel = np.ones((2, 2), 'uint8')
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # erode_img = cv2.erode(gray, kernel, iterations=1)
    # img_bin = cv2.threshold(erode_img, 128, 255, cv2.THRESH_BINARY_INV)
    # img_bin[1]
    image_with_counters = image.copy()
    detected_horizontal_lines = find_main_lines(image, 'h')
    detected_vertical_lines = find_main_lines(image, 'v')
    # for i in detected_horizontal_lines:
    # print(*i)
    # print(detected_horizontal_lines.shape[0])
    # print(detected_horizontal_lines.shape[1])
    detected_horizontal_lines = change_horizontal_lines(detected_horizontal_lines)
    merge_line = merge_lines(detected_horizontal_lines, detected_vertical_lines)
    merge_line_cut = merge_lines(detected_horizontal_lines, delete_vert_line(detected_vertical_lines))
    hor_lines_coor = get_horlines_coor(detected_horizontal_lines)
    ver_lines_coor = get_vertlines_coor(detected_vertical_lines)
    for i in range(image_with_counters.shape[0]):
        for j in range(image_with_counters.shape[1]):
            if merge_line_cut[i, j] == 255:
                image_with_counters[i, j, 0] = 255
                image_with_counters[i, j, 1] = 111
                image_with_counters[i, j, 2] = 111
    # plt.figure(num=None, figsize=(30, 30), dpi=80, facecolor='w', edgecolor='k')
    # plt.imshow(image)
    # plt.show()
    # plt.figure(num=None, figsize=(30, 30), dpi=80, facecolor='w', edgecolor='k')
    # plt.imshow(image_with_counters)
    # plt.show()
    # print('horizontal lines coorditanes: ')
    # print(hor_lines_coor)
    # print('vertical lines coordinates: ')
    # print(ver_lines_coor)
    return image, merge_line, merge_line_cut


def find_cells_tz(merge_line, image, merge_line_cut):  # нахождение и выделение ячеек = тз пункт 4 + 5
    united_image = merge_line.copy()
    united_image_cut = merge_line_cut.copy()
    contours, hierarchy = cv2.findContours(united_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    contours_cut, hierarchy_cut = cv2.findContours(united_image_cut, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    # find_coordinates_of_rows(image, united_image, contours)
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
    # pic_box = plt.figure(figsize=(40, 40))
    # pic_box.add_subplot(2, 5, 1)
    # plt.imshow(image)
    # pic_box.add_subplot(2, 5, 3)
    # plt.imshow(image_with_cells)
    # plt.show()
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
    print('len bbtp: ', len(bounding_boxes_to_predict))
    print('len bbtp[10]: ', len(bounding_boxes_to_predict[10]))
    '''x_avg, y_avg, w_avg, h_avg = bounding_boxes_to_predict[10][0],bounding_boxes_to_predict[10][1],bounding_boxes_to_predict[10][2],bounding_boxes_to_predict[10][3]
    for cell in bounding_boxes_to_predict:
        x, y, w, h = cell[0], cell[1], cell[2], cell[3]
        if h+5<h_avg:
            bounding_boxes_to_predict.remove(cell)'''
    # plt.figure(num=None, figsize=(5, 5), dpi=80, facecolor='w', edgecolor='k')
    # plt.imshow(image_with_cells_to_predict)
    # plt.show()
    counter = 0
    img_arr = [[], [], [], [], [], [], []]
    for i in range(len(bounding_boxes_to_predict)):
        x, y, w, h = bounding_boxes_to_predict[i][0], bounding_boxes_to_predict[i][1], bounding_boxes_to_predict[i][2], \
                     bounding_boxes_to_predict[i][3]
        img_arr[counter % 7].append(image[y - 1:y + h + 1, x - 1:x + w + 1])
        counter += 1
    return bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, img_arr

def run(pdf_filename):

    # ### заполнение списков пдф из пути(path надо задавать самому) (первый пункт тз)

    # In[3]:


    path = cfg.INPUT_PDFS_DIR
    list_of_elements, specification, other = search_pdf_in_folder(path)

    # ### разделение пдф на изображения (второй пункт тз)

    # In[4]:


    for path in list_of_elements:
        img_list_of_elems = break_up_pdf_to_array_png(path, 200)
    for path in specification:
        img_specification = break_up_pdf_to_array_png(path, 200)
    '''for image in img_specification:
        plt.figure(num=None, figsize=(30, 30), dpi=80, facecolor='w', edgecolor='k')
        plt.imshow(image)
        plt.show()
    for image in list_of_elements:
        plt.figure(num=None, figsize=(30, 30), dpi=80, facecolor='w', edgecolor='k')
        plt.imshow(image)
        plt.show()'''

    # ### распознавание линий (третий пункт тз)

    # In[5]:


    # pyt.pytesseract.tesseract_cmd = cfg.PYTESSERACT_CMD

    # In[22]:


    img_matrix = []
    unrecognized_list = []
    '''for path in list_of_elements:
        try:
            print(path)
            img_list_of_elems = break_up_pdf_to_array_png(path, 200)
            for img in img_list_of_elems:
                im = []
                image, merge_line, merge_line_cut = find_lines_tz(img)
                bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, img_arr = find_cells_tz(merge_line, image, merge_line_cut)
                for i in range(len(img_arr[0])):
                    for j in range(len(img_arr)-1, -1, -1):
                        d = []
                        ver = []
                        data = pyt.image_to_data(img_arr[j][i], lang='rus+eng', output_type = 'dict')
                        text = pyt.image_to_string(img_arr[j][i], lang='rus+eng', config='--psm 4')
                        plt.figure(num=None, figsize=(2, 2), dpi=80, facecolor='w', edgecolor='k')
                        plt.imshow(img_arr[j][i])
                        plt.show()
                        for v in data['conf']:
                            if v != '-1':
                                ver.append(float(v))
                        print(text)
                        print(np.mean(ver))
                        print('================================')
                        if text[:-1]:
                            d.append(text[:-1])
                            d.append(np.mean(ver))
                            im.append(d)
                img_matrix.append(im)
        except Exception:
            unrecognized_list.append(path)'''
    for path in specification:
        #    try:
        img_specification = break_up_pdf_to_array_png(path, 200)
        for img in img_specification:
            im = []
            image, merge_line, merge_line_cut = find_lines_tz(img)
            bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, img_arr = find_cells_tz(merge_line, image,
                                                                                                          merge_line_cut)
            for i in range(len(img_arr[0])):
                for j in range(len(img_arr) - 1, -1, -1):
                    d = []
                    ver = []
                    cnt = 1
                    data = pyt.image_to_data(img_arr[j][i], lang='rus+eng', output_type='dict')
                    text = pyt.image_to_string(img_arr[j][i], lang='rus+eng', config='--psm 4')
                    # plt.figure(num=None, figsize=(2, 2), dpi=80, facecolor='w', edgecolor='k')
                    # plt.imshow(img_arr[j][i])
                    # plt.show()
                    # for v in data['conf']:
                    # if v != '-1':
                    # ver.append(float(v))
                    print(text)
                    print(np.mean(ver))
                    print('================================')
                    if text[:-1]:
                        print(text)
                        d.append(text[:-1])
                        # d.append(np.mean(ver))
                    else:
                        d.append(' ')
                    im.append(d)
            img_matrix.append(im)
    #    except Exception:
    #        unrecognized_list.append(path)
    #        print('Документ ', path, ' Не распознан')


    # In[7]:

    fin = datetime.datetime.now()
    print(fin - start)

    print(unrecognized_list)

    # In[23]:


    print(img_matrix[0])

    # In[24]:


    df = []
    df_tmp = []
    c = 1
    for d in img_matrix[0]:
        if c == 7:
            df.append(df_tmp)
            df_tmp = []
        else:
            df_tmp.append(d)
            c += 1

    # In[25]:


    df = pd.DataFrame(df)
    print(df)

    # In[29]:


    data = img_matrix[0]
    w = len(data) / 7
    data = np.resize(data, (int(w), 7))

    # In[30]:


    data = pd.DataFrame(data)
    print(data)

    # In[31]:


    data.to_excel('./data_810.xlsx')

    # In[11]:




    path_to_json = "ekb.json"
    elements, dictionary = read_json_file(path_to_json)

    # In[12]:


    elems = []
    for elem in img_matrix[0]:
        elems.append(elem[0])

    # In[13]:


    elems

    # In[14]:


    create_report(elems, elements, dictionary)

    # In[ ]:




