from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Dialog(QDialog):
    def __init__(self, parent = None, flag = None):
        self.parent = parent
        super().__init__(parent)

        if flag == 1:
            self.initUI1()
        elif flag == 2:
            self.initUI2()
        elif flag == 3:
            self.initUI3()

    def initUI1(self):
        self.setWindowTitle("警告")

        #ラベル
        label = QLabel(self)
        label.setText("再生中または接続がありません")
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.close)
        okButton.move(self.parent.windowSize.width() / 24, self.parent.windowSize.height() / 50)

        self.resize(self.parent.windowSize.width() / 6, self.parent.windowSize.height() / 15)
        center = QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        self.show()

    def initUI2(self):
        self.setWindowTitle("警告")

        #ラベル
        label = QLabel(self)
        label.setText("再生中に押してください")
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.close)
        okButton.move(self.parent.windowSize.width() / 24, self.parent.windowSize.height() / 50)

        self.resize(self.parent.windowSize.width() / 6, self.parent.windowSize.height() / 15)
        center = QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        self.show()

    def initUI3(self):
        self.setWindowTitle("警告")

        #ラベル
        label = QLabel(self)
        label.setText("再生中または接続がありません")
        label.adjustSize()
        okButton = QPushButton("OK", self)
        okButton.clicked.connect(self.close)
        okButton.move(self.parent.windowSize.width() / 24, self.parent.windowSize.height() / 50)

        self.resize(self.parent.windowSize.width() / 6, self.parent.windowSize.height() / 15)
        center = QDesktopWidget().availableGeometry().center()
        frame = self.frameGeometry()
        frame.moveCenter(center)
        self.move(frame.topLeft())
        self.show()
