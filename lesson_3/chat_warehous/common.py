from socket import socket, AF_INET, SOCK_STREAM
import json
import time

def get_messages(client):
    encoded_response = client.recv(Constants.MAX_PACKAGE_SIZE)
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
    if Constants.ACTION in messages and messages[
        Constants.ACTION] == Constants.GREETINGS and Constants.TIME in messages and\
        Constants.USER in messages and\
        messages[Constants.USER][Constants.ACCOUNT_NAME] == 'Guest':
        print('Обработка сообщения. Все в порядке')
        return {Constants.RESPONSE: 200}
    print('Обработка сообщения. Неверный формат запроса.')
    return {Constants.RESPONSE: 400, Constants.ERROR: 'Bad Request'}

def create_greetings(account_name='Guest'):
    return {Constants.ACTION: Constants.GREETINGS, Constants.TIME: time.time(), Constants.USER: {
        Constants.ACCOUNT_NAME: account_name}}

def handler_response_from_server(message):
    if Constants.RESPONSE in message:
        if message[Constants.RESPONSE] == 200:
            return 'Код ответа:200 - "ОК"'
        return f'Код ответа:400 : {message[Constants.ERROR]}'


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
    GREETINGS = 'presense'
    RESPONSE = 'response'
    ERROR = 'error'

