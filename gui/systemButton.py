from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class systemButton(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        #parentから画面サイズ取得
        size = self.parent.windowSize

        #fontの設定
        font = QFont()
        #font.setFamily()
        font.setBold(True)
        font.setPointSize(32)

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
        connectButton = QPushButton("接続", self.parent)
        connectButton.setGeometry(size.width() / 18 * 15,
                                size.height() / 15 * 7,
                                size.width() / 18 * 2,
                                size.height() / 18 * 2)
        connectButton.setCheckable(True)
        connectButton.clicked[bool].connect(self.connect)

        #connectの状態ラベル
        statusLabel = QLabel("接続なし", self.parent)
        statusLabel.setGeometry(size.width() / 18 * 15,
                                size.height() / 15 * 9,
                                size.width() / 18 * 2,
                                size.height() / 18 * 2)
        statusLabel.setFont(font)




    def startFunc(self):
        print("start")

    def pushData(self):
        print("push")

    def connect(self, status):
        print("connet")
