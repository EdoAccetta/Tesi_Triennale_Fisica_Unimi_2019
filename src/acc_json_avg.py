import json
import plotly.graph_objects as go
import numpy as np
from os import listdir
from os.path import isfile, join

path_acc_data = "../data/acc"
path_acc_data_json = path_acc_data + "/json/"
path_acc_data_json_avg = path_acc_data + "/json_avg/"
list_files = [f for f in listdir(path_acc_data_json) if isfile(join(path_acc_data_json, f))]

raggruppamento = 3

def get_tempo():
    return {
    "gFx" : 0,
    "gFy" : 0,
    "gFz" : 0,
    "Vax" : 0,
    "Vay" : 0,
    "Vaz" : 0,
    "time" : 0
    }

for file in  list_files:
    print("Processing " + file)
    with open(path_acc_data_json + file,"r") as file_acc:
        json_obj = json.load(file_acc)

        # Let's be avg!
        tempi_avg = []
        tempo_avg = get_tempo()
        
        counter_avg = 0
        step = 1
        
        tempi = json_obj["tempi"]

        for tempo in tempi:
            tempo_avg["gFx"]  += float(tempo["gFx"])
            tempo_avg["gFy"]  += float(tempo["gFy"])
            tempo_avg["gFz"]  += float(tempo["gFz"])
            tempo_avg["Vax"]  += float(tempo["Vax"])
            tempo_avg["Vay"]  += float(tempo["Vay"])
            tempo_avg["Vaz"]  += float(tempo["Vaz"])
            tempo_avg["time"] += float(tempo["time"])
            counter_avg += 1
            
            if counter_avg == raggruppamento:
                tempo_avg["step"] = step
                step += 1
                tempo_avg["gFx"]  /= raggruppamento
                tempo_avg["gFy"]  /= raggruppamento
                tempo_avg["gFz"]  /= raggruppamento
                tempo_avg["Vax"]  /= raggruppamento
                tempo_avg["Vay"]  /= raggruppamento
                tempo_avg["Vaz"]  /= raggruppamento
                tempo_avg["time"] /= raggruppamento
                tempi_avg.append(tempo_avg)
                tempo_avg = get_tempo()
                counter_avg = 0
        
        #After raggrupped all the data, Check for leftovers
        if counter_avg > 0:
            tempo_avg["step"] = step
            step += 1
            tempo_avg["gFx"]  /= counter_avg
            tempo_avg["gFy"]  /= counter_avg
            tempo_avg["gFz"]  /= counter_avg
            tempo_avg["Vax"]  /= counter_avg
            tempo_avg["Vay"]  /= counter_avg
            tempo_avg["Vaz"]  /= counter_avg
            tempo_avg["time"] /= counter_avg
            tempo_avg["leftovers"] = counter_avg
            tempi_avg.append(tempo_avg)


    json_obj["tempi"] = tempi_avg

    with open(path_acc_data_json_avg + file,"w") as file_acc:
        json.dump(json_obj, file_acc)