import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from socket import socket
import json
import logging

import log.server_log_config
from log.server_log_config import log
import common

logger = logging.getLogger('server')


class Server:
    def __init__(self, address=common.Constants.DEFAULT_IP_ADDRESS, port=common.Constants.DEFAULT_PORT,
                 proto=common.Constants.DEFAULT_PROTO, soc_type=common.Constants.DEFAULT_TYPE):
        try:
            self.socket = socket(soc_type, proto)
            self.socket.bind((address, port))
            self.socket.listen(common.Constants.MAX_CONNECTIONS)
        except Exception as e:
            logger.log(logging.CRITICAL, str(e))
            sys.exit()
    @log
    def Run(self):
        try:
            while 1:
                client, client_address = self.socket.accept()
                logger.log(logging.INFO, f'Подключился клиент: {client_address}')
                try:
                    messages_from_client = common.get_messages(client)
                    logger.log(logging.INFO, f'Сообщение от клиента: {messages_from_client}')
                    response = common.handler_client_messages(messages_from_client)
                    common.send_mesages(client, response)
                    logger.log(logging.INFO, f'Клиенту отправлен ответ: {response}.')
                except (ValueError, json.JSONDecodeError):
                    print('Принято некорретное сообщение от клиента.')
                    logger.log(logging.ERROR, f'Принято некорретное сообщение от клиента.')
                client.close()
        except Exception as e:
            logger.log(logging.WARNING, f"Завершена работа сервера. Причина: {str(e)}")


if __name__ == '__main__':
    s = Server()
    s.Run()
