from process_dir import process_dir
from easy_way.reports.create_report import create_report
from config import path_to_pdf_dir

def main():
    elems, unrecognized_list = process_dir(path_to_pdf_dir)
    create_report(elems, unrecognized_list)

if __name__ == '__main__':
    main()

