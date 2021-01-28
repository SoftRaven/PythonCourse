import json
import socket
import _thread as thread
import random
from datetime import datetime

random.seed(datetime.now())


class ServerSocket(socket.socket):
    def __init__(self, port=12345, buffer=1024):
        super().__init__()
       # self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.port = port
        self.hostname = socket.gethostname()
        self.buffer = buffer
        self.clients = {}
        self.bind(('', self.port))
        self.listen()

    def run(self):
        print("Chat Started!")
        try:
            self.accept_client()
        except Exception as ex:
            print(ex)
        finally:
            print("Server Closed")
            for client in self.clients:
                client.close()
            self.close()

    def accept_client(self):
        while 1:
            (clientSock, address) = self.accept()
            print("start recv")
            name = clientSock.recv(self.buffer)
            print("end recv")
            id = self.create_id()
            self.clients[id] = {'name': name.decode(), 'addr': clientSock}
            self.on_client_conect()
            thread.start_new_thread(self.recive, (id,))

    def create_id(self):
        not_found = True
        while not_found:
            rand_int = random.randint(100000, 999999)
            if rand_int not in self.clients:
                return rand_int

    def recive(self, id):
        print(self.clients)
        client = self.clients[id]['addr']
        while 1:
            data = client.recv(self.buffer)
            answer = json.loads(data.decode())
            if answer['message'] == 'exit':
                break
            receiver_name = answer['name']
            print(receiver_name)
            if receiver_name is None:
                self.on_message(client, data)
            else:
                isFound = False
                for value in self.clients.values():
                    if receiver_name == value['name']:
                        sendClient = value['addr']
                        sendClient.send(answer['message'].encode('utf-8'))
                        client.send(b'Message is sent')
                        isFound = True
                        break
                if not isFound:
                    client.send(b'User is offline')


        self.clients.pop(id)
        self.on_client_disconnect()
        client.close()
        thread.exit()

    def find_receiver(self):
        pass

    def broadcast(self, currentClient, message):
        for client in self.clients:
            if currentClient is not client['addr']:
                client['addr'].send(message)

    def on_client_conect(self):
        print('User enter to chat')

    def on_client_disconnect(self):
        print('User leaves chat')

    def on_message(self, client, data):
        self.broadcast(client, data.decode('utf-8'))


def main():
    server = ServerSocket()
    server.run()


if __name__ == '__main__':
    main()

#TODO обработать гонку потоков
