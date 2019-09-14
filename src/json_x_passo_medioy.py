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
                if index_minimo - latest_min_ind > 30:
                    index_minimo = find_first_minimo_red(gfxs)
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
                if index_last_minimo - index_precedente > 30:
                    index_last_minimo = index_precedente + find_first_minimo_red(gfxs[index_precedente:])
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
                step_medio += minimi_array_index[x+1] - minimi_array_index[x]

            step_medio = int(step_medio / len(minimi_array_index))
            print("Step medio= {}".format(step_medio))

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
                        rapporto = step_medio / (minimi_array_index[y+1] - minimi_array_index[y])
                        step_from = int(rapporto * (x - minimi_array_index[y]))
                        step_to = int((rapporto * (x - minimi_array_index[y])) + 1)
                        # new_array_to_mean.append((gfxs[step_from] + gfxs[step_to]) / 2) # Così ho dei gradini nel caso step_med < step_original, devo pesare la media per risolvere la cosa
                        peso = (rapporto * (x - minimi_array_index[y])) - step_from # Considero la parte decimale di step from non tagliato e la uso come percentuale ovvero come peso
                        new_array_to_mean.append(( (gfxs[step_from] * peso) + (gfxs[step_to] * abs(1-peso)) / 2))

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

            '''
            # Certo la dimensione minima in step di un passo (distanza più piccola tra minimi) (per non andare out of bound con gli indici)
            step_minore = 0
            for x in range(0, len(minimi_array_index) - 1):
                if step_minore > minimi_array_index[x+1] - minimi_array_index[x]:
                    step_minore = minimi_array_index[x+1] - minimi_array_index[x]
                if x == 0 :
                    step_minore = minimi_array_index[1] - minimi_array_index[0]

            # Ore faccio la media di ogni valore del passo dal primo allo "step_minore" alla ricerca di un passo in cui ogni valore è mediato tra tutti
            gfx_med = []
            for n in range (0, step_minore): # Ciclo sul numero di step da considerare in ogni passo
                # print("n = {}".format(n))
                gfx_med.append(0)
                for x in range(0, json_object["into"] - 1): # Ciclo sui valori iniziali dei minimi   
                    # print("x = {} con into = {}".format(x, json_object["into"]))
                    # print("minimi_array_index[x] + n = {}".format(minimi_array_index[x] + n))   
                    # print("gfxs[{}] = {}".format(minimi_array_index[x] + n, gfxs[minimi_array_index[x] + n]))
                    # print("gfx_med[0] = {}".format(gfx_med[0]))
                    gfx_med[n] += gfxs[minimi_array_index[x] + n]
                gfx_med[n] /= json_object["into"]

            # gfx_med è un singolo passo formato dalla media di tutti gli altri passi visualizzati

            # Creo un vettore per il tempo nel grafico
            tempistica = []
            for x in range(0, step_minore):
                tempistica.append(0.01*x)

            plt = go.Figure()
            plt.add_trace(
                go.Scatter(x=np.array(tempistica),
                           y=np.array(gfx_med),
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

            '''
            '''
            # Possiamo trovare i massimi come punto più alto tra due minimi
            for x in range(0, len(minimi_array_index) - 2):
                massimo = 0
                # index_massimo = 0
                # print("minimi_array_index {}, minimi_array_index + 1 {}".format(minimi_array_index[x], minimi_array_index[x+1]))
                # for j in range(minimi_array_index[x], minimi_array_index[x+1]):
                #     if(massimo < gfxs[j]):
                #         massimo = gfxs[j]
                #         index_massimo = j
                # massimi_array.append(tempi[steps[index_massimo] - 1])
                array_in_campione = gfxs[minimi_array_index[x]:minimi_array_index[x+1]]
                massimo = find_first_minimo_locale(array_in_campione)
                # print("Index minimo: {}".format(index_minimo))
                # print("minimi_array_index: {}".format(minimi_array_index))
                # print("steps[minimi_array_index[x]]: {}".format(steps[minimi_array_index[x]]))
                # print("steps[minimi_array_index[x+1]]: {}".format(steps[minimi_array_index[x+1]]))
                # print("len(gfxs): {}".format(len(gfxs)))
                # print("len(steps): {}".format(len(steps)))
                # print("Nell'array: {}".format(array_in_campione))
                # print("Massimo è: {}".format(massimo))
                # print("Valore massimo è: {}".format(array_in_campione[massimo]))
                # for t in range(0, 9):
                    # print("Minimo inizio {} e minimo finale {}".format(minimi_array_index[t], minimi_array_index[t+1]))
                massimi_array.append(tempi[steps[minimi_array_index[x]]:][massimo])
                
        # print("minimi_array: {}".format(minimi_array))
        # print("massimi_array: {}".format(massimi_array))
        
        # Adesso che abbiamo tutta questa porcheria cerchiamo di calcolare altri tempi
        # print(colored("Calcolo tempo di contatto", "green"))
        tempo_contatto = 0
        for x in range(0, len(minimi_array_index) - 2):
            # print("Differenza tra: {} e {} fa {}".format(massimi_array[x]["time"], minimi_array[x]["time"], massimi_array[x]["time"] - minimi_array[x]["time"]))
            tempo_contatto += massimi_array[x]["time"] - minimi_array[x]["time"]

        tempo_contatto /= len(massimi_array)

        print(colored("Tempo di contatto: {}".format(tempo_contatto), "yellow"))

        # print(colored("Calcolo tempo di volo", "green"))
        tempo_volo = 0
        for x in range(1, len(minimi_array_index) - 1):
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
        '''

if __name__ == "__main__":
    parse_file()