import sys
import os
sys.path.insert(0,os.path.dirname(__file__))

import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('server')

formatter = logging.Formatter("%(asctime)s - %(levelname)10s - %(module)s - %(message)s ")

# Создаем файловый обработчик логирования (можно задать кодировку):
fh = TimedRotatingFileHandler("server.log", encoding='utf-8', when='D')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования')
