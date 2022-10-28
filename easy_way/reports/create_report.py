import os.path
import re
import json
import xlsxwriter
from config import path_to_database_json

pattern_cap_1 = re.compile('[0-9]*[.,]?[0-9]+.В')
pattern_cap_2 = re.compile('±\d{1,}')
pattern_cap_3 = re.compile('[0-9]*[.,]?[0-9]+..Ф')

pattern_res_1 = re.compile('[0-9]*[.,]?[0-9]+..Ом')
pattern_res_2 = re.compile('±\d{1,}%')
pattern_res_3_1 = re.compile('-[0-9]*[.,]?[0-9]+-')
pattern_res_3_2 = re.compile('[0-9]*[.,]?[0-9]+Вт')

pattern_ind_1 = re.compile('[0-9]*[.,]?[0-9]+[мнп]?Гн')
pattern_ind_2 = re.compile('±\d{1,}')

def capacitors(perech):
    print('Конденсатор', perech, 'имеет следующие характеристики:')
    print('Номинальное напряжение:', re.search(pattern_cap_1, perech))
    print('Номинальная ёмкость:', re.search(pattern_cap_3, perech))
    print('Допуск: ', re.search(pattern_cap_2, perech), str('%'), sep='')

def resistors(perech):
    print('Резистор:', perech, 'имеет следующие характеристики:')
    print('Номинальное сопротивление:', re.search(pattern_res_1, perech))
    if '-' in perech:
        print('Номинальная мощность рассеяния: ', re.search(pattern_res_3_1, perech)[1:-1], 'Вт', sep='')
    else:
        print('Номинальная мощность рассеяния:', re.search(pattern_res_3_2, perech))
    print('Допуск:', re.search(pattern_res_2, perech))

def inductor(perech):
    print('Катушка индуктивности', perech, 'имеет следующие характеристики:')
    print('Индуктивность катушки:', re.search(pattern_ind_1, perech))
    print('Допуск: ', re.search(pattern_ind_2, perech)[0], str('%'), sep='')

def create_json_db(path_to_json):
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



def create_report(recognitions):
    # print('Список файлов, в которых распознавание не удалось: ', unrecognized_list)
    elements, dictionary = create_json_db(path_to_database_json)
    for _, text, _, _ in recognitions:
        describe_element(text,
                         (elements, dictionary)
                         )

def create_report_xlsx(recognitions, tgt_dir):
    for section, data in recognitions.items():
        workbook = xlsxwriter.Workbook(f"{tgt_dir}/{section}.xlsx")
        for f_path, recognitions_per_pdf in data.items():
            w_sheet_name, _ = os.path.splitext(os.path.basename(f_path))
            worksheet = workbook.add_worksheet(
                name=w_sheet_name
            )
            maxlen_per_col = [0]*4
            for i, row in enumerate(recognitions_per_pdf):
                for j, col in enumerate(row):
                    text = col[1]
                    worksheet.write(i, j, text)
                    maxlen_per_col[j] = max(maxlen_per_col[j], len(text))
            for col_num in range(4):
                worksheet.set_column(col_num, col_num, maxlen_per_col[col_num]+2)
        workbook.close()



def describe_element(text, json_db):
    (elements, dictionary) = json_db

    key_dict = max([element for element in elements if element in text], key=len)
    if key_dict != '':
        charachters = dictionary[key_dict]
        if 'КИВ' in text:
            inductor(text)
            print('\n')
        elif text[0] == 'Р' or text[0] == 'P':
            resistors(text)
            print('\n')
        elif text[0] == 'К' or text[0] == 'K':
            capacitors(text)
            print('\n')
        else:
            print('Элемент', text, 'есть в БД, но пока характеристики не распознаны. \n')
    else:
        print('Элемент:', text,  'не распознан')

