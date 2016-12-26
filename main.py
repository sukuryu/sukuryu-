import numpy
import scipy.io.wavfile as wave
import pyaudio
import load_hrtf

#水平面のデータのみロード
load = load_hrtf.load_hrtf()
elev0Hrtf_L, elev0Hrtf_R = load.load_elev0hrtf()
