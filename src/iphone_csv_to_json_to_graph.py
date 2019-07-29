import json
import plotly.graph_objects as go
import numpy as np

path_iphone_data = "C:/Users/mtollari/Desktop/Code/tesi_dido/data/iphone/json/example.json"
with open(path_iphone_data,"r") as file_iphone:
    tempi = json.load(file_iphone)

    steps = np.array([])
    gfys = np.array([])

    for tempo in tempi:
        steps = np.append(steps, int(tempo["step"]))
        gfys = np.append(gfys, float(tempo["gFy"]))

    plt = go.Figure()
    plt.add_trace(go.Scatter(x=steps, y=gfys,
                    mode='lines',
                    name='gianpiero'))
    

    plt.show()