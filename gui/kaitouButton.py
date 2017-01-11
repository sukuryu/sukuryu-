from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy
import math
import sys

class kaitouButton(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        size = self.parent.windowSize

        for i in range(12):
            button = QPushButton(str(i), self.parent)
            button.setObjectName(str(i))
            button.setGeometry(size.width() / 4 + size.height() * 2 / 5 * numpy.cos(math.pi / 2 + math.pi / 6 * i),
                            size.height() / 2 - 50 - size.height() * 2 / 5 * numpy.sin(math.pi / 2 + math.pi / 6 * i),
                            size.width() / 15,
                            size.height() / 15)

            button.clicked.connect(self.button_event)

    def button_event(self):
        self.parent.stop_flag = True
        sender = self.sender()
        print(sender.objectName())
