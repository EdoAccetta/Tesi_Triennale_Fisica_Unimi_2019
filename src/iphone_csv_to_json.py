import json
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

path_iphone_data = "../data/iphone"
path_iphone_data_csv = path_iphone_data + "/csv/"
path_iphone_data_json = path_iphone_data + "/json/"
list_files = [f for f in listdir(path_iphone_data_csv) if isfile(join(path_iphone_data_csv, f))]

for file in  list_files:
    # Apriamo il file
    tempi = []
    i = 0
    first_time = datetime.strptime("00:00.0", "%M:%S.%f")
    one_hour = datetime.strptime("01", "%M")
    gravita = 9.80665

    with open(path_iphone_data_csv + file,"r") as file_iphone:
        # Leggiamo
        for line in file_iphone:
            valori = line.split(",")

            if valori[0] == "time" or file_iphone == "example.csv":
                continue

            linea = {}
            
            time = datetime.strptime(valori[0][11:], "%H:%M:%S.%f")
            
            if i == 0:
                first_time = time

            diff_time = time - first_time
    
            # The given data can start from 59:59.00 and goes to 00:00.00, therefore if we detect a negative delta of the days we add one hour to the current time
            # if diff_time.days < 0:
                # time = datetime.strptime( "01:" + valori[0], "%H:%M:%S.%f")
                # diff_time = time - first_time

            linea["step"] = i
            linea["time"] = str(diff_time)
            linea["timestamp"] = valori[0]
            linea["gFx"] = float(valori[1]) * gravita
            linea["gFy"] = float(valori[2]) * gravita
            linea["gFz"] = float(valori[3]) * gravita
            linea["gFTotal"] = valori[4].replace("\n", "")


            tempi.append(linea)
            i = i+1



    with open(path_iphone_data_json + file.replace(".csv", ".json"),"w") as file_iphone:
        json.dump(tempi, file_iphone)