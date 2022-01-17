"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

word_lst = ['разработка','администритование','protocol', 'standard']
for el in word_lst:
    el_encode = el.encode()
    el_decode = el_encode.decode()
    print(f'Строка "{el}" после encode - {el_encode}, и decode - {el_decode}')