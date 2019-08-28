import json
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

def load_pre():
    pre_array = []
    with open(path_acc_data_fje + "Passi_pre.csv", "r") as file_pre:
        for line in file_pre:
            # Ma che cazzo è "ï»¿" ? 
            pre_array.append(int(line.replace("\n", "").replace("ï»¿", "")))

    return pre_array


def load_into():
    into_array = []
    with open(path_acc_data_fje + "Passi_into.csv", "r") as file_into:
        for line in file_into:
            into_array.append(int(line.replace("\n", "").replace("ï»¿", "")))

    return into_array


path_acc_data = "../data/acc"
path_acc_data_fje = path_acc_data + "/fje/"
path_acc_data_json = path_acc_data + "/json/"
list_files = [
    f for f in listdir(path_acc_data_fje) if isfile(join(path_acc_data_fje, f))
]

pre_array = load_pre()
into_array = load_into()

for file in list_files:

    # Apriamo il file
    json_values = {}
    tempi = []
    i = 0

    if ".fje" not in file:
        continue

    json_values["pre"] = pre_array[i]
    json_values["into"] = into_array[i]
    
    print("Processing " + file)
    with open(path_acc_data_fje + file, "r") as file_acc:
        # Leggiamo
        for line in file_acc:
            valori = line.split(",")

            linea = {}

            # Acc X	Acc Y	Acc Z	V ang X	V ang Y	V ang Z	Latitudine	Longitudine	Timestamp
            linea["step"] = i
            linea["gFx"] = float(valori[0]) - 9.948443643
            linea["gFy"] = float(valori[1])
            linea["gFz"] = float(valori[2])
            linea["Vax"] = float(valori[3])
            linea["Vay"] = float(valori[4])
            linea["Vaz"] = float(valori[5])
            linea["time"] = float(valori[8].replace("\n", ""))

            tempi.append(linea)
            i = i + 1

    json_values["tempi"] = tempi

    with open(path_acc_data_json + file.replace(".fje", ".json"),
              "w") as file_acc:
        json.dump(json_values, file_acc)