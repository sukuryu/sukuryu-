import numpy
import load_hrtf
import pyaudio
import TCP_Server
import threading

class overlap_add:

    def __init__(self, fft_size = 1024, cut_size = 513, ovarLap = 511):
        self.index = 0
        self.fft_size = fft_size
        self.cut_size = cut_size
        self.overLap = ovarLap
        self.history_L = numpy.zeros(self.overLap, dtype = numpy.float64)
        self.history_R = numpy.zeros(self.overLap, dtype = numpy.float64)

    def convolution(self, data, hrtf):
        self.spectrum = numpy.fft.fft(data, n = self.fft_size)
        self.hrtf_fft = numpy.fft.fft(hrtf, n = self.fft_size)
        self.add = self.spectrum * self.hrtf_fft
        self.result = numpy.fft.ifft(self.add, n = self.fft_size)
        self.return_data = self.result.real * self.volume
        return self.return_data[:self.cut_size], self.return_data[self.cut_size:]

    def play_loop_elev0(self):
        while True:
            result_data = numpy.empty((0, 2), dtype=numpy.int16)
            receive_data = self.serverObj.get_yaw()

            if receive_data == 0 or receive_data > 72:
                continue

            receive_data -= 1

            if receive_data == 0:
                pass
            else:
                receive_data = 72 - receive_data

            tmp_conv_L, add_L = self.convolution(self.sound_data[self.index:self.index + self.cut_size, 0], self.hrtfL[receive_data])
            tmp_conv_R, add_R = self.convolution(self.sound_data[self.index:self.index + self.cut_size, 0], self.hrtfR[receive_data])

            tmp_conv_L[:self.overLap] += self.history_L
            tmp_conv_R[:self.overLap] += self.history_R

            self.history_L = add_L
            self.history_R = add_R

            for i in range(tmp_conv_L.size):
                result_data = numpy.append(result_data, numpy.array([[int(tmp_conv_L[i]), int(tmp_conv_R[i])]], dtype=numpy.int16), axis=0)

            self.streamObj.write(bytes(result_data))
            self.index += self.cut_size

            if(self.sound_data[self.index:, 0].size < self.cut_size):
                self.index = 0

    def start(self, serverObj, hrtfL, hrtfR, streamObj, mode, sound_data, init_position = 0, volume = 1):
        self.serverObj = serverObj
        self.hrtfL = hrtfL
        self.hrtfR = hrtfR
        self.streamObj = streamObj
        self.volume = volume
        self.init_position = init_position
        self.sound_data = sound_data

        #サーバーとクライアントの接続確認
        self.serverObj.create_server()
        self.serverObj.accept_and_start(mode=mode)

        if mode == "elev0":
            #水平のみの処理
            self.play_handler = threading.Thread(target=self.play_loop_elev0)
            self.play_handler.start()

        elif mode == "all_elev":
            #3次元空間の処理
            self.play_handler_allElev = threading.Thread(target=self.play_loop)
            self.play_handler_allElev.start()

        else:
            print("モード指定が正しくありません")

    def stop(self, mode):
        if mode == "elev0":
            self.play_handler._stop()
        elif mode == "all_elev":
            self.play_handler_allElev._stop()
        else:
            print("再生中またはモード指定が正しくありません")
