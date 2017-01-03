import socket
import threading
import quaternion
import re

class TCP_Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data_list = []
        self.yaw = 0

    def create_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(1)

    def accept_loop(self, client_socket):
        bufsize = 514
        while True:
            self.yaw = int.from_bytes(client_socket.recv(bufsize), "big")

    def accept_loop_2(self, client_socket):
        bufsize = 512
        while True:
            pitch_etc = client_socket.recv(bufsize).decode("ascii")
            self.data_list = pitch_etc.split(",")

            num_reg = re.compile("^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z")

            if len(self.data_list) != 3 or num_reg.match(self.data_list[0]) == False or num_reg.match(self.data_list[1]) == False or num_reg.match(self.data_list[2]) == False:
                continue

            for i in range(3):
                self.data_list[i] = float(self.data_list[i])

    def accept_and_start(self, mode):
        self.clientsock, client_address = self.serversocket.accept()

        send_data = b"s"

        print("接続完了")
        self.clientsock.sendall(send_data)

        if mode == "elev0":
            client_handler = threading.Thread(target=self.accept_loop, args=(self.clientsock,))
            client_handler.start()
        elif mode == "all_elev":
            #pitch_roll_yawかquaternionを使う
            client_handler = threading.Thread(target=self.accept_loop_2, args=(self.clientsock,))
            client_handler.start()

    def get_yaw(self):
        return self.yaw

    def get_pitch_etc(self):
        return self.data_list

    def socket_close(self):
        self.serversocket.close()
        self.clientsock.close()
