import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from socket import socket
import json
import logging
from select import select

import log.server_log_config
from log.server_log_config import log
import common

logger = logging.getLogger('server')


class Server:

    __slots__ = ['clients_list', 'messages_list','socket']

    def __init__(self, address=common.Constants.DEFAULT_IP_ADDRESS, port=common.Constants.DEFAULT_PORT,
                 proto=common.Constants.DEFAULT_PROTO, soc_type=common.Constants.DEFAULT_TYPE):
        try:
            self.socket = socket(soc_type, proto)
            self.socket.bind((address, port))
            self.socket.listen(common.Constants.MAX_CONNECTIONS)
            self.socket.settimeout(0.5)
            self.clients_list = list()
            self.messages_list = list()
        except Exception as e:
            logger.log(logging.CRITICAL, str(e))
            sys.exit()

    def connect_search(self, to=0.5):
        try:
            self.socket.settimeout(to)
            client, client_address = self.socket.accept()
            logger.log(logging.INFO, f'Подключился клиент: {client_address}')
            self.clients_list.append(client)
        except Exception as e:
            pass

    @log
    def Run(self):
        try:
            while 1:
                self.connect_search()
                # try:
                #     messages_from_client = common.get_messages(client)
                #     logger.log(logging.INFO, f'Сообщение от клиента: {messages_from_client}')
                #     response = common.handler_client_messages(messages_from_client)
                #     common.send_mesages(client, response)
                #     logger.log(logging.INFO, f'Клиенту отправлен ответ: {response}.')
                # except (ValueError, json.JSONDecodeError):
                #     print('Принято некорретное сообщение от клиента.')
                #     logger.log(logging.ERROR, f'Принято некорретное сообщение от клиента.')

                recv_lst = list()
                send_lst = list()
                err_lst = list()
                try:
                    if self.clients_list:
                        recv_lst, send_lst, err_lst = select(self.clients_list, self.clients_list,
                                                             [], 0)
                except OSError:
                    pass

                if recv_lst:
                    for client_with_messages in recv_lst:
                        try:
                            messages_from_client = common.get_messages(client_with_messages)
                            logger.log(logging.INFO, f'Сообщение от клиента: {messages_from_client}')
                            response = common.handler_client_messages(messages_from_client)
                            common.send_mesages(client_with_messages, response)
                            logger.log(logging.INFO, f'Клиенту отправлен ответ: {response}.')
                            if messages_from_client['action'] == 'broadcast':
                                for cl in self.clients_list:
                                    common.send_mesages(cl,common.create_message(action='broadcast',
                                    msg='Disconnect', source = messages_from_client['user']['account_name']))
                        except:
                            logger.log(logging.INFO,f'Клиент {client_with_messages.getpeername()} '
                                     f'отключился от сервера.')
                            self.clients_list.remove(client_with_messages)

                # if self.messages_list and send_lst:
                #     message = {ACTION: MESSAGE, SENDER: messages_list[0][0],
                #                TIME: time.time(), MESSAGE_TEXT: messages_list[0][1]}
                #     del messages_list[0]
                #     for expect_client in send_lst:
                #         try:
                #             send_mesages(expect_client, message)
                #         except:
                #             log.info(f'Клиент {expect_client.getpeername()} отключился')
                #             clients_list.remove(expect_client)
        except Exception as e:
            logger.log(logging.WARNING, f"Завершена работа сервера. Причина: {str(e)}")


if __name__ == '__main__':
    s = Server()
    s.Run()
