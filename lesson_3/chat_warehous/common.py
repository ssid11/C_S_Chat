from socket import socket, AF_INET, SOCK_STREAM
import json
import time
from select import select

def get_messages(client):
    recv_lst = list()
    send_lst = list()
    err_lst = list()
    recv_lst, send_lst, err_lst = select([client], [client],
                                         [], 0)
    if recv_lst:
        try:
            encoded_response = client.recv(Constants.MAX_PACKAGE_SIZE)
        except:
            return
        # encoded_response = client.recv(Constants.MAX_PACKAGE_SIZE)
        if isinstance(encoded_response, bytes):
            decode_response = encoded_response.decode(Constants.ENCODING)
            response = json.loads(decode_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError

def send_mesages(sock, messages):
    json_messages = json.dumps(messages)
    encoded_messages = json_messages.encode(Constants.ENCODING)
    sock.send(encoded_messages)

def handler_client_messages(messages):
    if not Constants.ACTION in messages or not Constants.TIME in messages or not Constants.USER in messages:
        print('Обработка сообщения. Неверный формат запроса.')
        # return {Constants.RESPONSE: 400, Constants.ERROR: 'Bad Request'}
        return create_message(response=400, error = 'Bad Request')
    if messages[Constants.ACTION] == Constants.GREETINGS:
        print('Обработка сообщения. Все в порядке')
        return create_message(response=200)
    if  messages[Constants.ACTION] == 'broadcast':
        print('Обработка широковещания')




def create_greetings(account_name='Guest'):
    return {Constants.ACTION: Constants.GREETINGS, Constants.TIME: time.time(), Constants.USER: {
        Constants.ACCOUNT_NAME: account_name}}

def handler_response_from_server(message):
    if Constants.RESPONSE in message:
        if message[Constants.RESPONSE] == 200:
            return 'Код ответа:200 - "ОК"'
        return f'Код ответа:400 : {message[Constants.ERROR]}'

def create_message(**kwargs):
    message = {}
    for el in kwargs.keys():
        message[el] = kwargs[el]
        message['time']=time.time()
    return message




class Constants:
    DEFAULT_PORT = 7777
    DEFAULT_PROTO = SOCK_STREAM
    DEFAULT_TYPE = AF_INET
    DEFAULT_IP_ADDRESS = '127.0.0.1'
    MAX_CONNECTIONS = 5
    MAX_PACKAGE_SIZE = 1024
    ENCODING = 'UTF-8'
    ACTION = 'action'
    TIME = 'time'
    USER = 'user'
    ACCOUNT_NAME = 'account_name'
    GREETINGS = 'presence'
    RESPONSE = 'response'
    ERROR = 'error'
    VALID_ACTIONS = ['presence','prоbe', 'msg', 'quit', 'authenticate', 'join', 'leave', 'broadcast']
