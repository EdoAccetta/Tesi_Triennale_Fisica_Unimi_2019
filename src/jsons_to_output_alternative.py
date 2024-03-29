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
path_grandezze_x = path_acc_data + "/json_grandezze/grandezze_x/"
path_grandezze_firstmax = path_acc_data + "/json_grandezze_firstmax/grandezze_x_firstmax/"
path_grandezze_basics = path_acc_data + "/json_grandezze_basics/grandezze_x_basics/"
path_grandezze_second_min = path_acc_data + "/json_grandezze_second_min/grandezze_x_second_min/"
path_grandezze_secondmax = path_acc_data + "/json_grandezze_secondmax/grandezze_x_secondmax/"
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

    with open(path_results + "risultati_alternative.csv", "w") as file_results:

        for file in list_files_grandezze:
            with open(path_grandezze_basics + file, "r") as file_basics, open(path_grandezze_x + file, "r") as file_grandezze_x, open(path_grandezze_firstmax + file, "r") as file_firstmax, open(path_grandezze_second_min + file, "r") as file_second_min, open(path_grandezze_secondmax + file, "r") as file_secondmax:
            
                # json_positions = json.load(file_posizioni)
                # json_speed = json.load(file_speed)
                json_great_x = json.load(file_grandezze_x)   # Qui dovrei trovare un modo per non caricare anche "minimi", che è lungo e non mi serve a nulla
                json_great_firstmax = json.load(file_firstmax)
                json_great_basics = json.load(file_basics)
                json_great_second_min = json.load(file_second_min)
                json_great_secondmax = json.load(file_secondmax)

                polletto_poppo = {
                    # "Lunghezza Passo": json_positions["posizioni_minimi_delta_media"],
                    # "Contatto_x": json_great_x["tempo_contatto"],
                    # "Volo_x": json_great_x["tempo_volo"],
                    # "T. Totale in x": json_great_x["tempo_totale"],
                    # "Ritmo in x": json_great_x["ritmo"],
                    # "Velocita in z": json_speed["velocita_z_media"]

                    "Contatto_basics": json_great_basics["tempo_contatto"],
                    "Volo_basics": json_great_basics["tempo_volo"],
                     
                    "Contatto_x": json_great_x["tempo_contatto"],
                    "Volo_x": json_great_x["tempo_volo"],

                    "Contatto_second_min": json_great_second_min["tempo_contatto"],
                    "Volo_second_min": json_great_second_min["tempo_volo"],

                    "Contatto_firstmax": json_great_firstmax["tempo_contatto"],
                    "Volo_firstmax": json_great_firstmax["tempo_volo"],

                    "Contatto_secondmax": json_great_secondmax["tempo_contatto"],
                    "Volo_secondmax": json_great_secondmax["tempo_volo"],
                    
                }

                file_results.write("{}\nT. Contatto basics;{}\n T. Volo basics;{}\n T. Contatto in x;{}\n T. Volo in x;{}\nT. Contatto s_min;{}\n T. Volo s_min;{}\nT. Contatto firstmax;{}\n T. Volo firstmax;{}\nT. Contatto secondmax;{}\n T. Volo secondmax;{}\n\n".format(
                    file,to_virgul(json_great_basics["tempo_contatto"]),to_virgul(json_great_basics["tempo_volo"]),to_virgul(json_great_x["tempo_contatto"]),to_virgul(json_great_x["tempo_volo"]),to_virgul(json_great_second_min["tempo_contatto"]),to_virgul(json_great_second_min["tempo_volo"]),to_virgul(json_great_firstmax["tempo_contatto"]),to_virgul(json_great_firstmax["tempo_volo"]),to_virgul(json_great_secondmax["tempo_contatto"]),to_virgul(json_great_secondmax["tempo_volo"])))


                # file_results.write("{}\nLunghezza Passo;{}\n T. Totale in x;{}\n Ritmo in x;{}\n Velocita in z;{}\n T. Contatto in basics;{}\n T. Volo in basics;{}\n T. Contatto in x;{}\n T. Volo in x;{}\n T. Contatto in s_min;{}\n T. Volo in s_min;{}\n T. Contatto in f_max;{}\n T. Volo in f_max;{}\n T. Contatto in s_max;{}\n T. Volo in s_max;{}\n\n".format(
                    # file,to_virgul(json_positions["posizioni_minimi_delta_media"]),to_virgul(json_great_x["tempo_totale"]),to_virgul(json_great_x["ritmo"]),to_virgul( json_speed["velocita_z_media"]),to_virgul(json_great_basics["tempo_contatto"]),to_virgul(json_great_basics["tempo_volo"]),to_virgul(json_great_x["tempo_contatto"]),to_virgul(json_great_x["tempo_volo"]),to_virgul(json_great_second_min["tempo_contatto"]),to_virgul(json_great_second_min["tempo_volo"]),to_virgul(json_great_firstmax["tempo_contatto"]),to_virgul(json_great_firstmax["tempo_volo"]),to_virgul(json_great_secondmax["tempo_contatto"]),to_virgul(json_great_secondmax["tempo_volo"])))

                getout.append(polletto_poppo)     # In realtà credo che dovrei metterlo fuori dal "with" ma dentro al "for", ma mi dà errore se lo sposto a sinistra
        

    with open(path_results + "risultati_alternative.json", "w") as file_results:
            json.dump(getout, file_results)

if __name__ == "__main__":
    output_all()