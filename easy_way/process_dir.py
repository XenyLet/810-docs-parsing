from search_pdf import split_pdf_to_pages_images, search_pdf_in_folder
from easy_way.lines_and_cells.lines_and_cells import find_lines_tz, find_cells_tz

from easy_way.recognition.TextRecognizer import EasyOcrRecognizer

def process_page(page, text_recognizer, f_type):
    """
    # returns 2-d array of followin structure:
    [
        [(any_text_found, text, confidence, bounding_box), (...), ...],
        [...],
        ...
    ]

    Therefore recognitions represent table but in text form
    """
    def get_page_progress(total_cells_to_predict, cur_i, cur_j):
        cur_cell_n = cur_i * 4 + cur_j
        if round(cur_cell_n) % 10 == 0:
            print(f"Page progress: {cur_cell_n} / {total_cells_to_predict}")

    merge_line, merge_line_cut = find_lines_tz(page)
    bounding_boxes, image_name, longest_image, bounding_boxes_to_predict, cells_to_predict = find_cells_tz(
        merge_line, page, merge_line_cut)

    recognitions = []
    if not cells_to_predict:
        return recognitions

    recognitions_row = []
    cells_l = len(cells_to_predict) * len(cells_to_predict[0])
    for i, row in enumerate(cells_to_predict):
        for j, cell in enumerate(row):
            text, conf, bbox = text_recognizer.read_text(cell)
            any_text_found = text != ""
            recognition =(
                    any_text_found,
                    text,
                    conf,
                    bbox
                )

            recognitions_row.append(recognition)

            get_page_progress(cells_l, i, j)
        recognitions.append(recognitions_row)
        recognitions_row = []

    return recognitions


def process_dir(path_to_pdf_dir):
    text_recognizer = EasyOcrRecognizer(allow_list="""0123456789!"%'()+,-.:;<=>?«±µ»Ω
ABCDEFGHIJKLMNOPQRSTUVWXYZ
abcdefghijklmnopqrstuvwxyz
АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
абвгдежзиклмнопрстуфхцчшщъыьэюя""")

    print('recognizing')

    file_paths = search_pdf_in_folder(path_to_pdf_dir)
    list_of_elements, specification, other = file_paths

    pages_per_pdf = {
        "specification": {
            file_path: split_pdf_to_pages_images(path_to_pdf=file_path, _type="specification")
            for file_path in specification
        },
        "list_of_elements": {
            file_path: split_pdf_to_pages_images(path_to_pdf=file_path, _type="list_of_elements")
            for file_path in list_of_elements
        }
    }

    recognitions_per_pdf = {
        "specification": {},
        "list_of_elements": {}
    }

    for section in pages_per_pdf:
        for pdf_path, pages_from_pdf in pages_per_pdf[section].items():
            recognitions_per_pdf[section][pdf_path] = []
            for i, page in enumerate(pages_from_pdf):
                print(f"Starting page {i} / {len(pages_from_pdf)} recognition")
                recognitions = process_page(page, text_recognizer, section)

                recognitions_per_pdf[section][pdf_path].extend(recognitions)


    print(recognitions_per_pdf)
    return recognitions_per_pdf
