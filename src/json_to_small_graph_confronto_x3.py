import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from os import listdir
from os.path import isfile, join

path_acc_data = "E:/Scuola/Università/Tesi/Python/data/acc"
path_acc_data_json = path_acc_data + "/json/"
path_acc_data_json_combined = path_acc_data + "/json_combinato_3/"
path_acc_data_graphics = path_acc_data + "/graphics/confronto_comb3_and_x_small/"
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
        with open(path_acc_data_json + file, "r") as file_acc, open(path_acc_data_json_combined + file, "r") as file_comb:
            json_object = json.load(file_acc)
            json_comb = json.load(file_comb)

            tempi = json_object["tempi"]
            tempi_c = json_comb["tempi"]

            times = []
            steps = []
            gfxs = []
            gfcs = []

            start_keep = False
            for tempo in tempi:
                time = float(tempo["time"])
                step = int(tempo["step"])
                gfx = float(tempo["gFx"])

                start_keep = start_keep or (step > values_to_skip[omino])

                if start_keep:
                    times.append(time)
                    steps.append(step)
                    gfxs.append(gfx)
            
            start_keep = False
            for tempo_c in tempi_c:
                time = float(tempo_c["time"])
                step = int(tempo_c["step"])
                gfc = float(tempo_c["gFc"])

                start_keep = start_keep or (step > values_to_skip[omino])

                if start_keep:
                    times.append(time)
                    steps.append(step)
                    gfcs.append(gfc)

            # Una volta creati gli arrays escludiamo n minimi NOTA: Cerco i minimi in x e sfrutto i minimi trovati per tagliare il set combinato
            latest_min_ind = 0
            for x in range(0, json_object["pre"]):
                index_minimo = find_first_minimo(gfxs)
                for y in range(25, 9, -1):
                    if y % 2 == 0:
                        continue
                    if index_minimo - latest_min_ind > 30:
                        index_minimo = _find_first_minimo(gfxs, y)
                    else:
                        break
                latest_min_ind = index_minimo
                if index_minimo > 0:
                    times = times[index_minimo:]
                    steps = steps[index_minimo:]
                    gfxs = gfxs[index_minimo:]
                    gfcs = gfcs[index_minimo:]
                else:
                    break

            # Adesso conto solamente n minimi dopo quello che ho trovato
            index_precedente = 0
            index_last_minimo = 0
            for x in range(0, json_object["into"]):
                index_last_minimo += find_first_minimo(gfxs[index_last_minimo:])
                for y in range(25, 9, -1):
                    # print("y= {}".format(y))
                    # print("Deltadiff = {}".format(index_last_minimo - index_precedente))
                    if y%2 == 0:
                        # print("BALZO")
                        continue
                    if index_last_minimo - index_precedente > 30:
                        # print("NO")
                        index_last_minimo = index_precedente + _find_first_minimo(gfxs[index_precedente:], y)
                    else:
                        # print("YES")
                        break
                index_precedente = index_last_minimo
                if index_last_minimo < 0:
                    break

            times = times[index_minimo:index_last_minimo]
            steps = steps[index_minimo:index_last_minimo]
            gfxs = gfxs[index_minimo:index_last_minimo]
            gfcs = gfcs[index_minimo:index_last_minimo]

            # Create figure with secondary y-axis
            plt = make_subplots(specs=[[{"secondary_y": True}]])

            # plt = go.Figure()
            plt.add_trace(
                go.Scatter(x=np.array(times),
                           y=np.array(gfcs),
                           mode='lines+markers',
                           name="Gf_Sum"),
                secondary_y=False,)
            # Aggiungo grafico delle x insieme               
            plt.add_trace(
                go.Scatter(
                    x = np.array(times),
                    y = np.array(gfxs),
                    mode='lines+markers',
                    name="Gf_x"),
                secondary_y=True,)

            # Add figure title
            plt.update_layout(title_text="Double Y Axis: Gf_Sum and Gf_x - {0}".format(str.replace(file, ".json", "")))

            # Set x-axis title
            plt.update_xaxes(title_text="Time")

            # Set y-axes titles
            plt.update_yaxes(title_text="Gf_Sum axis", secondary_y=False)
            plt.update_yaxes(title_text="Gf_x axis", secondary_y=True)

            # plt.show()
            # input("Premere INVIO per passare al prossimo grafico...\n")
            # break
            plt.write_image(path_acc_data_graphics + str.replace(file, "json", "pdf"))
        print("End processing " + file)
        omino += 1


if __name__ == "__main__":
    parse_file()