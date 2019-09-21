import json
import plotly.graph_objects as go
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from termcolor import colored

os.system('color')

path_acc_data = "E:/Scuola/Università/Tesi/Python/data/acc"

path_grandezze = path_acc_data + "/json_grandezze/"
path_grandezze_x = path_grandezze + "/grandezze_x/"
path_grandezze_y = path_grandezze + "/grandezze_y/"
path_grandezze_z = path_grandezze + "/grandezze_z/"
path_grandezze_basics = path_acc_data +"/json_grandezze_basics/grandezze_x_basics/"
path_grandezze_firstmax = path_acc_data +"/json_grandezze_firstmax/grandezze_x_firstmax/"
path_grandezze_second_min = path_acc_data +"/json_grandezze_second_min/grandezze_x_second_min/"
path_grandezze_secondmax = path_acc_data +"/json_grandezze_secondmax/grandezze_x_secondmax/"
path_grandezze_combinato = path_acc_data + "/json_grandezze_combinato/"
path_grandezze_passomedio_x = path_acc_data + "/json_passo_medio_grandezze/"
path_grandezze_passomedio_comb3 = path_acc_data + "/json_passo_medio_combinato_grandezze/"

path_real_val = path_acc_data + "/checks/valori_video/"

path_output = path_acc_data + "/checks/"

list_files = [
    f for f in listdir(path_grandezze_x)
    if isfile(join(path_grandezze_x, f))
]

def load_values():
    contatto_array = []
    with open(path_real_val + "valori_video_contatto.csv", "r") as file_contatto:
        for line in file_contatto:
            contatto_milliseconds = float(line.replace("\n", ""))
            contatto_array.append(contatto_milliseconds/1000)

    volo_array = []
    with open(path_real_val + "valori_video_volo.csv", "r") as file_volo:
        for line in file_volo:
            volo_milliseconds = float(line.replace("\n", ""))
            volo_array.append(volo_milliseconds/1000)

    array_coppie = []
    for x in range (0, len(volo_array)):
        array_coppie.append(contatto_array[x])
        array_coppie.append(volo_array[x])
    
    return array_coppie

def find_minore(array):
    which_min = 0
    minore = array[0]
    for x in range (1, len(array) - 1):
        if array[x] < minore:
            minore = array[x]
            which_min = x
    
    return which_min


