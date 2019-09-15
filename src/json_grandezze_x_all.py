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
list_files = [
    f for f in listdir(path_acc_data_json)
    if isfile(join(path_acc_data_json, f))
]

path_acc_data_json_grandezze_basics = path_acc_data + "/json_grandezze_basics/grandezze_x_basics/"
path_acc_data_json_grandezze_firstmax = path_acc_data + "/json_grandezze_firstmax/grandezze_x_firstmax/"
path_acc_data_json_grandezze_secondmin = path_acc_data + "/json_grandezze_second_min/grandezze_x_second_min/"
path_acc_data_json_grandezze_secondmax = path_acc_data + "/json_grandezze_secondmax/grandezze_x_secondmax/"


# Carico in values_to_skip il numero di valori da saltare per ogni tipello
values_to_skip = []

with open(path_acc_data + "/utility/Escludere_Pre_Custom12.csv",
          "r") as file_utility:
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

def find_first_massimo_locale(tempi):
    return _find_first_massimo(tempi, 5)

def parse_file():
    omino = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))
        minimi_array_index = []
        minimi_array = []
        massimi_array = []
        massimi_array_b = []
        massimi_array_fma = []
        massimi_array_smi = []
        massimi_array_sma = []
        with open(path_acc_data_json + file, "r") as file_acc:
            json_object = json.load(file_acc)

            tempi = json_object["tempi"]

            steps = []
            gfxs = []

            start_keep = False
            for tempo in tempi:
                step = int(tempo["step"])
                gfx = float(tempo["gFx"])

                start_keep = start_keep or (step > values_to_skip[omino])

                if start_keep:
                    steps.append(step)
                    gfxs.append(gfx)

            # Una volta creati gli arrays escludiamo n minimi
            latest_min_ind = 0
            for x in range(0, json_object["pre"]):
                index_minimo = find_first_minimo(gfxs)
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
                else:
                    break

            # Adesso conto solamente n minimi dopo quello che ho trovato
            index_precedente = 0
            index_last_minimo = 0
            for x in range(0, json_object["into"]):
                index_last_minimo += find_first_minimo(gfxs[index_last_minimo:])
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
                if index_last_minimo < 0:
                    break


            # Possiamo trovare i massimi come STANDARD
            for x in range(0, len(minimi_array_index) - 2):
                massimo = 0
                
                array_in_campione = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]
                massimo = find_first_minimo_locale(array_in_campione)
                
                massimi_array.append(tempi[steps[minimi_array_index[x]]:][massimo])

            # Possiamo trovare i massimi come BASICS
            for x in range(0, len(minimi_array_index) - 2):
                massimo = 0

                for j in range(minimi_array_index[x], minimi_array_index[x+1]):

                    array_in_barone = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]
                    massimo = find_first_massimo_locale(array_in_barone)
                
                massimi_array_b.append(tempi[steps[minimi_array_index[x]]:][massimo])

            # Possiamo trovare i massimi come FIRSTMAX
            for x in range(0, len(minimi_array_index) - 2):
                loc_min = 0
                massimo = 0
               
                array_in_campione = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]
                loc_min = find_first_minimo_locale(array_in_campione)
                array_in_barone = gfxs[minimi_array_index[x]+loc_min:minimi_array_index[x+1]]
                massimo = find_first_massimo_locale(array_in_barone)
                
                massimi_array_fma.append(tempi[steps[minimi_array_index[x]]:][massimo])

            # Possiamo trovare i massimi come SECONDMIN
            for x in range(0, len(minimi_array_index) - 2):
                massimo = 0
                loc_min = 0
                
                array_in_campione = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]
                
                loc_min = find_first_minimo_locale(array_in_campione)
                array_in_barone = gfxs[minimi_array_index[x]+loc_min:minimi_array_index[x+1]]
                massimo = find_first_minimo_locale(array_in_barone)
                    
                massimi_array_smi.append(tempi[steps[minimi_array_index[x]]:][massimo])

            # Possiamo trovare i massimi come SECONDMAX
            for x in range(0, len(minimi_array_index) - 2):
                loc_min = 0
                second_loc_min = 0
                massimo = 0
               
                array_in_campione = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]
                loc_min = find_first_minimo_locale(array_in_campione)
                array_in_barone = gfxs[minimi_array_index[x]+loc_min:minimi_array_index[x+1]]
                second_loc_min = find_first_minimo_locale(array_in_barone)
                array_in_prova = gfxs[minimi_array_index[x]+second_loc_min:minimi_array_index[x+1]]
                massimo = find_first_massimo_locale(array_in_prova)
                
                massimi_array_sma.append(tempi[steps[minimi_array_index[x]]:][massimo])
        

        # CALCOLO GRANDEZZE ALL

        # STD
        tempo_contatto = 0
        for x in range(0, len(minimi_array_index) - 2):
            tempo_contatto += massimi_array[x]["time"] - minimi_array[x]["time"]
        tempo_contatto /= len(massimi_array)

        # BASICS
        tempo_contatto_b = 0
        for x in range(0, len(minimi_array_index) - 2):
            tempo_contatto_b += massimi_array_b[x]["time"] - minimi_array[x]["time"]
        tempo_contatto_b /= len(massimi_array_b)

        # FIRSTMAX
        tempo_contatto_fma = 0
        for x in range(0, len(massimi_array_fma) - 2):
            tempo_contatto_fma += massimi_array_fma[x]["time"] - minimi_array[x]["time"]
        tempo_contatto_fma /= len(massimi_array_fma)

        # SECONDMIN
        tempo_contatto_smi = 0
        for x in range(0, len(minimi_array_index) - 2):
            tempo_contatto_smi += massimi_array_smi[x]["time"] - minimi_array[x]["time"]
        tempo_contatto_smi /= len(massimi_array_smi)

        # SECONDMAX
        tempo_contatto_sma = 0
        for x in range(0, len(massimi_array_sma) - 2):
            tempo_contatto_sma += massimi_array_sma[x]["time"] - minimi_array[x]["time"]
        tempo_contatto_sma /= len(massimi_array_sma)

        print(colored("Tempo di contatto_STD: {}".format(tempo_contatto), "yellow"))
        print(colored("Tempo di contatto_B: {}".format(tempo_contatto_b), "yellow"))
        print(colored("Tempo di contatto_FMA: {}".format(tempo_contatto_fma), "yellow"))
        print(colored("Tempo di contatto_SMI: {}".format(tempo_contatto_smi), "yellow"))
        print(colored("Tempo di contatto_SMA: {}".format(tempo_contatto_sma), "yellow"))

        # STANDARD
        tempo_volo = 0
        for x in range(1, len(minimi_array_index) - 1):
            tempo_volo += minimi_array[x]["time"] - massimi_array[x-1]["time"]
        tempo_volo /= len(massimi_array)

        # BASICS
        tempo_volo_b = 0
        for x in range(1, len(minimi_array_index) - 1):
            tempo_volo_b += minimi_array[x]["time"] - massimi_array_b[x-1]["time"]
        tempo_volo_b /= len(massimi_array_b)

        # FIRSTMAX
        tempo_volo_fma = 0
        for x in range(1, len(massimi_array_fma) - 2):
            tempo_volo_fma += minimi_array[x]["time"] - massimi_array_fma[x-1]["time"]
        tempo_volo_fma /= len(massimi_array_fma)

        # SECONDMIN
        tempo_volo_smi = 0
        for x in range(1, len(minimi_array_index) - 1):
            tempo_volo_smi += minimi_array[x]["time"] - massimi_array_smi[x-1]["time"]

        tempo_volo_smi /= len(massimi_array_smi)

        # SECONDMAX
        tempo_volo_sma = 0
        for x in range(1, len(massimi_array_sma) - 2):
            tempo_volo_sma += minimi_array[x]["time"] - massimi_array_sma[x-1]["time"]
        tempo_volo_sma /= len(massimi_array_sma)

        print(colored("Tempo di volo_STD: {}".format(tempo_volo), "yellow"))
        print(colored("Tempo di volo_B: {}".format(tempo_volo_b), "yellow"))
        print(colored("Tempo di volo_FMA: {}".format(tempo_volo_fma), "yellow"))
        print(colored("Tempo di volo_SMI: {}".format(tempo_volo_smi), "yellow"))
        print(colored("Tempo di volo_SMA: {}".format(tempo_volo_sma), "yellow"))        

        tempo_totale = minimi_array[len(minimi_array) - 1]["time"] - minimi_array[0]["time"]
        ritmo = len(minimi_array) / tempo_totale

        print(colored("Tempo di totale: {}".format(tempo_totale), "yellow"))
        print(colored("Ritmo: {}".format(ritmo), "yellow"))

        jsello = {}
        jsello["minimi"] = minimi_array
        jsello["massimi"] = massimi_array
        jsello["tempo_contatto"] = tempo_contatto
        jsello["tempo_volo"] = tempo_volo
        jsello["tempo_totale"] = tempo_totale
        jsello["ritmo"] = ritmo

        with open(path_acc_data_json_grandezze + file, "w") as file_grandezze:
            json.dump(jsello, file_grandezze)
        
        jsello_b = {}
        jsello_b["minimi"] = minimi_array
        jsello_b["massimi"] = massimi_array_b
        jsello_b["tempo_contatto"] = tempo_contatto_b
        jsello_b["tempo_volo"] = tempo_volo_b
        jsello_b["tempo_totale"] = tempo_totale
        jsello_b["ritmo"] = ritmo

        with open(path_acc_data_json_grandezze_basics + file, "w") as file_grandezze_b:
            json.dump(jsello_b, file_grandezze_b)

        jsello_fma = {}
        jsello_fma["minimi"] = minimi_array
        jsello_fma["massimi"] = massimi_array_fma
        jsello_fma["tempo_contatto"] = tempo_contatto_fma
        jsello_fma["tempo_volo"] = tempo_volo_fma
        jsello_fma["tempo_totale"] = tempo_totale
        jsello_fma["ritmo"] = ritmo

        with open(path_acc_data_json_grandezze_firstmax + file, "w") as file_grandezze_fma:
            json.dump(jsello_fma, file_grandezze_fma)

        jsello_smi = {}
        jsello_smi["minimi"] = minimi_array
        jsello_smi["massimi"] = massimi_array_smi
        jsello_smi["tempo_contatto"] = tempo_contatto_smi
        jsello_smi["tempo_volo"] = tempo_volo_smi
        jsello_smi["tempo_totale"] = tempo_totale
        jsello_smi["ritmo"] = ritmo

        with open(path_acc_data_json_grandezze_secondmin + file, "w") as file_grandezze_smi:
            json.dump(jsello_smi, file_grandezze_smi)

        jsello_sma = {}
        jsello_sma["minimi"] = minimi_array
        jsello_sma["massimi"] = massimi_array_sma
        jsello_sma["tempo_contatto"] = tempo_contatto_sma
        jsello_sma["tempo_volo"] = tempo_volo_sma 
        jsello_sma["tempo_totale"] = tempo_totale
        jsello_sma["ritmo"] = ritmo

        with open(path_acc_data_json_grandezze_secondmax + file, "w") as file_grandezze_sma:
            json.dump(jsello_sma, file_grandezze_sma)

        print(colored("End processing " + file, "red"))
        omino += 1



if __name__ == "__main__":
    parse_file()