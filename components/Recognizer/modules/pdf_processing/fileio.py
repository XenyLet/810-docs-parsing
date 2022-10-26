import json
import re
from pathlib import Path

# Функция для первого пункта(Производим поиск PDF документов в указанном каталоге и подкаталогах)
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


def read_json_file(path_to_json):
    with open(path_to_json, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    df = []
    for date in data:
        df += date['Children']
    dictionary = {}
    for x in df:
        dictionary[x[0]] = x[1]
    elements = dictionary.keys()
    return (elements, dictionary)