from socket import socket
import json
import lesson_3.chat_warehous.common as common


class Server:
    def __init__(self, address=common.Constants.DEFAULT_IP_ADDRESS, port=common.Constants.DEFAULT_PORT,
                 proto = common.Constants.DEFAULT_PROTO, soc_type=common.Constants.DEFAULT_TYPE):
        self.socket = socket(soc_type, proto)
        self.socket.bind((address, port))
        self.socket.listen(common.Constants.MAX_CONNECTIONS)

    def Run(self):
        while 1:
            client, client_address = self.socket.accept()
            print(f'\nПодключился клиент: {client_address}')
            try:
                messages_from_client = common.get_messages(client)
                print(f'Сообщение от клиента: {messages_from_client}')
                response = common.handler_client_messages(messages_from_client)
                common.send_mesages(client, response)
            except (ValueError, json.JSONDecodeError):
                print('Принято некорретное сообщение от клиента.')
            client.close()