import unittest
import json
import chat_warehous


class FakeSocket:

    def set_in_mess(self, in_mess):
        self.in_mess = json.dumps(in_mess).encode(chat_warehous.Constants.ENCODING)

    def recv(self, size):
        return self.in_mess

    def send(self, mess):
        self.out_mess = bytes(mess)


class MyTest(unittest.TestCase):

    def setUp(self):
        self.fake_socket = FakeSocket()
        self.test_data = {chat_warehous.Constants.ACTION: chat_warehous.Constants.GREETINGS,
                     chat_warehous.Constants.TIME: 111111.111111, chat_warehous.Constants.USER: {
                chat_warehous.Constants.ACCOUNT_NAME: 'test_guest'}}

    def test_get_messages(self):

        self.fake_socket.set_in_mess(self.test_data)
        self.assertEqual(chat_warehous.get_messages(self.fake_socket), self.test_data)

    def test_send_messages(self):
        chat_warehous.send_mesages(self.fake_socket, self.test_data)
        self.assertEqual(self.fake_socket.out_mess,
                         bytes(json.dumps(self.test_data).encode(chat_warehous.Constants.ENCODING)))

    def test_handler_client_messages_ok(self):
        self.assertEqual(chat_warehous.handler_client_messages({chat_warehous.Constants.ACTION: chat_warehous.Constants.GREETINGS,
                     chat_warehous.Constants.TIME: 111111.111111, chat_warehous.Constants.USER: {
                chat_warehous.Constants.ACCOUNT_NAME: 'Guest'}}),{chat_warehous.Constants.RESPONSE: 200})

    def test_handler_client_messages_bad(self):
        self.assertEqual(chat_warehous.handler_client_messages(self.test_data),
                         {chat_warehous.Constants.RESPONSE: 400, chat_warehous.Constants.ERROR: 'Bad Request'})

    def test_handler_response_from_server_ok(self):
        self.assertEqual(chat_warehous.handler_response_from_server({chat_warehous.Constants.RESPONSE: 200}),
                         'Код ответа:200 - "ОК"')

    def test_handler_response_from_server_bad(self):
        self.assertEqual(chat_warehous.handler_response_from_server({chat_warehous.Constants.RESPONSE: 400,
                        chat_warehous.Constants.ERROR: 'Bad Request'}),'Код ответа:400 : Bad Request')


unittest.main()
