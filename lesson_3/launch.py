import subprocess
import os

process_list = list()

command = input('Очистить файлы логов (y/n): ')
if command.upper() == 'Y':
    try:
        os.remove('./server.log')
        os.remove('./client.log')
    except:
        pass

while True:
    command = input('Выберите действие: q - закрыть окна и выйти, '
                    's - запустить сервер, c - запустить клиента: ')
    if command.upper() == 'Q':
        while process_list:
            process_list.pop().kill()
        break
    elif command.upper() == 'S':
        process = subprocess.Popen('python server.py',
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
        process_list.append(process)
    elif command.upper() == 'C':
        process_list.append(subprocess.Popen('python client.py',
                                             creationflags=subprocess.CREATE_NEW_CONSOLE))
