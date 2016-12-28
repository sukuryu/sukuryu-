import numpy
import scipy.io.wavfile as scw
import pyaudio
import load_hrtf
import matplotlib.pyplot as plt

#水平面のデータのみロード
load = load_hrtf.load_hrtf()
elev0Hrtf_L, elev0Hrtf_R = load.load_elev0hrtf()

sound_data_path = "./test.wav"
N = 512
CHANNELS = 2
position = 45
#FFT2048
#FFT_size = 2048
#M = 1537
#overLap = 511

#FFT1024
FFT_size = 1024
M = 513
overLap = 511

volume = 3
index = 0
history_L = numpy.zeros(overLap, dtype = numpy.float64)
history_R = numpy.zeros(overLap, dtype = numpy.float64)

rate, sound_data = scw.read(sound_data_path)

p = pyaudio.PyAudio()
stream = p.open(format = 8,
                channels = CHANNELS,
                rate = rate,
                output = True)

buf = numpy.empty((0, 2), dtype = numpy.int16)

#-----------------------------------------------------------------

#畳み込み処理
def convolution(data, hrtf):
    spectrum = numpy.fft.fft(data, n = FFT_size)
    hrtf_fft = numpy.fft.fft(hrtf, n = FFT_size)
    add = spectrum * hrtf_fft
    result = numpy.fft.ifft(add, n = FFT_size)
    return_data = result.real * volume
    return return_data[:M], return_data[M:]

#リアルタイム処理部分
while(True):
    result_data = numpy.empty((0, 2), dtype = numpy.int16)
    tmp_conv_L, add_L = convolution(sound_data[index:index + M, 0], elev0Hrtf_L[position])
    tmp_conv_R, add_R = convolution(sound_data[index:index + M, 1], elev0Hrtf_R[position])

    tmp_conv_L[:overLap] += history_L
    tmp_conv_R[:overLap] += history_R

    history_L = add_L
    history_R = add_R

    for i in range(tmp_conv_L.size):
        result_data = numpy.append(result_data, numpy.array([[int(tmp_conv_L[i]), int(tmp_conv_R[i])]], dtype = numpy.int16), axis = 0)

    stream.write(bytes(result_data))
    index += M

    if(sound_data[index:, 0].size < M):
        index = 0

#ストリームを閉じる
stream.close()
p.terminate()
