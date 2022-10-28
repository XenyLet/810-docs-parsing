import re
import numpy as np
from pathlib import Path
from pdf2image import convert_from_path
from easy_way.deskew_img import deskew_img


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

def split_pdf_to_pages_images(path_to_pdf, _type):
    if _type not in ["specification", "list_of_elements"]:
        _type = "other"

    if _type == "list_of_elements":
        pages = break_up_pdf_to_array_png(path_to_pdf, 200)
        deskewed_imgs = []
        for i, img in enumerate(pages):
            if i == 0:
                page_type = "elements_list_page_1"
            else:
                page_type = "elements_list_other_pages"
            deskewed_imgs.append(deskew_img(img, page_type))

        return deskewed_imgs

    elif _type =="specification":
        pages = break_up_pdf_to_array_png(path_to_pdf, 200)
        deskewed_imgs = [deskew_img(image, "specification") for image in pages]

        return deskewed_imgs

    else:
        raise NotImplementedError

