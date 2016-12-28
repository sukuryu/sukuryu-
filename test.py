
import matplotlib.pyplot as plt
import numpy
import scipy.io.wavfile as scw
import pyaudio
import wave
import load_hrtf

load = load_hrtf.load_hrtf()
elev0Hrtf_L, elev0Hrtf_R = load.load_elev0hrtf()

sound_data_path = "./test.wav"
N = 512
CHANNELS = 2
position = 18
FFT_size = 2048
M = 1537
overLap = 511
write_size = 1026

count = 0

def convolutionL(data):
    #与えられたデータに窓をかける
    #window = numpy.hanning(N)
    #dt = data * window

    #fft
    spectrum = numpy.fft.fft(data, n = FFT_size)

    #---------hrtfを足し合わせる--------------------

    hrtf_fft = numpy.fft.fft(elev0Hrtf_L[position], n = FFT_size)
    #print(hrtf_fft)
    result = spectrum * hrtf_fft

    #ifft
    ret_dt = numpy.fft.ifft(result, n = M)

    return ret_dt.real

def convolutionR(data):
    #与えられたデータに窓をかける
    #window = numpy.hanning(N)
    #dt = data * window

    #fft
    spectrum = numpy.fft.fft(data, n = FFT_size)

    #---------hrtfを足し合わせる--------------------

    hrtf_fft = numpy.fft.fft(elev0Hrtf_R[position], n = FFT_size)
    #print(hrtf_fft)
    result = spectrum * hrtf_fft

    #ifft
    ret_dt = numpy.fft.ifft(result, n = M)

    return ret_dt.real

def play(sound_data):
    p = pyaudio.PyAudio()
    stream = p.open(format = 8,
                    channels = CHANNELS,
                    rate = rate,
                    output = True)

    #while(sound_data[index:, 0].size > N):
    #    stream.write(bytes(sound_data[index:index + N]))
    #    index += N

    stream.write(bytes(sound_data))

    stream.close()
    p.terminate()

rate, data = scw.read(sound_data_path)

L_data = data[:, 0]
R_data = data[:, 1]

ret_data_L = numpy.zeros(L_data.size)
ret_data_R = numpy.zeros(R_data.size)

index = 0

while(ret_data_L[index:].size > M):
    ret_data_L[index:index + M] += convolutionL(L_data[index:index + M])
    ret_data_R[index:index + M] += convolutionR(R_data[index:index + M])

    index += write_size

result_data = numpy.empty((0, 2), numpy.int16)

for i in range(L_data.size):
    result_data = numpy.append(result_data, numpy.array([[int(ret_data_L[i]), int(ret_data_R[i])]]).astype(numpy.int16), axis=0)


plt.plot(result_data[:, 0])
plt.show()
#再生部分作成
#rate = int(rate * 1.2)
play(result_data)
