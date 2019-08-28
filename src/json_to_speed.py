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

with open(path_acc_data + "/utility/Escludere_Pre_All.csv",
          "r") as file_utility:
    for line in file_utility:
        values_to_skip.append(int(line.replace("\n", "")))


def parse_file():
    omino = 0
    for file in list_files:
        print(colored("Processing " + file, "red"))
        tempi = []
        with open(path_acc_data_json + file, "r") as file_acc:
            json_object = json.load(file_acc)
            tempi = json_object["tempi"][values_to_skip[omino] - 1:]

        # Calcolo la prima parte della formula
        jsello = []
        for x in range(0, len(tempi) - 2):
            velocita_no_step = ((tempi[x]["gFz"] + tempi[x + 1]["gFz"]) *
                        (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            node = {
                "velocita_no_step": velocita_no_step,
                "time": tempi[x]["time"],
                "step": tempi[x]["step"]
            }
            if x > 0:
                node["velocita_step"] = node["velocita_no_step"] + jsello[x-1]["velocita_no_step"]
            else:
                node["velocita_step"] = velocita_no_step
            jsello.append(node)

        with open(path_acc_data_json_speed + file, "w") as file_speed:
            json.dump(jsello, file_speed)

        omino += 1


if __name__ == "__main__":
    parse_file()