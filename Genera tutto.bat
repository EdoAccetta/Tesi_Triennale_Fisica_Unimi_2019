cd bat

START /wait acc_fje_to_json.bat
START /wait acc_json_avg.bat
START acc_csv_to_json_to_graph.bat
START avg_json_to_graph.bat