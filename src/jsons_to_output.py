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
path_speed = path_acc_data + "/json_speed/"
path_position = path_acc_data + "/json_position/"
path_grandezze_x = path_grandezze + "/grandezze_x/"
path_grandezze_z = path_grandezze + "/grandezze_z/"
path_results = path_acc_data + "/results/"
list_files_grandezze = [
    f for f in listdir(path_grandezze_x)
    if isfile(join(path_grandezze_x, f))
]

def to_virgul(value):
    return str(value).replace(".",",")

def output_all():

    # count = 0
    getout = []

    with open(path_results + "risultati_all.csv", "w") as file_results:

        for file in list_files_grandezze:
            with open(path_position + file, "r") as file_posizioni, open(path_grandezze_x + file, "r") as file_grandezze_x, open(path_grandezze_z + file, "r") as file_grandezze_z, open(path_speed + file, "r") as file_speed:
            
                json_positions = json.load(file_posizioni)
                json_greatness_x = json.load(file_grandezze_x)   # Qui dovrei trovare un modo per non caricare anche "minimi", che è lungo e non mi serve a nulla
                json_greatness_z = json.load(file_grandezze_z)
                json_speed = json.load(file_speed)
                polletto_poppo = {
                    "Lunghezza Passo": json_positions["posizioni_minimi_delta_media"],
                    "T. Contatto in x": json_greatness_x["tempo_contatto"],
                    "T. Contatto in z": json_greatness_z["tempo_contatto"],
                    "T. Volo in x": json_greatness_x["tempo_volo"],
                    "T. Volo in z": json_greatness_z["tempo_volo"],
                    "T. Totale in x": json_greatness_x["tempo_totale"],
                    "T. Totale in z": json_greatness_z["tempo_totale"],
                    "Ritmo in x": json_greatness_x["ritmo"],
                    "Ritmo in z": json_greatness_z["ritmo"],
                    "Velocita in z": json_speed["velocita_z_media"]
                }

                file_results.write("{}\nLunghezza Passo;{}\n T. Contatto in x;{}\n T. Volo in x;{}\n T. Totale in x;{}\n Ritmo in x;{}\n T. Contatto in z;{}\n T. Volo in z;{}\n""T. Totale in z;{}\n Ritmo in z;{}\nVelocita in z;{}\n\n".format(
                    file,to_virgul(json_positions["posizioni_minimi_delta_media"]),to_virgul(json_greatness_x["tempo_contatto"]),to_virgul(json_greatness_x["tempo_volo"]),to_virgul(json_greatness_x["tempo_totale"]),to_virgul(json_greatness_x["ritmo"]),to_virgul(json_greatness_z["tempo_contatto"]),to_virgul(json_greatness_z["tempo_volo"]),to_virgul(json_greatness_z["tempo_totale"]),to_virgul(json_greatness_z["ritmo"]),to_virgul( json_speed["velocita_z_media"])))

                getout.append(polletto_poppo)     # In realtà credo che dovrei metterlo fuori dal "with" ma dentro al "for", ma mi dà errore se lo sposto a sinistra
        

    with open(path_results + "risultati_all.json", "w") as file_results:
            json.dump(getout, file_results)

if __name__ == "__main__":
    output_all()