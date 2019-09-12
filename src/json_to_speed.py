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
path_acc_data_json_speed = path_acc_data + "/json_speed/"
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


def parse_file():
    omino = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))
        tempi = []
        minimi_da_escludere = 0
        minimi_da_tenere = 0
        steps = []
        gfzs = []
        with open(path_acc_data_json + file, "r") as file_acc:
            json_object = json.load(file_acc)
            tempi = json_object["tempi"][values_to_skip[omino] - 1:]
            minimi_da_escludere = json_object["pre"]
            minimi_da_tenere = json_object["into"]
            #Prepariamo steps e gfzs per dopo
            for tempo in tempi:
                steps.append(tempo["step"])
                gfzs.append(tempo["gFz"])

        # Calcolo la prima parte della formula
        jsello = {}
        velocita = []
        # INTEGRAZIONE A RETTANGOLI
        for x in range(0, len(tempi) - 2):
            velocita_z_no_step = tempi[x]["gFz"] * (tempi[x + 1]["time"] - tempi[x]["time"])
            velocita_x_no_step = tempi[x]["gFx"] * (tempi[x + 1]["time"] - tempi[x]["time"])
            velocita_y_no_step = tempi[x]["gFy"] * (tempi[x + 1]["time"] - tempi[x]["time"])
            node = {
                "velocita_z_no_step": velocita_z_no_step,
                "velocita_x_no_step": velocita_x_no_step,
                "velocita_y_no_step": velocita_y_no_step,
                "time": tempi[x]["time"],
                "step": tempi[x]["step"]
            }
            if x > 0:
                node["velocita_z_step"] = node["velocita_z_no_step"] + velocita[x-1]["velocita_z_step"]
                node["velocita_x_step"] = node["velocita_x_no_step"] + velocita[x-1]["velocita_x_step"]
                node["velocita_y_step"] = node["velocita_y_no_step"] + velocita[x-1]["velocita_y_step"]
            else:
                node["velocita_z_step"] = velocita_z_no_step
                node["velocita_x_step"] = velocita_x_no_step
                node["velocita_y_step"] = velocita_y_no_step

        #  INTEGRAZIONE PER TRAPEZI
        # for x in range(0, len(tempi) - 2):
            # velocita_z_no_step = ((tempi[x]["gFz"] + tempi[x + 1]["gFz"]) *
                        # (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            # velocita_x_no_step = ((tempi[x]["gFx"] + tempi[x + 1]["gFx"]) *
                        # (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            # velocita_y_no_step = ((tempi[x]["gFy"] + tempi[x + 1]["gFy"]) *
                        # (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            # node = {
                # "velocita_z_no_step": velocita_z_no_step,
                # "velocita_x_no_step": velocita_x_no_step,
                # "velocita_y_no_step": velocita_y_no_step,
                # "time": tempi[x]["time"],
                # "step": tempi[x]["step"]
            # }
            # if x > 0:
                # node["velocita_z_step"] = node["velocita_z_no_step"] + velocita[x-1]["velocita_z_step"]
                # node["velocita_x_step"] = node["velocita_x_no_step"] + velocita[x-1]["velocita_x_step"]
                # node["velocita_y_step"] = node["velocita_y_no_step"] + velocita[x-1]["velocita_y_step"]
            # else:
                # node["velocita_z_step"] = velocita_z_no_step
                # node["velocita_x_step"] = velocita_x_no_step
                # node["velocita_y_step"] = velocita_y_no_step

            velocita.append(node)

        # Una volta creati gli arrays escludiamo n minimi
        minimi_esclusi = 0
        for x in range(0, minimi_da_escludere):
            index_minimo = find_first_minimo(gfzs)
            minimi_esclusi += index_minimo
            if index_minimo > 0:
                steps = steps[index_minimo:]
                gfzs = gfzs[index_minimo:]
            else:
                break

        # Adesso conto solamente n minimi dopo quello che ho trovato
        index_last_minimo = 0
        for x in range(0, minimi_da_tenere):
            index_last_minimo += find_first_minimo(
                gfzs[index_last_minimo:])
            if index_last_minimo < 0:
                break

        da_step = minimi_esclusi
        a_step = da_step + index_last_minimo

        velocita_z_media = 0
        for x in range(da_step, a_step):
            velocita_z_media += velocita[x]["velocita_z_step"]

        velocita_z_media /= (index_last_minimo)

        jsello = { "velocita" : velocita, "velocita_z_media" : velocita_z_media}

        with open(path_acc_data_json_speed + file, "w") as file_speed:
            json.dump(jsello, file_speed)

        omino += 1


if __name__ == "__main__":
    parse_file()