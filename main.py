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
position = 18
#2048
FFT_size = 2048
M = 1537
overLap = 511
write_size = 1026
volume = 2

index = 0
history_L = numpy.zeros(overLap, dtype = numpy.int16)
history_R = numpy.zeros(overLap, dtype = numpy.int16)

buf = numpy.empty((0, 2), dtype = numpy.int16)

rate, sound_data = scw.read(sound_data_path)

p = pyaudio.PyAudio()
stream = p.open(format = 8,
                channels = CHANNELS,
                rate = rate,
                output = True)

def convolution(data, hrtf):
    spectrum = numpy.fft.fft(data, n = FFT_size)
    hrtf_fft = numpy.fft.fft(hrtf, n = FFT_size)
    add = spectrum * hrtf_fft
    result = numpy.fft.ifft(add, n = M)
    return_data = result.real.astype(numpy.int16) * volume
    return return_data[:write_size], return_data[write_size:]

while(sound_data[index:, 0].size > M):
    result_data = numpy.empty((0, 2), dtype = numpy.int16)
    tmp_conv_L, add_L = convolution(sound_data[index:index + M, 0], elev0Hrtf_L[position])
    tmp_conv_R, add_R = convolution(sound_data[index:index + M, 1], elev0Hrtf_R[position])

    tmp_conv_L[:overLap] += history_L
    tmp_conv_R[:overLap] += history_R

    history_L = add_L
    history_R = add_R

    for i in range(tmp_conv_L.size):
        result_data = numpy.append(result_data, numpy.array([tmp_conv_L[i], tmp_conv_R[i]]))

    stream.write(bytes(result_data))
    index += write_size

stream.close()
p.terminate()