def find_best():

    val_to_check = []   # Fuori dal for perchè deve essere esterno, generale. Ci accedo con y che modifico con ogni passaggio del for come y += 2
    # Qui ci saranno i valori misurati col videotracker per il confronto, T.Contatto e T.Volo

    val_to_check = load_values()
    # Ho riempito il vettore dei valori da controllare
    # print("Vettore valori: {}".format(val_to_check))

    # Variabili per il conteggio
    conteggio = []
    for j in range(0, 11):
        conteggio.append(0)
    ################################

    y = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))

        with open(path_grandezze_x + file, "r") as file_grandezze_x, open(path_grandezze_y + file, "r") as file_grandezze_y, open(path_grandezze_z + file, "r") as file_grandezze_z, open(path_grandezze_basics + file, "r") as file_basics, open(path_grandezze_firstmax + file, "r") as file_firstmax, open(path_grandezze_second_min + file, "r") as file_second_min, open(path_grandezze_secondmax + file, "r") as file_secondmax, open(path_grandezze_combinato + file, "r") as file_combinato, open(path_grandezze_passomedio_x + file, "r") as file_passomedio, open(path_grandezze_passomedio_comb3 + file, "r") as file_passomedio_comb3:

            couple_values = []  # All'interno del for perchè voglio generarlo ogni volta per ogni file che analizzo
            # "In ordine avremo: x,
            #                    y,
            #                    z,
            #                    basics,
            #                    firstmax,
            #                    second_min,
            #                    secondmax,
            #                    combinato,
            #                    passomedio,
            #                    passomedio combinato3"
            # Nel vettore couple_values ci saranno T.contatto e T.volo per ognuna di queste

            # Scarico i valori dai file
            json_great_x = json.load(file_grandezze_x)                      # Due valori T contatto e T volo
            json_great_y = json.load(file_grandezze_y)                      # Due valori T contatto e T volo
            json_great_z = json.load(file_grandezze_z)                      # Due valori T contatto e T volo
            json_great_basics = json.load(file_basics)                      # Due valori T contatto e T volo
            json_great_firstmax = json.load(file_firstmax)                  # Due valori T contatto e T volo
            json_great_second_min = json.load(file_second_min)              # Due valori T contatto e T volo
            json_great_secondmax = json.load(file_secondmax)                # Due valori T contatto e T volo
            json_great_combinato = json.load(file_combinato)                # Due valori T contatto e T volo
            json_great_passomedio = json.load(file_passomedio)              # Quattro valori T contatto e T volo, T contatto_loc e T volo_loc
            json_great_passomedio_comb3 = json.load(file_passomedio_comb3)  # Quattro valori T contatto e T volo, T contatto_loc e T volo_loc

            # Carico i valori nel vettore couple_values
            couple_values.append(json_great_x["tempo_contatto"])
            couple_values.append(json_great_x["tempo_volo"])

            couple_values.append(json_great_y["tempo_contatto"])
            couple_values.append(json_great_y["tempo_volo"])

            couple_values.append(json_great_z["tempo_contatto"])
            couple_values.append(json_great_z["tempo_volo"])

            couple_values.append(json_great_basics["tempo_contatto"])
            couple_values.append(json_great_basics["tempo_volo"])

            couple_values.append(json_great_firstmax["tempo_contatto"])
            couple_values.append(json_great_firstmax["tempo_volo"])

            couple_values.append(json_great_second_min["tempo_contatto"])
            couple_values.append(json_great_second_min["tempo_volo"])

            couple_values.append(json_great_secondmax["tempo_contatto"])
            couple_values.append(json_great_secondmax["tempo_volo"])

            couple_values.append(json_great_combinato["tempo_contatto"])
            couple_values.append(json_great_combinato["tempo_volo"])

            couple_values.append(json_great_passomedio["tempo_contatto"])
            couple_values.append(json_great_passomedio["tempo_volo"])

            couple_values.append(json_great_passomedio["tempo_contatto_loc"])
            couple_values.append(json_great_passomedio["tempo_volo_loc"])

            couple_values.append(json_great_passomedio_comb3["tempo_contatto"])
            couple_values.append(json_great_passomedio_comb3["tempo_volo"])

            couple_values.append(json_great_passomedio_comb3["tempo_contatto_loc"])
            couple_values.append(json_great_passomedio_comb3["tempo_volo_loc"])

            # Solo per l'output finale
            tempo_totale = json_great_x["tempo_totale"]
            ritmo = json_great_x["ritmo"]

            # Opero il confronto
            scarti = []     # Come dimensioni sarà la meta di couple_values perchè ne prende i valori a due a due
            x = 0
            # print("len(val_to_check)= {}".format(len(val_to_check)))
            while x in range (0, len(couple_values) - 1):
                # print("X = {}, Y = {}".format(x, y))
                scarti.append( abs(couple_values[x] - val_to_check[y]) + abs(couple_values[x+1] - val_to_check[y+1]) ) # Sommo gli scarti tra contatto e volo per ogni misura fatta
                x += 2

            # print("len(couple_values)= {})".format(len(couple_values)))
            # print("len(scarti)= {}".format(len(scarti)))
            minore = find_minore(scarti)

            # Conteggio per l'utilizzo dei metodi
            conteggio[minore] += 1
            ##################################

            # print(colored("Dei casi: 1 = x, 2 = y, 3 = z, 4 = basics, 5 = firstmax, 6 = second_min, 7 = secondmax, 8 = combinato, 9 = passomedio, 10 = passomedio_loc, 11 = passomedio_comb3, 12 = passomedio_comb3_loc"), "yellow")
            # print(colored("Con scarti: 1 = {}, 2 = {}, 3 = {}, 4 = {}, 5 = {}, 6 = {}, 7 = {}, 8 = {}, 9 = {}, 10 = {}, 11 = {}, 12 = {}".format(scarti[0], scarti[1], scarti[2], scarti[3], scarti[4], scarti[5], scarti[6], scarti[7], scarti[8], scarti[9], scarti[10], scarti[11])), "yellow")
            # print("Il minore è in: {}".format(minore))

            tempo_contatto_giusto = couple_values[minore*2]
            tempo_volo_giusto = couple_values[(minore*2) + 1]

            # print("Confrontato a= {}".format(val_to_check[y]))
            # print("tempo_contatto_migliore = {}".format(tempo_contatto_giusto))
            # print("Confrontato a= {}".format(val_to_check[y+1]))
            # print("tempo_volo_migliore = {}".format(tempo_volo_giusto))

            jsello = {}
            jsello["tempo_contatto"] = tempo_contatto_giusto
            jsello["tempo_volo"] = tempo_volo_giusto
            jsello["tempo_totale"] = tempo_totale
            jsello["ritmo"] = ritmo

            with open(path_output + file, "w") as file_output:
                json.dump(jsello, file_output)

        y += 2
        # print("y= {}".format(y))
        print(colored("End processing " + file, "red"))
    
    print("Quante volte si è usato x: {}".format(conteggio[0]))
    print("Quante volte si è usato y: {}".format(conteggio[1]))
    print("Quante volte si è usato z: {}".format(conteggio[2]))
    print("Quante volte si è usato basics: {}".format(conteggio[3]))
    print("Quante volte si è usato firstmax: {}".format(conteggio[4]))
    print("Quante volte si è usato second_min: {}".format(conteggio[5]))
    print("Quante volte si è usato secondmax: {}".format(conteggio[6]))
    print("Quante volte si è usato combinato: {}".format(conteggio[7]))
    print("Quante volte si è usato passomedio_x: {}".format(conteggio[8]))
    print("Quante volte si è usato passomedio_x_loc: {}".format(conteggio[9]))
    print("Quante volte si è usato passomedio_comb3: {}".format(conteggio[10]))
    print("Quante volte si è usato passomedio_comb3_oc: {}".format(conteggio[11]))

            





if __name__ == "__main__":
    find_best()