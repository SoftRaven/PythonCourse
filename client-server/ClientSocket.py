import re
import socket
import threading
import json


class ClientSocket(socket.socket):
    def __init__(self, port=12345):
        super().__init__()
        self.host = socket.gethostname()
        self.server = (self.host, port)  # Данные сервера
        self.alias = ""

    def run(self):
        print("Chat is opened!")
        self.connect(self.server)
        self.set_username()
        print("start sending")
        self.send(self.alias.encode('utf-8'))
        print("end sending")
        thread = threading.Thread(target=self.read_socket)
        thread.start()
        self.choose_sending_method()

    def set_username(self):
        print('Введите ваше имя:')
        self.alias = str(input())

    def choose_sending_method(self):
        print('Выберите способ отправки')
        print('1 - всем')
        print('2 - конкретному пользователю')
        option = int(input())
        self.enter_message(option)

    def enter_message(self, choice):
        if choice == 1:
            while 1:
                message = input('Ваше сообщение:')
                reply = {'name': None, 'message': message}
                reply_json = json.dumps(reply)
                self.send(reply_json.encode('utf-8'))
        elif choice == 2:
            while 1:
                print('Введите имя получателя:')
                receiver = str(input())
                message = input('Ваше сообщение:')
                reply = {'name': receiver, 'message': message}
                reply_json = json.dumps(reply)
                self.send(reply_json.encode('utf-8'))

    def read_socket(self):
        while 1:
            data = self.recv(1024).decode('utf-8')
            result = re.split(r':', data)
            user = result[0]
            message = result[1]
            print(user + ":" + message)


def main():
    client = ClientSocket()
    client.run()


if __name__ == '__main__':
    main()
