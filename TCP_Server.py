import socket
import threading

class TCP_Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.yaw = 0

    def create_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(1)

    def get_roop(self, client_socket):
        bufsize = 514
        while True:
            self.yaw = int.from_bytes(client_socket.recv(bufsize), "big")

    def accept_and_start(self):
        self.clientsock, client_address = self.serversocket.accept()

        send_data = b"s"

        print("接続完了")
        self.clientsock.sendall(send_data)

        client_handler = threading.Thread(target=self.get_roop, args=(self.clientsock,))
        client_handler.start()

    def get_yaw(self):
        return self.yaw

    def socket_close(self):
        self.serversocket.close()
        self.clientsock.close()
