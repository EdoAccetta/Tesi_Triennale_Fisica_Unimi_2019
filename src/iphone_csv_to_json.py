import json
from datetime import datetime, timedelta

# Apriamo il file
tempi = []
i = 0
first_time = datetime.strptime("00:00.0", "%M:%S.%f")
one_hour = datetime.strptime("01", "%M")

path_iphone_data = "../data/iphone/"
with open(path_iphone_data + "csv/example.csv","r") as file_iphone:
    # Leggiamo
    for line in file_iphone:
        valori = line.split(";")

        linea = {}
        
        time = datetime.strptime( valori[0], "%M:%S.%f")

        if i == 0:
            first_time = time

        linea["step"] = i

        diff_time = time - first_time
 
        # The given data can start from 59:59.00 and goes to 00:00.00, therefore if we detect a negative delta of the days we add one hour to the current time
        if diff_time.days < 0:
            time = datetime.strptime( "01:" + valori[0], "%H:%M:%S.%f")
            diff_time = time - first_time

        linea["time"] = str(diff_time)
        linea["gFx"] = valori[1]
        linea["gFy"] = valori[2]
        linea["gFz"] = valori[3]
        linea["gFTotal"] = valori[4].replace("\n", "")


        tempi.append(linea)
        i = i+1



with open(path_iphone_data + "json/example.json","w") as file_iphone:
    json.dump(tempi, file_iphone)