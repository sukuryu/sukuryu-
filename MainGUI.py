from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
sys.path.append("gui/")
from kaitouButton import kaitouButton
from systemButton import systemButton


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        #windowSize取得
        self.windowSize = QDesktopWidget().availableGeometry().size()

        #回答ボタン初期化
        kaitouButton(self)

        #右側の画面初期化
        systemButton(self)

        #全画面表示
        self.resize(self.windowSize.width(), self.windowSize.height())
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
