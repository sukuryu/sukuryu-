import socket
import threading
import re

class TCP_Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data_list = []
        self.yaw = 0

    def create_server(self, parent = None):
        self.parent = parent
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(1)

    def accept_loop(self):
        try:
            self.clientsock, client_address = self.serversocket.accept()
        except socket.timeout:
            print("timeout")
        self.clientsock.sendall(b"s")

        print("接続")
        self.parent.statusLabel.setText("接続中")
        self.parent.statusLabel.setStyleSheet("color: green")

        bufsize = 514
        while True:
            if self.stop_event.is_set() == True:
                break
            self.yaw = int.from_bytes(self.clientsock.recv(bufsize), "big")

    def accept_loop_2(self):
        try:
            self.clientsock, client_address = self.serversocket.accept()
        except socket.timeout:
            print("timeout")

        self.clientsock.sendall(b"s")

        print("接続")
        self.parent.statusLabel.setText("接続中")
        self.parent.statusLabel.setStyleSheet("color: green")

        bufsize = 512
        while True:
            if self.stop_event.is_set() == True:
                break
            pitch_etc = self.clientsock.recv(bufsize).decode("ascii")
            if pitch_etc == "o":
                self.socket_close()
                break
            self.data_list = pitch_etc.split(",")

            if len(self.data_list) != 3 or len(self.data_list[0]) > 15 or len(self.data_list[1]) > 15 or len(self.data_list[2]) > 15:
                continue

            for i in range(3):
                self.data_list[i] = float(self.data_list[i])

            #print(self.data_list[0])

    def accept_and_start(self, mode):

        self.stop_event = threading.Event()

        if mode == "elev0":
            self.client_handler = threading.Thread(target=self.accept_loop)
            self.client_handler.start()
        elif mode == "all_elev":
            #pitch_roll_yawかquaternionを使う
            self.client_handler = threading.Thread(target=self.accept_loop_2)
            self.client_handler.start()

    def get_yaw(self):
        return self.yaw

    def get_pitch_etc(self):
        return self.data_list

    def socket_close(self):
        self.stop_event.set()
        self.serversocket.close()
        self.clientsock.close()

    def time_out(self):
        self.stop_event.set()
        self.serversocket.close()

    def send_stop(self):
        self.clientsock.sendall(b"o")
