import wave
import pyaudio

hrtf_L = {}
hrtf_R = {}

#--------------L_Load-----------------------------------
for i in range(72):
    str_i = str(i * 5)

    if len(str_i) < 2:
        str_i = "00" + str_i
    elif len(str_i) < 3:
        str_i = "0" + str_i

    filename = "L0e" + str_i + "a.dat"
    filepath = "../hrtfs/elev0/" + filename
    test = open(filepath, "r").read().split("\n")

    data = []

    for item in test:
        if item != '':
            data.append(float(item))

    hrtf_L[i] = data

#---------------R_Load----------------------------
for i in range(72):
    str_i = str(i * 5)

    if len(str_i) < 2:
        str_i = "00" + str_i
    elif len(str_i) < 3:
        str_i = "0" + str_i

    filename = "R0e" + str_i + "a.dat"
    filepath = "../hrtfs/elev0/" + filename
    test = open(filepath, "r").read().split("\n")

    data = []

    for item in test:
        if item != '':
            data.append(float(item))

    hrtf_R[i] = data

#------------変数------------------------
sound_data_path = "./test.wav"

def play():
    wf = wave.open(sound_data_path, "r")


    p = pyaudio.PyAudio()

    stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    chunk = 512

    data = wf.readframes(chunk)

    print(p.get_format_from_width(wf.getsampwidth()))

    while data != b'':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.close()
    p.terminate

play()




#--------------------------

#--------------L_Load-----------------------------------
for i in range(72):
    str_i = str(i * 5)

    if len(str_i) < 2:
        str_i = "00" + str_i
    elif len(str_i) < 3:
        str_i = "0" + str_i

    filename = "L0e" + str_i + "a.dat"
    filepath = "../hrtfs/elev0/" + filename
    test = open(filepath, "r").read().split("\n")

    data = []

    for item in test:
        if item != '':
            data.append(float(item))

    hrtf_L[i] = data

#---------------R_Load----------------------------
for i in range(72):
    str_i = str(i * 5)

    if len(str_i) < 2:
        str_i = "00" + str_i
    elif len(str_i) < 3:
        str_i = "0" + str_i

    filename = "R0e" + str_i + "a.dat"
    filepath = "../hrtfs/elev0/" + filename
    test = open(filepath, "r").read().split("\n")

    data = []

    for item in test:
        if item != '':
            data.append(float(item))

    hrtf_R[i] = data

#hrtf_data = hrtf_R[0]

#-----------------処理-------------------
