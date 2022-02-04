import sys
import os
import traceback
import inspect
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

def log(func_to_log):
    def log_saver(*args, **kwargs):
        logger.debug(f'Была вызвана функция {func_to_log.__name__} c параметрами {args}, {kwargs}. '
                     f'Вызов из модуля {func_to_log.__module__}. Вызов из'
                     f' функции {traceback.format_stack()[0].strip().split()[-1]}.'
                     f'Вызов из функции {inspect.stack()[1][3]}')
        ret = func_to_log(*args, **kwargs)
        return ret
    return log_saver

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    logger.info('Тестовый запуск логирования')