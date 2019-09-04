import json
import plotly.graph_objects as go
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from termcolor import colored

os.system('color')

path_acc_data = "E:/Scuola/Università/Tesi/Python/data/acc"
path_acc_data_json = path_acc_data + "/json_speed/"
path_acc_data_json_position = path_acc_data + "/json_position/"
path_acc_data_json_grandezze = path_acc_data + "/json_grandezze/"
list_files = [
    f for f in listdir(path_acc_data_json)
    if isfile(join(path_acc_data_json, f))
]

def parse_file():
    for file in list_files:
        print(colored("Processing " + file, "red"))
        with open(path_acc_data_json + file, "r") as file_speed:
            tempi = json.load(file_speed)

        # Calcolo la prima parte della formula
        jsello = { "positions" : []}
        for x in range(0, len(tempi) - 2):
            posizione_z_no_step = (
                (tempi[x]["velocita_z_step"] + tempi[x + 1]["velocita_z_step"]) *
                (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            posizione_x_no_step = (
                (tempi[x]["velocita_x_step"] + tempi[x + 1]["velocita_x_step"]) *
                (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            posizione_y_no_step = (
                (tempi[x]["velocita_y_step"] + tempi[x + 1]["velocita_y_step"]) *
                (tempi[x + 1]["time"] - tempi[x]["time"])) / 2
            
            node = {
                "posizione_z_no_step": posizione_z_no_step,
                "posizione_x_no_step": posizione_x_no_step,
                "posizione_y_no_step": posizione_y_no_step,
                "time": tempi[x]["time"],
                "step": tempi[x]["step"],
                "posizione_z_step": 0,
                "posizione_x_step": 0,
                "posizione_y_step": 0
            }

            if x >= 1:
                node["posizione_z_step"] = node["posizione_z_no_step"] + jsello["positions"][
                    x - 1]["posizione_z_step"]
                node["posizione_x_step"] = node["posizione_x_no_step"] + jsello["positions"][
                    x - 1]["posizione_x_step"]
                node["posizione_y_step"] = node["posizione_y_no_step"] + jsello["positions"][
                    x - 1]["posizione_y_step"]
            else:
                node["posizione_z_step"] = node["posizione_z_no_step"]
                node["posizione_x_step"] = node["posizione_x_no_step"]
                node["posizione_y_step"] = node["posizione_y_no_step"]

            jsello["positions"].append(node)

        # Adesso analizziamo la differenza di posizioni tra minimi calcolati prima
        with open(path_acc_data_json_grandezze + file, "r") as file_min:
            minimi = json.load(file_min)["minimi"]
            jsello["posizioni_minimi"] = []
            jsello["posizioni_minimi_delta"] = []
            last_index_minimo = 0
            for x in range(0, len(minimi)):
                minimo = minimi[x]
                while minimo["step"] > jsello["positions"][last_index_minimo]["step"]:
                    last_index_minimo += 1
                    if last_index_minimo >= len(jsello["positions"]): 
                        print("asd")
                jsello["posizioni_minimi"].append(jsello["positions"][last_index_minimo])
                if len(jsello["posizioni_minimi"])> 0:
                    jsello["posizioni_minimi_delta"].append(jsello["positions"][last_index_minimo]["posizione_z_step"] - jsello["posizioni_minimi"][len(jsello["posizioni_minimi"]) - 2]["posizione_z_step"])





















        with open(path_acc_data_json_position + file, "w") as file_posizione:
            json.dump(jsello, file_posizione)


if __name__ == "__main__":
    parse_file()