from socket import socket
import json
import lesson_3.chat_warehous.common as common

class Client:
    def __init__(self,address = common.Constants.DEFAULT_IP_ADDRESS, port=common.Constants.DEFAULT_PORT,
                 proto = common.Constants.DEFAULT_PROTO, soc_type=common.Constants.DEFAULT_TYPE):
        self.socket = socket(soc_type,proto)
        self.socket.connect((address, port))

    def Exchange(self, to_server):
        common.send_mesages(self.socket, to_server)
        print(f'На сервер отправлено сообщение :{to_server}')
        try:
            message = common.get_messages(self.socket)
            print(f'От сервера получено сообщение:{message}')
            response = common.handler_response_from_server(message)
            print(response)
        except (ValueError, json.JSONDecodeError):
            print('Не удалось декодировать сообщение сервера.')

    def Greetings(self):
        self.Exchange( common.create_greetings())