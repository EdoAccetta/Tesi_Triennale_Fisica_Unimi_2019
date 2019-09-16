import json
import plotly.graph_objects as go
import numpy as np
from os import listdir
from os.path import isfile, join

path_acc_data = "../data/acc"
path_acc_data_json = path_acc_data + "/json/"
path_acc_data_graphics = path_acc_data + "/graphics/steps_gfxs/"
list_files = [f for f in listdir(path_acc_data_json) if isfile(join(path_acc_data_json, f))]

for file in  list_files:
    print("Processing " + file)
    with open(path_acc_data_json + file,"r") as file_acc:
        tempi = json.load(file_acc)["tempi"]

        times = np.array([])
        steps = np.array([])
        gfxs = np.array([])

        for tempo in tempi:
            times = np.append(times, tempo["time"])
            steps = np.append(steps, tempo["step"])
            gfxs = np.append(gfxs, float(tempo["gFx"]))

        plt = go.Figure()
        plt.add_trace(go.Scatter(
            x=times, 
            y=gfxs,
            mode='lines+markers'))

        # Edit the layout
        plt.update_layout(title='Test {0}'.format(str.replace(file, ".json", "")),
                        xaxis_title='Time',
                        yaxis_title='GfXs')

        # plt.show()
        # input("Premere INVIO per passare al prossimo grafico...\n")
        # break
        plt.write_image(path_acc_data_graphics + str.replace(file, "json", "pdf"))
              
    print("End processing " + file)