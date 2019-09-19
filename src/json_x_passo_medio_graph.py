# ATTENZIONE NON VA BENE, DEVI SUDDIVIDERE OGNI STEP IN UN UGAL NUMERO DI VALORI ALTRIMENTI NON TROVI LA FORMA GIUSTA
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
path_acc_data_graphics = path_acc_data + "/graphics/passo_medio/"
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
            return x
    return -1

def find_first_minimo(tempi):
    return _find_first_minimo(tempi, 27)

def find_first_minimo_red(tempi):
    return _find_first_minimo(tempi, 19)


def find_first_minimo_locale(tempi):
    return _find_first_minimo(tempi, 3)

def parse_file():
    omino = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))
        minimi_array_index = []
        minimi_array = []

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

            # Certo la dimensione media degli step in un passo
            step_medio = 0
            for x in range(0, len(minimi_array_index) - 1):
                step_medio += (minimi_array_index[x+1] - minimi_array_index[x]) # la sottrazione mi da sempre un valore in meno perchè esclude il primo

            step_medio = int(step_medio / len(minimi_array_index))
            # print("Step medio= {}".format(step_medio))

            # Creo dei vettori che abbiano tutti "step_medio" numero di step per poi mediarli
            thankyou_next = []
            new_array_to_mean = []
            step_from = 0
            step_to = 0
            for y in range(0, len(minimi_array_index) - 1): # Ciclo su ogni passo
                thankyou_next.append(step_medio * y)
                # print(thankyou_next)
                for x in range(minimi_array_index[y], minimi_array_index[y+1]): # Ciclo all'interno di ogni passo
                    if x == minimi_array_index[y] or x == minimi_array_index[y+1]:
                        new_array_to_mean.append(gfxs[x])
                    else:
                        rapporto = (minimi_array_index[y+1] - minimi_array_index[y]) / step_medio #La sottrazione mi toglie un valore
                        step_from = int(rapporto * (x - minimi_array_index[y]))
                        step_to = int((rapporto * (x - minimi_array_index[y])) + 1)
                        # new_array_to_mean.append((gfxs[step_from] + gfxs[step_to]) / 2) # Così ho dei gradini nel caso step_med < step_original, devo pesare la media per risolvere la cosa
                        decimale = (rapporto * (x - minimi_array_index[y])) - step_from
                        if decimale > 0.5:
                            peso = 1 - decimale
                        else:
                            peso = decimale
                        new_array_to_mean.append(( (gfxs[step_from] * peso) + (gfxs[step_to] * (1-peso)) / 2))

            # Adesso ho "new_array_to_mean" che contiene i valori di ogni vettore stretchato e "thankyou_next" che contiene dove ogni passo finisce e inizia quello nuovo nel vettore valori
            
            mean_step = []

            for n in range(0, step_medio):
                mean_step.append(0)
                for x in range(0, len(thankyou_next) - 1):
                    # print("n= {} x= {} into= {} tkyn:lenght= {}".format(n, x, json_object["into"], len(thankyou_next)))
                    # print("Thankyou_next[x]= {}".format(thankyou_next[x]))
                    mean_step[n] += new_array_to_mean[thankyou_next[x] + n]

                mean_step[n] /= len(thankyou_next) - 1

            # mean_step è un singolo passo formato dalla media di tutti gli altri passi visualizzati

            # Creo un vettore per il tempo nel grafico
            tempistica = []
            for x in range(0, step_medio):
                tempistica.append(0.01*x)

            plt = go.Figure()
            plt.add_trace(
                go.Scatter(x=np.array(tempistica),
                           y=np.array(mean_step),
                           mode='lines+markers'))

            # Edit the layout
            plt.update_layout(title='Test {0}'.format(
                str.replace(file, ".json", "")),
                              xaxis_title='Time',
                              yaxis_title='Gfxs_medio')

            # plt.show()
            # input("Premere INVIO per passare al prossimo grafico...\n")
            # break
            plt.write_image(path_acc_data_graphics + str.replace(file, "json", "pdf"))

        omino += 1

if __name__ == "__main__":
    parse_file()