from recognize import recognizing
from create_report import create_report
from config import path_to_pdf

def main():
    elems, unrecognized_list = recognizing(path_to_pdf)
    create_report(elems, unrecognized_list)

if __name__ == '__main__':
    main()

