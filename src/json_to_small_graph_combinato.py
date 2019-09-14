import json
import plotly.graph_objects as go
import numpy as np
from os import listdir
from os.path import isfile, join

path_acc_data = "E:/Scuola/Università/Tesi/Python/data/acc"
path_acc_data_json = path_acc_data + "/json_combinato/"
path_acc_data_graphics = path_acc_data + "/graphics/steps_combinato_small/"
list_files = [
    f for f in listdir(path_acc_data_json)
    if isfile(join(path_acc_data_json, f))
]

# Carico in values_to_skip il numero di valori da saltare per ogni tipello
values_to_skip = []

with open(path_acc_data + "/utility/Escludere_Pre_Custom12.csv",
          "r") as file_utility:
    for line in file_utility:
        values_to_skip.append(int(line.replace("\n", "")))

def is_val_min(val_to_check, test_values):
    for value in test_values:
        if val_to_check >= value:
            return False
    return True


# Funzione ignoranta per trovare il primo minimo
def _find_first_minimo(tempi, accuracy):
    accuracy_half = int(accuracy / 2)
    for x in range(accuracy_half, len(tempi) - accuracy_half):
        test_values = []
        for j in range(accuracy_half, 0, -1):
            test_values.append(tempi[x - j])
        for j in range(1, accuracy_half + 1):
            test_values.append(tempi[x + j])

        val_to_check = tempi[x]

        if is_val_min(val_to_check, test_values):
            return x
    return -1

def find_first_minimo(tempi):
    return _find_first_minimo(tempi, 27)

def find_first_minimo_red(tempi):
    return _find_first_minimo(tempi, 11)

def find_first_minimo_locale(tempi):
    return _find_first_minimo(tempi, 3)



def parse_file():
    omino = 0
    for file in list_files:
        print("Processing " + file)
        with open(path_acc_data_json + file, "r") as file_acc:
            json_object = json.load(file_acc)

            tempi = json_object["tempi"]

            steps = []
            gfcs = []

            start_keep = False
            for tempo in tempi:
                step = int(tempo["step"])
                gfc = float(tempo["gFc"])

                start_keep = start_keep or (step > values_to_skip[omino])

                if start_keep:
                    steps.append(step)
                    gfcs.append(gfc)

            # Una volta creati gli arrays escludiamo n minimi
            latest_min_ind = 0
            for x in range(0, json_object["pre"]):
                index_minimo = find_first_minimo(gfcs)
                for y in range(25, 9, -1):
                    if y % 2 == 0:
                        continue
                    if index_minimo - latest_min_ind > 30:
                        index_minimo = _find_first_minimo(gfcs, y)
                    else:
                        break
                latest_min_ind = index_minimo
                if index_minimo > 0:
                    steps = steps[index_minimo:]
                    gfcs = gfcs[index_minimo:]
                else:
                    break

            # Adesso conto solamente n minimi dopo quello che ho trovato
            index_precedente = 0
            index_last_minimo = 0
            for x in range(0, json_object["into"]):
                index_last_minimo += find_first_minimo(gfcs[index_last_minimo:])
                for y in range(25, 9, -1):
                    # print("y= {}".format(y))
                    # print("Deltadiff = {}".format(index_last_minimo - index_precedente))
                    if y%2 == 0:
                        # print("BALZO")
                        continue
                    if index_last_minimo - index_precedente > 30:
                        # print("NO")
                        index_last_minimo = index_precedente + _find_first_minimo(gfcs[index_precedente:], y)
                    else:
                        # print("YES")
                        break
                index_precedente = index_last_minimo
                if index_last_minimo < 0:
                    break

            steps = steps[index_minimo:index_last_minimo]
            gfcs = gfcs[index_minimo:index_last_minimo]

            plt = go.Figure()
            plt.add_trace(
                go.Scatter(x=np.array(steps),
                           y=np.array(gfcs),
                           mode='lines+markers'))

            # Edit the layout
            plt.update_layout(title='Test {0}'.format(
                str.replace(file, ".json", "")),
                              xaxis_title='Steps',
                              yaxis_title='Gf_comb_s')

            # plt.show()
            # input("Premere INVIO per passare al prossimo grafico...\n")
            # break
            plt.write_image(path_acc_data_graphics + str.replace(file, "json", "pdf"))
        print("End processing " + file)
        omino += 1


if __name__ == "__main__":
    parse_file()