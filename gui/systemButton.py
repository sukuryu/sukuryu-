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

        #スタートボタン
        startButton = QPushButton("スタート", self.parent)
        startButton.setGeometry(size.width() / 18 * 15,
                                size.height() / 15,
                                size.width() / 18 * 2,
                                size.height() / 18 * 2)
        startButton.clicked.connect(self.startFunc)



    def startFunc(self):
        print("start")
