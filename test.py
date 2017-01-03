import load_hrtf
import overlap_add
import TCP_Server
import pyaudio
import scipy.io.wavfile as scw

sound_data_path = "./test.wav"
rate, sound_data = scw.read(sound_data_path)
port = 7000
mode = "all_elev"
init_position = 18
CHANNELS = 2
p = pyaudio.PyAudio()
stream = p.open(format = 8,
                channels = CHANNELS,
                rate = rate,
                output = True)

hrtf = load_hrtf.load_hrtf()
L, R = hrtf.load_elev0hrtf()

server = TCP_Server.TCP_Server("", port=port)

ob = overlap_add.overlap_add()
ob.start(serverObj=server,
         hrtfL=L,
         hrtfR=R,
         streamObj=stream,
         mode=mode,
         init_position=init_position,
         sound_data=sound_data)
