import numpy
import load_hrtf
import pyaudio
import TCP_Server
import threading
import math

class overlap_add:

    def __init__(self, fft_size = 1024, cut_size = 513, ovarLap = 511, parent = None):
        self.index = 0
        self.fft_size = fft_size
        self.cut_size = cut_size
        self.overLap = ovarLap
        self.history_L = numpy.zeros(self.overLap, dtype = numpy.float64)
        self.history_R = numpy.zeros(self.overLap, dtype = numpy.float64)
        self.parent = parent
        #スレッドが動作しているかの判定
        self.threadActiveFlag = False

    def convolution(self, data, hrtf):
        self.spectrum = numpy.fft.fft(data, n = self.fft_size)
        self.hrtf_fft = numpy.fft.fft(hrtf, n = self.fft_size)
        self.add = self.spectrum * self.hrtf_fft
        self.result = numpy.fft.ifft(self.add, n = self.fft_size)
        self.return_data = self.result.real * self.volume
        return self.return_data[:self.cut_size], self.return_data[self.cut_size:]

    #水平面のみ
    def play_loop_elev0(self):
        self.threadActiveFlag = True

        while True:
            #gui処理
            if self.parent.stop_flag == True:
                print("break")
                break

            result_data = numpy.empty((0, 2), dtype=numpy.int16)
            receive_data = self.serverObj.get_yaw()

            if receive_data == 0 or receive_data > 72:
                continue

            #このマイナス1はいずれ消す
            receive_data -= 1

            if receive_data == 0:
                pass

            receive_data = receive_data + self.init_position

            if receive_data < 72 and receive_data >= 0:
                receive_data = 71 - receive_data
            else:
                receive_data = 142 - receive_data
                print(receive_data)

            tmp_conv_L, add_L = self.convolution(self.sound_data[self.index:self.index + self.cut_size, 0], self.hrtfL[receive_data])
            tmp_conv_R, add_R = self.convolution(self.sound_data[self.index:self.index + self.cut_size, 1], self.hrtfR[receive_data])

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

        self.threadActiveFlag = False

    #全方向再生処理
    def play_loop_allElev(self):
        self.threadActiveFlag = True

        while True:
            #gui処理
            if self.parent.stop_flag == True:
                print("break")
                break

            result_data = numpy.empty((0, 2), dtype=numpy.int16)
            datalist = self.serverObj.get_pitch_etc()

            if datalist == [] or len(datalist) != 3 or type(datalist[0]) != float:
                continue

            #受信データから行列作成
            R = numpy.array([[numpy.cos(datalist[1]) * numpy.cos(datalist[2]),
                             -numpy.cos(datalist[1]) * numpy.sin(datalist[2]),
                             numpy.sin(datalist[1])],
                            [numpy.sin(datalist[0]) * numpy.sin(datalist[1]) * numpy.cos(datalist[2]) + numpy.cos(datalist[0]) * numpy.sin(datalist[2]),
                             -numpy.sin(datalist[0]) * numpy.sin(datalist[1]) * numpy.sin(datalist[2]) + numpy.cos(datalist[0]) * numpy.cos(datalist[2]),
                             -numpy.sin(datalist[0]) * numpy.cos(datalist[1])],
                            [-numpy.cos(datalist[0]) * numpy.sin(datalist[1]) * numpy.cos(datalist[2]) + numpy.sin(datalist[0]) * numpy.sin(datalist[2]),
                             numpy.cos(datalist[0]) * numpy.sin(datalist[1]) * numpy.sin(datalist[2]) + numpy.sin(datalist[0]) * numpy.cos(datalist[2]),
                             numpy.cos(datalist[0]) * numpy.sin(datalist[1])]])

            init_position = numpy.array(self.init_position_3d)

            #内積
            current_coordinates = numpy.dot(R, init_position)

            #r = numpy.sqrt(current_coordinates[0] ** 2 + current_coordinates[1] ** 2 + current_coordinates[2] ** 2)
            θ = (numpy.arccos(current_coordinates[2] / numpy.sqrt(current_coordinates[0] ** 2 + current_coordinates[1] ** 2 + current_coordinates[2] ** 2))) * 180 / math.pi
            if current_coordinates[1] < 0:
                φ = (-numpy.arccos(current_coordinates[0] / numpy.sqrt(current_coordinates[0] ** 2 + current_coordinates[1] ** 2))) * 180 / math.pi
            else:
                φ = (numpy.arccos(current_coordinates[0] / numpy.sqrt(current_coordinates[0] ** 2 + current_coordinates[1] ** 2))) * 180 / math.pi

            if φ < 0:
                φ = 360 + φ

            #φを0-71、θを0-27に変換
            φ = round(φ / 5)
            θ = round(θ / 5)

            if φ == 72:
                φ = 0
            if θ > 27:
                θ = 27

            if φ == 0:
                pass
            else:
                φ = 72 - φ

            #畳込みと再生
            tmp_conv_L, add_L = self.convolution(self.sound_data[self.index:self.index + self.cut_size, 0], self.hrtfL[θ][φ])
            tmp_conv_R, add_R = self.convolution(self.sound_data[self.index:self.index + self.cut_size, 0], self.hrtfR[θ][φ])

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

        print("end")
        self.threadActiveFlag = False

    def start(self, serverObj, hrtfL, hrtfR, streamObj, mode, sound_data, init_position = 0, init_position_3d = [1, 0, 0], volume = 1):
        self.serverObj = serverObj
        self.hrtfL = hrtfL
        self.hrtfR = hrtfR
        self.streamObj = streamObj
        self.volume = volume
        self.init_position = init_position
        self.init_position_3d = init_position_3d
        self.sound_data = sound_data

        #サーバーとクライアントの接続確認
        #self.serverObj.create_server()
        #self.serverObj.accept_and_start(mode=mode)

        if mode == "elev0":
            #水平のみの処理
            self.play_handler = threading.Thread(target=self.play_loop_elev0)
            self.play_handler.start()

        elif mode == "all_elev":
            #3次元空間の処理
            self.play_handler_allElev = threading.Thread(target=self.play_loop_allElev)
            self.play_handler_allElev.start()

        else:
            print("モード指定が正しくありません")

    def stop(self):
        self.streamObj.close()

    def is_active(self):
        return self.threadActiveFlag
