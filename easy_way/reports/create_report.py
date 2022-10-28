import re
import json
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



def create_report(perechni, unrecognized_list):
    print('Список файлов, в которых распознавание не удалось: ', unrecognized_list)
    elements, dictionary = read_json_file(path_to_database_json)
    for perech in perechni:
        key_dict = max([element for element in elements if element in perech], key=len)
        if key_dict != '':
            charachters = dictionary[key_dict]
            if 'КИВ' in perech:
                inductor(perech)
                print('\n')
            elif perech[0] == 'Р' or perech[0] == 'P':
                resistors(perech)
                print('\n')
            elif perech[0] == 'К' or perech[0] == 'K':
                capacitors(perech)
                print('\n')
            else:
                print('Элемент', perech, 'есть в БД, но пока характеристики не распознаны. \n')
        else:
            print('Элемент:', perech,  'не распознан')