import argparse
import sys
import logging

from chat_warehous.server import Server
import log.server_log_config
from log.server_log_config import logger


parser = argparse.ArgumentParser()
parser.add_argument('-a',dest='a', default='127.0.0.1')
parser.add_argument('-p', '--port', dest='p', default=7777, type=int)
args = parser.parse_args()
logger = logging.getLogger('server')
if not args.p in range(1025,65556):
    logger.log(logging.ERROR,'Значение прослушиваемого порта должны быть между 1024 и 65555')
    sys.exit(1)
try:
    server = Server(address=args.a, port=args.p)
    logger.log(logging.INFO, f'Запущенн чат-сервер. Слушает адрес {args.a} на порту {args.p}.')
    server.Run()
except Exception as e:
    logger.log(logging.CRITICAL,str(e))

