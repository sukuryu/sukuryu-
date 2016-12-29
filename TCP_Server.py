import socket
import threading

class TCP_Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.pitch = 0
        self.roll = 0
        self.yaw = 0

    def create_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(1)

    def get_loop(self, client_socket):
        bufsize = 514
        while True:
            self.yaw = int.from_bytes(client_socket.recv(bufsize), "big")

    def get_loop_2(self, client_socket):
        bufsize = 514
        while True:
            quaternion = str.from_bytes(client_socket.recv(bufsize), "big")
            #stringを3つのintに変換
            data_list = quaternion.split(",")
            self.pitch = int(data_list[0])
            self.roll = int(data_list[1])
            self.yaw = int(data_list[2])

    def accept_and_start(self, mode):
        self.clientsock, client_address = self.serversocket.accept()

        send_data = b"s"

        print("接続完了")
        self.clientsock.sendall(send_data)

        if mode == "elev0":
            client_handler = threading.Thread(target=self.get_loop, args=(self.clientsock,))
            client_handler.start()
        elif mode == "all_elev":
            client_handler = threading.Thread(target=self.get_loop_2, args=(self.clientsock,))
            client_handler.start()


    def get_yaw(self):
        return self.yaw

    def get_quaternion(self):
        return self.pitch, self.roll, self.yaw

    def socket_close(self):
        self.serversocket.close()
        self.clientsock.close()
