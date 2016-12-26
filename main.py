import numpy
import scipy.io.wavfile as wave
import pyaudio
import load_hrtf

#水平面のデータのみロード
load = load_hrtf.load_hrtf()
elev0Hrtf_L, elev0Hrtf_R = load.load_elev0hrtf()

sound_data_path = "./test.wav"
N = 512
CHANNELS = 2
position = 36
FFT_size = 1024
M = 513
overLap = 511

count = 0
move_count = 0

def convolutionL(data):
    #与えられたデータに窓をかける
    #window = numpy.hanning(N)
    #dt = data * window

    #fft
    spectrum = numpy.fft.fft(data, n = FFT_size)

    #---------hrtfを足し合わせる--------------------

    hrtf_fft = numpy.fft.fft(hrtf_L[position], n = FFT_size)
    #print(hrtf_fft)
    result = spectrum * hrtf_fft

    #ifft
    ret_dt = numpy.fft.ifft(result, n = N)

    return ret_dt.real

def convolutionR(data):
    #与えられたデータに窓をかける
    #window = numpy.hanning(N)
    #dt = data * window

    #fft
    spectrum = numpy.fft.fft(data, n = FFT_size)

    #---------hrtfを足し合わせる--------------------

    hrtf_fft = numpy.fft.fft(hrtf_R[position], n = FFT_size)
    #print(hrtf_fft)
    result = spectrum * hrtf_fft

    #ifft
    ret_dt = numpy.fft.ifft(result, n = N)

    return ret_dt.real

def play(sound_data):
    p = pyaudio.PyAudio()
    stream = p.open(format = 8,
                    channels = CHANNELS,
                    rate = rate,
                    output = True)

    index = 0

    #while(sound_data[index:, 0].size > N):
    #    stream.write(bytes(sound_data[index:index + N]))
    #    index += N

    stream.write(sound_data)

    stream.close()
    p.terminate()

rate, data = scw.read(sound_data_path)

L_data = data[:, 0]
R_data = data[:, 1]

ret_data_L = numpy.zeros(L_data.size)
ret_data_R = numpy.zeros(R_data.size)

index = 0

while(ret_data_L[index:].size > N):
    ret_data_L[index:index + N] += convolutionL(L_data[index:index + N])
    ret_data_R[index:index + N] += convolutionR(R_data[index:index + N])
    index += 1

result_data = numpy.empty((0, 2), numpy.int16)

for i in range(L_data.size):
    result_data = numpy.append(result_data, numpy.array([[int(ret_data_L[i]), int(ret_data_R[i])]]).astype(numpy.int16), axis=0)

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
#rate = int(rate * 1.2)
play(result_data)