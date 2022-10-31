from process_dir import process_dir
from easy_way.reports.create_report import create_report_xlsx
from config import path_to_pdf_dir
from logg import get_logger

def main():
    logger = get_logger('main')
    recognitions = process_dir(path_to_pdf_dir)

    # found_recognitions = {}
    # for section, pdfs_in_section in recognitions.items():
    #     found_recognitions[section] = {}
    #     for pdf_path, recognitions_per_pdf in pdfs_in_section.items():
    #         found_recognitions[section][pdf_path] = recognitions_search(recognitions_per_pdf)

    create_report_xlsx(recognitions, ".")
    

if __name__ == '__main__':
    main()

