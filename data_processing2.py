import csv
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import plotly

def create_pandas_data_frame_from_csv(path_to_csv, marker_tags, highlight_tags=None):
    '''
    Input: 
        path_to_csv:
            string 'path/to/example_csv_file.csv'

        marker_tags:
            string that matches the markers/rigid bodies entry: 'Rigid Body 1' OR 'Rigid Body 2:Marker1' OR any other row 4 (idx = 3) header

    Return: 
        list of dictionaries for each time with keys:
            [{time: rot_y: pos_x: pos_y: pos_z:}, ...]
    '''

    # Open csv and store it as a reader object
    with open(path_to_csv, newline='') as file:
        reader_obj = list(csv.reader(file))
    
    # Find out how many valid data entries the MoCap has
    for i, header in enumerate(reader_obj[0]):
        if header == 'Total Exported Frames':
            data_length = int(reader_obj[0][i + 1]) - 1
            break

    # Create a dict whose headers are the keys and dict[key] returns a list of values in the column
    Data = dict({'frame': [], 'time': [], 'z_position': [], 'x_position': []}) # 'time': [], 'y_rotation': [], 'x_position': [], 'y_position': [], 'z_position': []})

    # Iterate through each motion capture marker, as specified by its tag in the list of marker_tags supplied to the function

    for tag in marker_tags:
        Data[f'color for: {tag}'] = []
        Data[f'y_rotation for: {tag}'] = []
        Data[f'x_position for: {tag}'] = []
        Data[f'y_position for: {tag}'] = []
        Data[f'z_position for: {tag}'] = []

    for frame in list(range(7, data_length+7)):
        z_temp = []
        x_temp = []

        # frame data:
        Data['frame'].append(float(reader_obj[frame][0]))

        # time data:
        Data['time'].append(float(reader_obj[frame][1]))

        for tag in marker_tags:

            # Find the column index of the desired marker/rigid body
            for i, header in enumerate(reader_obj[3]):
                if header == tag:
                    column_num = i
                    break
        
            # color data:
            if tag in highlight_tags:
                Data[f'color for: {tag}'].append('r')
            else:
                Data[f'color for: {tag}'].append('b')

            # rot_y data:
            Data[f'y_rotation for: {tag}'].append(float("NaN"))  #reader_obj[frame][column_num + 1]))  doesnt work since rigid body x:markerx has different format than rigid body x

            # pos_x data:
            if reader_obj[frame][column_num] == '':
                Data[f'x_position for: {tag}'].append(float("NaN"))
            else:
                Data[f'x_position for: {tag}'].append(float(reader_obj[frame][column_num]))
                x_temp.append(Data[f'x_position for: {tag}'])

            # pos_y data: 
            if reader_obj[frame][column_num + 1] == '':
                Data[f'y_position for: {tag}'].append(float("NaN"))
            else:
                    Data[f'y_position for: {tag}'].append(float(reader_obj[frame][column_num + 1]))

            # pos_z data:
            if reader_obj[frame][column_num + 2] == '':
                Data[f'z_position for: {tag}'].append(float("NaN"))         
            else:
                Data[f'z_position for: {tag}'].append(float(reader_obj[frame][column_num + 2]))
                z_temp.append(Data[f'z_position for: {tag}'])
        
        Data['z_position'].append(z_temp)
        Data['x_position'].append(x_temp)


    # print("=================================================================")
    # print(f"key: frame ---> has length {len(Data['frame'])}")
    # print(f"key: time ---> has length {len(Data['time'])}")

    # for tag in marker_tags:
    #     print(f"key: 'color for: {tag}' ---> has length {len(Data[f'color for: {tag}'])}")

    #     print(f"key: 'y_rotation for: {tag}' ---> has length {len(Data[f'y_rotation for: {tag}'])}")
    #     print(f"key: 'x_position for: {tag}' ---> has length {len(Data[f'x_position for: {tag}'])}")
    #     print(f"key: 'z_position for: {tag}' ---> has length {len(Data[f'z_position for: {tag}'])}")

    # print("=================================================================")

    return pd.DataFrame(data=Data)


path_to_csv = 'CSV MoCap Data/Take 2023-06-28 02.03.55 PM.csv'
marker_tags = [
                #'Rigid Body 1', 'Rigid Body 2', 'Rigid Body 3',
                'Rigid Body 1:Marker1',
                'Rigid Body 1:Marker2', 
                'Rigid Body 1:Marker3', 
                'Rigid Body 1:Marker4', 
                'Rigid Body 1:Marker5', 
                'Rigid Body 1:Marker6', 
                'Rigid Body 1:Marker7',
                'Rigid Body 2:Marker1', 
                'Rigid Body 2:Marker2', 
                'Rigid Body 2:Marker3', 
                'Rigid Body 2:Marker4', 
                'Rigid Body 2:Marker5', 
                'Rigid Body 2:Marker6', 
                'Rigid Body 2:Marker7',
                'Rigid Body 3:Marker1', 
                'Rigid Body 3:Marker2', 
                'Rigid Body 3:Marker3', 
                'Rigid Body 3:Marker4', 
                'Rigid Body 3:Marker5', 
                'Rigid Body 3:Marker6',
                ]

df2 = px.data.gapminder()
print(df2)

df = create_pandas_data_frame_from_csv(path_to_csv, marker_tags, ['Rigid Body 3:Marker5'])
print(df)
fig = px.scatter(df, x='z_position', y='x_position', animation_frame='time', range_x=[-2.5, 2.5], range_y=[-2.5, 2.5])
fig.show()


