import json
import plotly.graph_objects as go
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from termcolor import colored

os.system('color')

path_acc_data = "E:/Scuola/Università/Tesi/Python/data/acc"
path_speed = path_acc_data + "/json_speed/"
path_position = path_acc_data + "/json_position/"
path_grandezze = path_acc_data + "/checks/"
# path_grandezze_firstmax = path_acc_data + "/json_grandezze_firstmax/grandezze_x_firstmax/"
# path_grandezze_basics = path_acc_data + "/json_grandezze_basics/grandezze_x_basics/"
# path_grandezze_second_min = path_acc_data + "/json_grandezze_second_min/grandezze_x_second_min/"
# path_grandezze_secondmax = path_acc_data + "/json_grandezze_secondmax/grandezze_x_secondmax/"
path_results = path_acc_data + "/results/"

list_files_grandezze = [
    f for f in listdir(path_grandezze)
    if isfile(join(path_grandezze, f))
]

def to_virgul(value):
    return str(value).replace(".",",")

def output_all():

    # count = 0
    getout = []

    with open(path_results + "risultati_all.csv", "w") as file_results:

        for file in list_files_grandezze:
            with open(path_position + file, "r") as file_posizioni, open(path_speed + file, "r") as file_speed, open(path_grandezze + file, "r") as file_grandezze:
            
                json_positions = json.load(file_posizioni)
                json_speed = json.load(file_speed)
                json_great = json.load(file_grandezze)   # Qui dovrei trovare un modo per non caricare anche "minimi", che è lungo e non mi serve a nulla

                polletto_poppo = {
                    "Lunghezza Passo": json_positions["posizioni_minimi_delta_media"],
                    "Contatto_x": json_great["tempo_contatto"],
                    "Volo_x": json_great["tempo_volo"],
                    "T. Totale in x": json_great["tempo_totale"],
                    "Ritmo in x": json_great["ritmo"],
                    "Velocita in z": json_speed["velocita_z_media"]
                }

                file_results.write("{}\nLunghezza Passo;{}\n T. Contatto;{}\n T. Volo;{}\n T. Totale;{}\n Ritmo;{}\n Velocita;{}\n\n".format(
                    file,to_virgul(json_positions["posizioni_minimi_delta_media"]),to_virgul(json_great["tempo_contatto"]),to_virgul(json_great["tempo_volo"]),to_virgul(json_great["tempo_totale"]),to_virgul(json_great["ritmo"]),to_virgul(json_speed["velocita_z_media"])))

                getout.append(polletto_poppo)     # In realtà credo che dovrei metterlo fuori dal "with" ma dentro al "for", ma mi dà errore se lo sposto a sinistra
        

    with open(path_results + "risultati_all.json", "w") as file_results:
            json.dump(getout, file_results)

if __name__ == "__main__":
    output_all()