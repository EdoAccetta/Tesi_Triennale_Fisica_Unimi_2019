import json
import matplotlib.pyplot as plt #library used for simple plots 
from datetime import datetime, timedelta

# Apriamo il file
tempi = []
i = 0
first_time = datetime.strptime("00:00.0", "%M:%S.%f")
one_hour = datetime.strptime("01", "%M")
gravita = 9.80665

path_iphone_data = "../data/iphone/"    #This is for the old example file
with open(path_iphone_data + "csv/example.csv","r") as file_iphone:


#path_iphone_data = "../data/iphone/"    #This is ok for the new files, but they are formatted differently and need a different approach ||
#with open(path_iphone_data + "csv/0001 - (1) - IPH.csv","r") as file_iphone:   # || ValueError: time data 'time,gFx,gFy,gFz,gFTotal\n' does not match format '%M:%S.%f'

    # Leggiamo
    for line in file_iphone:
        valori = line.split(";")

        linea = {}
        
        time = datetime.strptime( valori[0], "%M:%S.%f")

        if i == 0:
            first_time = time

        diff_time = time - first_time
 
        # The given data can start from 59:59.00 and goes to 00:00.00, therefore if we detect a negative delta of the days we add one hour to the current time
        if diff_time.days < 0:
            time = datetime.strptime( "01:" + valori[0], "%H:%M:%S.%f")
            diff_time = time - first_time

        linea["step"] = i
        linea["time"] = str(diff_time)
        linea["gFx"] = float(valori[1]) * gravita
        linea["gFy"] = float(valori[2]) * gravita
        linea["gFz"] = float(valori[3]) * gravita
        linea["gFTotal"] = valori[4].replace("\n", "")


        tempi.append(linea)
        i = i+1

#numero = len(tempi)    #in future we'll surely need to know the vector lenght to do stuff
#for n in range (0, tempi[numero-1]["step"])    #tried to go for a cycle to fill the plot but i don't think it works, it needs the full vector
#   plt.plot(int(tempi[n]["step"]), float(tempi[n]["gFy"]))

plt.plot(int(tempi["step"]), float(tempi["gFy"]))   #TypeError: list indices must be integers or slices, not str || I don't get why these would still be considered strings

plt.xlabel('Step')  #gives x-axis a label
plt.ylabel('gFy  value') #gives y-axis a label
plt.title('Acceleration on Y axes (Vertical)')  #gives a title to the plot
plt.show()  #actually shows the plot on screen


with open(path_iphone_data + "json/example.json","w") as file_iphone:
    json.dump(tempi, file_iphone)