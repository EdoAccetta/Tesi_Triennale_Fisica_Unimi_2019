import json
import plotly.graph_objects as go
import numpy as np
from os import listdir
from os.path import isfile, join

path_iphone_data = "../data/iphone"
path_iphone_data_json = path_iphone_data + "/json/"
path_iphone_data_graphics = path_iphone_data + "/graphics/steps_gfys/"
list_files = [f for f in listdir(path_iphone_data_json) if isfile(join(path_iphone_data_json, f))]

for file in  list_files:
    print("Processing " + file)
    with open(path_iphone_data_json + file,"r") as file_iphone:
        tempi = json.load(file_iphone)

        steps = np.array([])
        gfys = np.array([])

        for tempo in tempi:
            steps = np.append(steps, int(tempo["step"]))
            gfys = np.append(gfys, float(tempo["gFy"]))

        plt = go.Figure()
        plt.add_trace(go.Scatter(
            x=steps, 
            y=gfys,
            mode='lines+markers'))

        # Edit the layout
        plt.update_layout(title='Test {0}'.format(str.replace(file, ".json", "")),
                        xaxis_title='Steps',
                        yaxis_title='GfYs')

        # plt.show()
        plt.write_image(path_iphone_data_graphics + str.replace(file, "json", "pdf"))
    print("End processing " + file)