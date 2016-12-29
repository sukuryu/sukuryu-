import numpy

#hrtfをロード
class load_hrtf:

    def __init__(self):
        #0°のhrtf
        self.elev0Hrtf_L = {}
        self.elev0Hrtf_R = {}

    #水平面のhrtfをロード
    def load_elev0hrtf(self):
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

            self.elev0Hrtf_L[i] = data

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

            self.elev0Hrtf_R[i] = data

        return self.elev0Hrtf_L, self.elev0Hrtf_R

    #全方向のhrtfをロード
    def load_all_hrtfs(self):

        #全方位のhrtf
        allHrtf_L = {}
        allHrtf_R = {}

        #ディクショナリの中に入れるhrtfディクショナリ
        hrtfs_L = {}
        hrtfs_R = {}

        #elev0からelev90まで読み込み
        for elev in range(19):
            tmp_filePath = "../hrtfs/elev" + str(elev * 5) + "/"

            #90°の時のみデータが左右一つづつなので処理を分ける
            if elev * 5 == 90:
                filename = "L" + str(elev * 5) + "e000a.dat"
                filepath = tmp_filePath + filename

                test = open(filepath, "r").read().split("\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                hrtfs_L[0] = data

                filename = "R" + str(elev * 5) + "e000a.dat"
                filepath = tmp_filePath + filename

                test = open(filepath, "r").read().split("\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                hrtfs_R[0] = data

                allHrtf_L[elev] = hrtfs_L
                allHrtf_R[elev] = hrtfs_R

                continue

            #指定elevのｈｒｔｆ_Lを取得
            for i in range(72):
                str_i = str(i * 5)

                if len(str_i) < 2:
                    str_i = "00" + str_i
                elif len(str_i) < 3:
                    str_i = "0" + str_i

                filename = "L" + str(elev * 5) + "e" + str_i + "a.dat"
                filepath = tmp_filePath + filename

                test = open(filepath, "r").read().split("\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                hrtfs_L[i] = data

            #指定elevのｈｒｔｆ_Rを取得
            for i in range(72):
                str_i = str(i * 5)

                if len(str_i) < 2:
                    str_i = "00" + str_i
                elif len(str_i) < 3:
                    str_i = "0" + str_i

                filename = "R" + str(elev * 5) + "e" + str_i + "a.dat"
                filepath = tmp_filePath + filename

                test = open(filepath, "r").read().split("\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                hrtfs_R[i] = data

            allHrtf_L[elev] = hrtfs_L
            allHrtf_R[elev] = hrtfs_R

            #hrtfsディクショナリを初期化
            hrtfs_L = {}
            hrtfs_R = {}

        #0°から-45°まで読み込み
        for elev in range(9):
            tmp_filePath = "../hrtfs/elev" + str(-((elev + 1) * 5)) + "/"

            #指定elevのｈｒｔｆ_Lを取得
            for i in range(72):
                str_i = str(i * 5)

                if len(str_i) < 2:
                    str_i = "00" + str_i
                elif len(str_i) < 3:
                    str_i = "0" + str_i

                filename = "L" + str(-((elev + 1) * 5)) + "e" + str_i + "a.dat"
                filepath = tmp_filePath + filename

                test = open(filepath, "r").read().split("\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                hrtfs_L[i] = data

            #指定elevのｈｒｔｆ_Rを取得
            for i in range(72):
                str_i = str(i * 5)

                if len(str_i) < 2:
                    str_i = "00" + str_i
                elif len(str_i) < 3:
                    str_i = "0" + str_i

                filename = "R" + str(-((elev + 1) * 5)) + "e" + str_i + "a.dat"
                filepath = tmp_filePath + filename

                test = open(filepath, "r").read().split("\n")

                data = []

                for item in test:
                    if item != '':
                        data.append(float(item))

                hrtfs_R[i] = data

            allHrtf_L[-(elev + 1)] = hrtfs_L
            allHrtf_R[-(elev + 1)] = hrtfs_R

            #hrtfsディクショナリを初期化
            hrtfs_L = {}
            hrtfs_R = {}

        return allHrtf_L, allHrtf_R
