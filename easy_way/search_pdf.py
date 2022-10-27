import re
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
from config import path_poopler, path_to_pdf

#Функция для первого пункта(Производим поиск PDF документов в указанном каталоге и подкаталогах)
def search_pdf_in_folder(path):
    dir_path = Path(path)
    pdf_files = sorted(dir_path.rglob('*.pdf'))
    pdf_files = list(map(str, pdf_files))
    pattern_1 = re.compile('\.\d\d\d\П\Э\d.pdf')
    pattern_2 = re.compile('\.\d\d\d.pdf')
    list_of_elements = []
    specification = []
    other = []
    for file in pdf_files:
        if (re.findall(pattern_1, file)):
            list_of_elements.append(file)
        elif (re.findall(pattern_2, file)):
            specification.append(file)
        else:
            other.append(file)
    return list_of_elements, specification, other

#Функция для второго пункта(Разделяем документ на картинки, того же разрешения (dpi) что и исходный документ)
def break_up_pdf_to_array_png(path_to_pdf, dpi):
    array_png = []
    pages = convert_from_path(path_to_pdf, dpi,
                              # poppler_path=path_poopler
                              )
    for page, i in zip(pages, range(len(pages))):
        pix = np.array(page)
        array_png.append(pix[30:-30, 30:-30])
    return array_png

def create_list_of_pdf(path_to_create_list_pdf):

    list_of_elements, specification, other = search_pdf_in_folder(path_to_create_list_pdf)

    img_list_of_elems, img_specification = [], []
    for path in list_of_elements:
        img_list_of_elems = break_up_pdf_to_array_png(path, 200)
    for path in specification:
        img_specification = break_up_pdf_to_array_png(path, 200)
    return list_of_elements, specification, other, img_list_of_elems, img_specification

