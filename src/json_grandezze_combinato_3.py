# grandezze_x sono io che cerco di usare il secondo sistema di ricerca dei massimi per confrontare quale sia il migliore
# MASSIMO = minimo locale tra i due minimi
import json
import plotly.graph_objects as go
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from termcolor import colored

os.system('color')

path_acc_data = "E:/Scuola/Università/Tesi/Python/data/acc"
path_acc_data_json = path_acc_data + "/json/"
path_acc_data_json_grandezze = path_acc_data + "/json_grandezze/grandezze_x/"
path_data_comb = path_acc_data + "/json_combinato_3/"
path_output = path_acc_data + "/json_grandezze_combinato_3/"
list_files = [
    f for f in listdir(path_acc_data_json)
    if isfile(join(path_acc_data_json, f))
]

# Carico in values_to_skip il numero di valori da saltare per ogni tipello
values_to_skip = []

with open(path_acc_data + "/utility/Escludere_Pre_Custom12.csv","r") as file_utility:
    for line in file_utility:
        values_to_skip.append(int(line.replace("\n", "")))

def is_val_min(val_to_check, test_values):
    for value in test_values:
        if val_to_check >= value:
            return False
    return True

def is_val_max(val_to_check, test_values):
    for value in test_values:
        if val_to_check <= value:
            return False
    return True


# Funzione ignoranta per trovare il primo minimo
def _find_first_minimo(tempi, accuracy):
    accuracy_half = int(accuracy / 2)
    for x in range(accuracy_half, len(tempi) - accuracy_half):
        test_values = []
        for j in range(accuracy_half, 0, -1):
            test_values.append(tempi[x - j])
        for j in range(1, accuracy_half + 1):
            test_values.append(tempi[x + j])

        val_to_check = tempi[x]

        if is_val_min(val_to_check, test_values):
            return x
    return -1

def find_first_minimo(tempi):
    return _find_first_minimo(tempi, 27)

def find_first_minimo_locale(tempi):
    return _find_first_minimo(tempi, 3)

# Funzione ignoranta per trovare il primo massimo
def _find_first_massimo(tempi, accuracy):
    accuracy_half = int(accuracy / 2)
    for x in range(accuracy_half, len(tempi) - accuracy_half):
        test_values = []
        for j in range(accuracy_half, 0, -1):
            test_values.append(tempi[x - j])
        for j in range(1, accuracy_half + 1):
            test_values.append(tempi[x + j])

        val_to_control = tempi[x]

        if is_val_max(val_to_control, test_values):
            # print("Trovato in {}".format(x))
            return x
    return -1

def find_first_massimo(tempi):
    return _find_first_massimo(tempi, 9)

def find_first_massimo_locale(tempi):
    return _find_first_massimo(tempi, 5)

