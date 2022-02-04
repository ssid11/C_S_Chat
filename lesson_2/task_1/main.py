"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений или другого инструмента извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import os
import chardet
import csv

def get_data():
    param_lst = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    main_data = []
    main_data.append(param_lst)
    file_no = 1
    for file in list(filter(lambda x: x.endswith('.txt'), os.listdir(os.path.abspath('.')))):
        with open(os.path.join('.',file), mode='rb') as f:
            ret_dict = {}
            for line in f.readlines():
                result = chardet.detect(line)
                line = line.decode(result['encoding'])
                if len(line.split(':')) > 1 and line.split(':')[0] in param_lst :
                    ret_dict[line.split(':')[0]]=line.split(':')[1].strip()
        row =  [ret_dict[x] for x in param_lst]
        row.insert(0,file_no)
        main_data.append(row)
        file_no += 1
    return main_data

def write_to_csv(out_file):
    with open(out_file, mode='w', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for el in get_data():
            writer.writerow(el)

write_to_csv('my.csv')


