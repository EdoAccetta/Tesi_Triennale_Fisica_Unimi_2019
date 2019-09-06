import json
import plotly.graph_objects as go
import numpy as np
from os import listdir
from os.path import isfile, join

path_acc_data = "../data/acc"
path_acc_data_json = path_acc_data + "/json_position/"
path_acc_data_graphics = path_acc_data + "/graphics/position_graphs/"
list_files = [f for f in listdir(path_acc_data_json) if isfile(join(path_acc_data_json, f))]

for file in  list_files:
    print("Processing " + file)
    with open(path_acc_data_json + file,"r") as file_acc:
        positions = json.load(file_acc)

        steps = np.array([])
        posz = np.array([])

        for pos in positions["positions"]:
            steps = np.append(steps, pos["step"])
            posz = np.append(posz, float(pos["posizione_z_step"]))

        plt = go.Figure()
        plt.add_trace(go.Scatter(
            x=steps, 
            y=posz,
            mode='lines+markers'))

        # Edit the layout
        plt.update_layout(title='Test {0}'.format(str.replace(file, ".json", "")),
                        xaxis_title='Steps',
                        yaxis_title='Position_z')

        # plt.show()
        # input("Premere INVIO per passare al prossimo grafico...\n")
        # break
        plt.write_image(path_acc_data_graphics + str.replace(file, "json", "pdf"))
              
    print("End processing " + file)