import numpy as np
from pdf2image import convert_from_path


def split_pdf_to_images(path_to_pdf, dpi):
    array_png = []
    pages = convert_from_path(path_to_pdf, dpi,
                              #poppler_path=cfg.POPPLER_PATH
                              )
    for page, i in zip(pages, range(len(pages))):
        pix = np.array(page)
        array_png.append(pix[30:-30, 30:-30])
    return array_png


def padding(img_to_predict):
    l = max(img_to_predict.shape)
    # itog_l = l + (28 - l%28)
    im_bg = np.ones((l, l))
    im_bg = im_bg * 255
    im_bg[:img_to_predict.shape[0], :img_to_predict.shape[1]] = img_to_predict
    return im_bg
