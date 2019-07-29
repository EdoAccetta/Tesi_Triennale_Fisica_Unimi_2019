import json
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

path_acc_data = "../data/acc"
path_acc_data_fje = path_acc_data + "/fje/"
path_acc_data_json = path_acc_data + "/json/"
list_files = [f for f in listdir(path_acc_data_fje) if isfile(join(path_acc_data_fje, f))]

for file in  list_files:

    # Apriamo il file
    tempi = []
    i = 0

    with open(path_acc_data_fje + file,"r") as file_acc:
        # Leggiamo
        for line in file_acc:
            valori = line.split(",")

            linea = {}

            #Acc X	Acc Y	Acc Z	V ang X	V ang Y	V ang Z	Latitudine	Longitudine	Timestamp

            linea["step"] = i
            
            linea["gFx"] = valori[0]
            linea["gFy"] = valori[1]
            linea["gFz"] = valori[2]
            linea["Vax"] = valori[3]
            linea["Vay"] = valori[4]
            linea["Vaz"] = valori[5]
            linea["time"] = valori[8].replace("\n", "")

            tempi.append(linea)
            i = i+1



    with open(path_acc_data_json + file.replace(".fje", ".json"),"w") as file_acc:
        json.dump(tempi, file_acc)