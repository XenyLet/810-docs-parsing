import re

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


def create_report(perechni, elements, dictionary):
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
            print('Элемент:', perech, 'не распознан')


if __name__ == '__main__':
    elements, dictionary = read_json_file(path_to_json)
    create_report(elems, elements, dictionary)