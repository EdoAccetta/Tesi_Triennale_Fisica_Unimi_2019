# grandezze_trial sono io che cerco di creare un mix tra due sistemi di ricerca dei massimi per trovare una sintesi con grande fallimento
# MASSIMO = minimo locale centrale se trovo "dispari" minimi locali, massimo centrale se trovo "pari" minimi locali
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
path_acc_data_json_grandezze = path_acc_data + "/json_grandezze_trial/grandezze_x_trial/"
list_files = [
    f for f in listdir(path_acc_data_json)
    if isfile(join(path_acc_data_json, f))
]

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
            # print("Trovato in {}".format(x))
            return x
    return -1

def find_first_minimo(tempi):
    return _find_first_minimo(tempi, 27)

def find_first_minimo_locale(tempi):
    return _find_first_minimo(tempi, 5)

def parse_file():
    omino = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))
        minimi_array_index = []
        minimi_array = []
        massimi_array = []
        with open(path_acc_data_json + file, "r") as file_acc:
            json_object = json.load(file_acc)

            tempi = json_object["tempi"]

            steps = []
            gfxs = []

            start_keep = False
            for tempo in tempi:
                step = int(tempo["step"])
                gfx = float(tempo["gFx"])

                start_keep = start_keep or (step > values_to_skip[omino]
                                            and gfx < -3)

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

            # steps = steps[index_minimo:index_last_minimo]
            # gfxs = gfxs[index_minimo:index_last_minimo]

            # Possiamo trovare i massimi come punto più alto tra due minimi
            for x in range(0, len(minimi_array_index) - 2):
                massimo = 0
                index_massimo = 0
                # for j in range(minimi_array_index[x], minimi_array_index[x+1]):
                #     if(massimo < gfxs[j]):
                #         massimo = gfxs[j]
                #         index_massimo = j
                # massimi_array.append(tempi[steps[index_massimo] - 1])
                array_in_campione = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]

                conto = 0       # Con questa variabile vorrò contare quanti minimi locali ci sono tra due minimi assoluti
                local_min_steps = []     # Qui dentro metterò gli step relativi ai minimi locali
                array_in_barone = array_in_campione     # PROBABILMENTE NON SERVE E POTREI USARE DIRETTAMENTE ARRAY_IN CAMPIONE, MA VEDI RIGA 12
                last_position = 0
                check_value = 0
                while check_value >= 0:    # CICLO DA 0 ALLA FINE DI ARRAY_IN_BARONE (CHE CAMBIA OGNI CICLO)

                    check_value = find_first_minimo_locale(array_in_barone)      # OGNI VOLTA DEVO RIPARTIRE DAL MINIMO TROVATO
                    if check_value > 0: 
                        last_position += check_value
                        local_min_steps.append(last_position)     # Metto lo step del minimo locale trovato nel vettore local_min_steps
                        array_in_barone = array_in_campione[last_position:]
                        # print("check value {}".format(check_value))
                        # print("Primo punto array {}".format(minimi_array_index[0]))
                        # print("Last_min {}".format(check_value))
                        check_value = 0
                        conto += 1
                
                # print("Minimi trovati {}".format(conto))
                # Se non trovo minimi vado al prossimo
                if conto == 0:
                    continue

                if conto % 2 == 0:  # DATO CHE CONTO HA DENTRO IL NUMERO DI MINIMI, MA LOCAL_MIN_STEPS PARTE DA 0, vado da conto/2 -1 e conto/2
                    for j in range(local_min_steps[int((conto/2) -1)], local_min_steps[int((conto/2))]):       # devo assicurarmi che arrotndi per...?
                        real_value = minimi_array_index[x] + j
                        if(massimo < gfxs[real_value]):
                            massimo = gfxs[real_value]
                            index_massimo = real_value
                else:
                    massimo = gfxs[minimi_array_index[x] + local_min_steps[int((conto) / 2)]]   # DATO CHE CONTO HA DENTRO IL NUMERO DI MINIMI, MA LOCAL_MIN_STEPS PARTE DA 0, IL MINIMO CENTRALE è IN (CONTO+1)/2
                    index_massimo = minimi_array_index[x] + local_min_steps[int((conto) / 2)]
                    
                massimi_array.append(tempi[steps[minimi_array_index[x]]:][index_massimo])
                
        # print("minimi_array: {}".format(minimi_array))
        # print("massimi_array: {}".format(massimi_array))
        
        # Adesso che abbiamo tutta questa porcheria cerchiamo di calcolare altri tempi
        # print(colored("Calcolo tempo di contatto", "green"))
        tempo_contatto = 0
        for x in range(0, len(massimi_array) - 2):
            #
            # print("Differenza tra: {} e {} fa {}".format(massimi_array[x]["time"], minimi_array[x]["time"], massimi_array[x]["time"] - minimi_array[x]["time"]))
            tempo_contatto += massimi_array[x]["time"] - minimi_array[x]["time"]

        tempo_contatto /= len(massimi_array)

        print(colored("Tempo di contatto: {}".format(tempo_contatto), "yellow"))

        # print(colored("Calcolo tempo di volo", "green"))
        tempo_volo = 0
        for x in range(1, len(massimi_array) - 2):
            # print("Differenza tra: {} e {} fa {}".format(minimi_array[x]["time"], massimi_array[x-1]["time"], minimi_array[x]["time"] - massimi_array[x-1]["time"]))
            tempo_volo += minimi_array[x]["time"] - massimi_array[x-1]["time"]

        tempo_volo /= len(massimi_array)

        print(colored("Tempo di volo: {}".format(tempo_volo), "yellow"))

        # print(colored("Calcolo tempo totale e ritmo", "green"))
        tempo_totale = minimi_array[len(minimi_array) - 1]["time"] - minimi_array[0]["time"]
        ritmo = len(minimi_array) / tempo_totale

        print(colored("Tempo di totale: {}".format(tempo_totale), "yellow"))
        print(colored("Ritmo: {}".format(ritmo), "yellow"))

        print(colored("End processing " + file, "red"))

        jsello = {}
        jsello["minimi"] = minimi_array
        jsello["massimi"] = massimi_array
        jsello["tempo_contatto"] = tempo_contatto
        jsello["tempo_volo"] = tempo_volo
        jsello["tempo_totale"] = tempo_totale
        jsello["ritmo"] = ritmo

        with open(path_acc_data_json_grandezze + file, "w") as file_grandezze:
            json.dump(jsello, file_grandezze)

        omino += 1


if __name__ == "__main__":
    parse_file()