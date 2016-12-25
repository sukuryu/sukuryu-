
import matplotlib.pyplot as plt
import numpy
import scipy.io.wavfile as scw
import pyaudio
import wave

hrtf_L = {}
hrtf_R = {}

sound_data_path = "./test.wav"
N = 512
CHANNELS = 2

def convolution(data):
    #与えられたデータに窓をかける
    #window = numpy.hanning(N)
    #dt = data * window

    #fft
    spectrum = numpy.fft.fft(data, n = N)

    #---------hrtfを足し合わせる--------------------

    #ifft
    ret_dt = numpy.fft.ifft(spectrum, n = N)

    return ret_dt.real

def play(sound_data):
    p = pyaudio.PyAudio()
    stream = p.open(format = 8,
                    channels = 2,
                    rate = rate,
                    output = True)

    index = 0

    while(sound_data[index:, 0].size > N):
        stream.write(bytes(sound_data[index:index + N]))
        index += N
        #byte_data = bytearray(data[index:index + N] )

    #stream.write(data)

    stream.close()
    p.terminate()

rate, data = scw.read(sound_data_path)

L_data = data[:, 0]
R_data = data[:, 1]

ret_data_L = numpy.zeros(L_data.size)
ret_data_R = numpy.zeros(R_data.size)

index = 0

while(ret_data_L[index:].size > N):
    ret_data_L[index:index + N] += convolution(L_data[index:index + N])
    ret_data_R[index:index + N] += convolution(R_data[index:index + N])
    index += N

result_data = numpy.empty((0, 2), int)

for i in range(L_data.size):
    result_data = numpy.append(result_data, numpy.array([[int(ret_data_L[i]), int(ret_data_R[i])]]), axis=0)

#波形をプロット
def create_plot(real_data, conv_data):
    plt.subplot(221)
    plt.plot(real_data[:, 0])

    plt.subplot(222)
    plt.plot(real_data[:, 1])

    plt.subplot(223)
    plt.plot(conv_data[:, 0])

    plt.subplot(224)
    plt.plot(conv_data[:, 1])

    plt.show()

#再生部分作成
play(result_data)

#print(result_data[500:600])
#print(data[500:600])
