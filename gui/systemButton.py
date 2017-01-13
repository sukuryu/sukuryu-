from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
sys.path.append("gui/")
from dialog import Dialog

class systemButton(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        #parentから画面サイズ取得
        size = self.parent.windowSize

        #スタートボタン
        startButton = QPushButton("スタート", self.parent)
        startButton.setGeometry(size.width() / 18 * 15,
                                size.height() / 15,
                                size.width() / 18 * 2,
                                size.height() / 18 * 2)
        startButton.clicked.connect(self.startFunc)

        #データ吐き出しボタン
        pushDataButton = QPushButton("データ出力", self.parent)
        pushDataButton.setGeometry(size.width() / 18 * 15,
                                size.height() / 15 * 13,
                                size.width() / 18 * 2,
                                size.height() / 18 * 2)
        pushDataButton.clicked.connect(self.pushData)

        #セーブするときの名前
        pushName = QLineEdit("", self.parent)
        pushName.setGeometry(size.width() / 18 * 13,
                            size.height() / 15 * 14,
                            size.width() / 18 * 2,
                            size.height() / 25 * 1)

        #socket待機ボタン(on-off)
        self.connectButton = QPushButton("接続", self.parent)
        self.connectButton.setGeometry(size.width() / 18 * 15,
                                    size.height() / 15 * 7,
                                    size.width() / 18 * 2,
                                    size.height() / 18 * 2)
        self.connectButton.setCheckable(True)
        self.connectButton.clicked[bool].connect(self.connect)
        #self.connectButton.setChecked(True)

    def startFunc(self):

        if self.parent.server.check_connection() == True and self.parent.ob.is_active() == False:
            self.parent.stop_flag = False
            self.parent.ob.start(serverObj=self.parent.server,
                                hrtfL=self.parent.L,
                                hrtfR=self.parent.R,
                                streamObj=self.parent.stream,
                                mode=self.parent.mode,
                                init_position=self.parent.init_position,
                                sound_data=self.parent.sound_data)
        else:
            Dialog(self.parent, 1)
            #QMessageBox.question(self, "再生中または接続がありません", QMessageBox.Yes, QMessageBox.Yes)


    def pushData(self):
        print("push")

    def connect(self, status):

        if status == True:
            self.parent.statusLabel.setStyleSheet("color: red")
            self.parent.statusLabel.setText("接続待機中")
            self.parent.server.create_server(self.parent)
            self.parent.server.accept_and_start(self.parent.mode)

        else:
            if self.parent.statusLabel.text() == "接続待機中":
                self.parent.statusLabel.setText("接続なし")
                self.parent.statusLabel.setStyleSheet("color: black")
                self.parent.server.time_out()
            else:
                self.parent.server.send_stop()
                self.parent.server.socket_close()
                self.parent.statusLabel.setText("接続なし")
                self.parent.statusLabel.setStyleSheet("color: black")
