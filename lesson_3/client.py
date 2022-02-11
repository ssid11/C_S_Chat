import argparse
import sys, os
import logging

from chat_warehous.client import Client
import log.client_log_config

logger = logging.getLogger('client')
parser = argparse.ArgumentParser()
parser.add_argument('-a','--address',dest='a', default='127.0.0.1')
parser.add_argument('-p', '--port', dest='p', default=7777, type=int)
args = parser.parse_args()
if not args.p in range(1025,65556):
    logger.log(logging.ERROR, 'Значение прослушиваемого порта должны быть между 1024 и 65555')
    sys.exit(1)

try:
    nik_name = input('Введите ваш ник:')
    client = Client(address=args.a, port=args.p)
    logger.log(logging.INFO, f'Запущенн чат-клиент. Адрес {args.a}, порт {args.p}.')
    client.greetings(nik_name)
except Exception as e:
    logger.log(logging.CRITICAL,str(e))

while 1:
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    try:
        print(client.get_message())
        resp = int(input(
"""Вы можете:
    0 - завершить программу
    1 - послать широковещательное сообщение
    Ваш выбор?(0):"""
        ))
    except:
        resp = 0
    if resp > 1 or resp < 0:
        continue
    if resp == 0:
        sys.exit(0)
    ms = client.assemble_message(action='broadcast', msg='Disconnect', user={'account_name':nik_name})
    client.exchange(ms)
client.stop()

