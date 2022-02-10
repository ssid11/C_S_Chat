import sys
import os
sys.path.insert(0,os.path.dirname(__file__))
from socket import socket
import json
import logging

import log.client_log_config
from log.client_log_config import log
import common

logger = logging.getLogger('client')

class Client:

    __slots__ = ['socket']

    def __init__(self,address = common.Constants.DEFAULT_IP_ADDRESS, port=common.Constants.DEFAULT_PORT,
                 proto = common.Constants.DEFAULT_PROTO, soc_type=common.Constants.DEFAULT_TYPE):
        try:
            self.socket = socket(soc_type,proto)
            self.socket.settimeout(0.1)
            self.socket.connect((address, port))
        except Exception as e:
            logger.log(logging.CRITICAL, str(e))
            sys.exit()

    @log
    def exchange(self, to_server):
        common.send_mesages(self.socket, to_server)
        logger.log(logging.INFO, f'На сервер отправлено сообщение :{to_server}')
        try:
            message = common.get_messages(self.socket)
            logger.log(logging.INFO, f'От сервера получено сообщение:{message}')
            response = common.handler_response_from_server(message)
            logger.log(logging.INFO, f'Пришел ответ сервера:{response}')

        except (ValueError, json.JSONDecodeError):
            logger.log(logging.WARNING,'Не удалось декодировать сообщение сервера.')

    @log
    def greetings(self, name='Guest'):
        self.exchange( common.create_greetings(name))

    def stop(self):
        self.socket.close()

    def assemble_message(self, **kvargs):
        return common.create_message(**kvargs)

    def get_message(self):
        try:
            return common.get_messages(self.socket)
        except:
            pass