def parse_file():
    omino = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))
        minimi_array_index = []
        minimi_array = []

        minimi_c_array = []
        massimi_c_array = []
        with open(path_acc_data_json + file, "r") as file_acc, open(path_data_comb + file, "r") as file_comb:
            json_object = json.load(file_acc)
            json_comb = json.load(file_comb)

            tempi = json_object["tempi"]
            tempi_c = json_comb["tempi"]

            steps = []
            gfxs = []
            gfcs = []

            start_keep = False
            for tempo in tempi:
                step = int(tempo["step"])
                gfx = float(tempo["gFx"])

                start_keep = start_keep or (step > values_to_skip[omino])

                if start_keep:
                    steps.append(step)
                    gfxs.append(gfx)

            start_keep = False
            for tempo in tempi_c:
                step = int(tempo["step"])
                gfc = float(tempo["gFc"])

                start_keep = start_keep or (step > values_to_skip[omino])

                if start_keep:
                    steps.append(step)
                    gfcs.append(gfc)

            # Una volta creati gli arrays escludiamo n minimi
            latest_min_ind = 0
            for x in range(0, json_object["pre"]):
                index_minimo = find_first_minimo(gfxs)
                for j in range (37, 27, -1):
                    if j % 2 == 0:
                        continue
                    if index_minimo - latest_min_ind < 15:
                        index_minimo = _find_first_minimo(gfxs, j)
                    else:
                        break
                for y in range (25, 9, -1):
                    if y % 2 == 0:
                        continue
                    if index_minimo - latest_min_ind > 30:
                        index_minimo = _find_first_minimo(gfxs, y)
                    else:
                        break
                latest_min_ind = index_minimo
                if index_minimo > 0:
                    steps = steps[index_minimo:]
                    gfxs = gfxs[index_minimo:]
                    gfcs = gfcs[index_minimo:]
                else:
                    break

            # Adesso conto solamente n minimi dopo quello che ho trovato
            index_precedente = 0
            index_last_minimo = 0
            for x in range(0, json_object["into"]):
                index_last_minimo += find_first_minimo(gfxs[index_last_minimo:])
                for j in range (39, 27, -1):
                    if j%2 == 0:
                        continue
                    if index_last_minimo - index_precedente < 17:
                        index_last_minimo = index_precedente + _find_first_minimo(gfxs[index_precedente:], j)
                    else:
                        break
                for y in range (25, 9, -1):
                    if y%2 == 0:
                        continue
                    if index_last_minimo - index_precedente > 30:
                        index_last_minimo = index_precedente + _find_first_minimo(gfxs[index_precedente:], y)
                    else:
                        break
                index_precedente = index_last_minimo
                minimi_array_index.append(index_last_minimo)
                minimi_array.append(tempi[steps[index_last_minimo] - 1])
                minimi_c_array.append(tempi_c[steps[index_last_minimo] - 1])
                if index_last_minimo < 0:
                    break

            # steps = steps[index_minimo:index_last_minimo]
            # gfcs = gfcs[index_minimo:index_last_minimo]


            # Possiamo trovare i massimi come punto più alto tra due minimi
            for j in range(0, len(minimi_array_index) - 2):
                massimo = 0
                array_in_campione = gfcs[minimi_array_index[j]:minimi_array_index[j+1]]
                massimo = find_first_massimo_locale(array_in_campione)
                i = 0
                if massimo == -1:
                    for n in range (0, len(array_in_campione) - 1):
                        val_att = array_in_campione[0]
                        if array_in_campione[n] > val_att:
                            massimo = n

                massimi_c_array.append(tempi_c[steps[minimi_array_index[x]]:][massimo])

        tempo_contatto = 0
        for x in range(0, len(minimi_array_index) - 2):
            # print("Differenza tra: {} e {} fa {}".format(massimi_array[x]["time"], minimi_array[x]["time"], massimi_array[x]["time"] - minimi_array[x]["time"]))
            tempo_contatto += massimi_c_array[x]["time"] - minimi_array[x]["time"]

        tempo_contatto /= len(massimi_c_array)

        print(colored("Tempo di contatto: {}".format(tempo_contatto), "yellow"))

        # print(colored("Calcolo tempo di volo", "green"))
        tempo_volo = 0
        for x in range(1, len(minimi_array_index) - 1):
            # print("Differenza tra: {} e {} fa {}".format(minimi_array[x]["time"], massimi_array[x-1]["time"], minimi_array[x]["time"] - massimi_array[x-1]["time"]))
            tempo_volo += minimi_array[x]["time"] - massimi_c_array[x-1]["time"]

        tempo_volo /= len(massimi_c_array)

        print(colored("Tempo di volo: {}".format(tempo_volo), "yellow"))

        # print(colored("Calcolo tempo totale e ritmo", "green"))
        tempo_totale = minimi_array[len(minimi_array) - 1]["time"] - minimi_array[0]["time"]
        ritmo = len(minimi_array) / tempo_totale

        print(colored("Tempo di totale: {}".format(tempo_totale), "yellow"))
        print(colored("Ritmo: {}".format(ritmo), "yellow"))

        print(colored("End processing " + file, "red"))

        jsello = {}
        jsello["minimi"] = minimi_array
        jsello["massimi"] = massimi_c_array
        jsello["tempo_contatto"] = tempo_contatto
        jsello["tempo_volo"] = tempo_volo
        jsello["tempo_totale"] = tempo_totale
        jsello["ritmo"] = ritmo

        with open(path_output + file, "w") as file_grandezze:
            json.dump(jsello, file_grandezze)

        omino += 1


if __name__ == "__main__":
    parse_file()