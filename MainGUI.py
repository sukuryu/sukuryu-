from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
sys.path.append("gui/")
from kaitouButton import kaitouButton
from systemButton import systemButton
import load_hrtf
import overlap_add
import TCP_Server
import pyaudio
import scipy.io.wavfile as scw

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        sound_data_path = "./test.wav"
        rate, self.sound_data = scw.read(sound_data_path)
        port = 7000
        self.mode = "all_elev"
        self.init_position = 18
        CHANNELS = 2
        p = pyaudio.PyAudio()
        self.stream = p.open(format = 8,
                        channels = CHANNELS,
                        rate = rate,
                        output = True)

        self.hrtf = load_hrtf.load_hrtf()
        self.L, self.R = self.hrtf.load_all_hrtfs()

        self.server = TCP_Server.TCP_Server("", port=port)
        #self.server.create_server()
        self.ob = overlap_add.overlap_add(parent=self)
        self.stop_flag = False

        self.initUI()

    def initUI(self):
        #windowSize取得
        self.windowSize = QDesktopWidget().availableGeometry().size()

        #fontの設定
        font = QFont()
        font.setBold(True)
        font.setPointSize(26)

        #回答ボタン初期化
        kaitouButton(self)

        #右側の画面初期化
        systemButton(self)

        #connectの状態ラベル
        self.statusLabel = QLabel("接続なし", self)
        self.statusLabel.setGeometry(self.windowSize.width() / 18 * 15,
                                self.windowSize.height() / 15 * 9,
                                self.windowSize.width() / 18 * 2,
                                self.windowSize.height() / 18 * 2)
        self.statusLabel.setFont(font)

        #全画面表示
        self.resize(self.windowSize.width(), self.windowSize.height())
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
