import socket
import threading

class TCP_Server:

    def __init__(self, host, ip):
        self.host = host
        self.ip = ip
        self.yaw = 1


    def create_server:
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((self.host, self.port))
        serversocket.listen(1)

    def get_roop(self, client_socket):
        bufsize = 1024
        while True:
            get_data = client_socket.recv(bufsize)
            print(get_data)


    def accept_and_start(self):
        clientsock, client_address = self.serversocket.accept()

        print("接続完了")

        client_handler = threading.Thread(target=get_roop, args=(clientsock,))
        client_handler.start()


test = TCP_Server(0.0.0.0, 8000)
test.create_server()
test.accept_and_start()
