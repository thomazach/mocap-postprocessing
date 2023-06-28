import csv
import matplotlib
from matplotlib import pyplot as plot
import time as timeee
import math
import time

def create_marker_data(path_to_csv, marker_tag):
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

    with open(path_to_csv, newline='') as file:
        reader_obj = list(csv.reader(file))

    # Get number of data entry rows
    for i, header in enumerate(reader_obj[0]):
        if header == 'Total Exported Frames':
            data_length = int(reader_obj[0][i + 1])
            break
    
    # Find the index of the desired marker/rigid body
    for i, header in enumerate(reader_obj[3]):
        if header == marker_tag:
            column_num = i
            break

    data_frame = []
    for frame in list(range(7, data_length+7)):

        try:
            # time data:
            time = float(reader_obj[frame][1])

            # rot_y data:
            y_rotation = float(reader_obj[frame][column_num + 1])

            # pos_x data:
            x_position = float(reader_obj[frame][column_num + 3])

            # pos_y data: 
            y_position = float(reader_obj[frame][column_num + 4])

            # pos_z data:
            z_position = float(reader_obj[frame][column_num + 5])
        except ValueError:
            # time data:
            time = float('NaN')

            # rot_y data:
            y_rotation = float('NaN')

            # pos_x data:
            x_position = float('NaN')

            # pos_y data: 
            y_position = float('NaN')

            # pos_z data:
            z_position = float('NaN')
        
        data_frame.append(dict({'time': time,  'rot_y': y_rotation, 'pos_x': x_position, 'pos_y': y_position, 'pos_z': z_position}))

    return data_frame

path_to_csv = 'Take 2023-06-27 01.17.18 PM.csv'
path_to_csv2 = 'Take 2023-06-27 01.24.14 PM.csv'
marker_tags = ['Rigid Body 1:Marker1', 
               'Rigid Body 1:Marker2', 
               'Rigid Body 1:Marker3', 
               'Rigid Body 1:Marker4', 
               'Rigid Body 1:Marker5', 
               'Rigid Body 1:Marker6',
               'Rigid Body 2:Marker1', 
               'Rigid Body 2:Marker2', 
               'Rigid Body 2:Marker3', 
               'Rigid Body 2:Marker4', 
               'Rigid Body 2:Marker5', 
               'Rigid Body 3:Marker1', 
               'Rigid Body 3:Marker2', 
               'Rigid Body 3:Marker3', 
               'Rigid Body 3:Marker4', 
               #'Rigid Body 3:Marker5'
               ]

rigid_bodies = {}
for tag in marker_tags:
    rigid_bodies[tag] = create_marker_data(path_to_csv2, tag)


#Working, but VERY slow
# ### Graphing time!
f = plot.figure(1)
f.set_size_inches(18.5, 7)
plot.clf()
ax = f.add_subplot(1, 1, 1)
plot.axis('equal')
plot.box('on')
ax.set_ylim(-2.5, 2.5)
ax.set_xlim(-2.5, 2.5)

x = [] # is pos_z since mocap uses y as vertical axis
y = [] # is pos_x to place the linkage how its expected (left to right motion)
for i, body in enumerate(rigid_bodies):
    x.append(rigid_bodies[body][0]['pos_z'])
    y.append(rigid_bodies[body][0]['pos_x'])

body_plot = ax.plot(x, y, c='b', linestyle='', marker='.')
plot.pause(0.00833333) # 1second/120fps

X = []
Y = []
for i in list(range(1, 3150)):
    x = []
    y = [] # is pos_z since mocap uses y as vertical axis


    for body in rigid_bodies:
         x.append(rigid_bodies[body][i]['pos_z'])
         y.append(rigid_bodies[body][i]['pos_x'])
    
    X.append(x)
    Y.append(y)
    

    #print(i, rigid_bodies['Rigid Body 3:Marker1'][i]['time'])

for i in list(range(1, 3150)):

    print(i)

    for i3 in range(0, len(body_plot)):
        body_plot[i3].set_xdata(X[i])
        body_plot[i3].set_ydata(Y[i])

    plot.pause(0.001)


'''

The rigid body rotations captured by Mocap are garbage. 



marker_tags = ['Rigid Body 1', 'Rigid Body 2', 'Rigid Body 3']

rigid_bodies = {}
for tag in marker_tags:
    rigid_bodies[tag] = create_marker_data(path_to_csv, tag)

### Graphing time!
f = plot.figure(1)
ax = f.add_subplot(1, 1, 1)
plot.axis('equal')
plot.box('on')
ax.set_ylim(-2.5, 2.5)
ax.set_xlim(-2.5, 2.5)

x = []
line_x = []
y = [] # is pos_z since mocap uses y as vertical axis
line_y = []
for i, body in enumerate(rigid_bodies):
    x.append(rigid_bodies[body][0]['pos_x'])
    y.append(rigid_bodies[body][0]['pos_z'])

    r = 0.15 # In meters
    m = math.tan(rigid_bodies[body][0]['rot_y'])
    x_diff = r/math.sqrt(1 + m**2)

    y_diff = m * x_diff 

    min_x = x[i] - x_diff
    max_x = x[i] + x_diff

    min_y = y[i] - y_diff
    max_y = y[i] + y_diff

    line_x.append(min_x)
    line_x.append(max_x)

    line_y.append(min_y)
    line_y.append(max_y)

    # Calculate line 

# Make scatter of center of rigid bodies as listed by MoCap
body_plot = ax.plot(x, y, c='b', marker='.', linestyle='')
line_plot = ax.plot(line_x, line_y, c='k')


for i in list(range(1, 2176)):
    print(i)
    x = []
    y = [] # is pos_z since mocap uses y as vertical axis

    line_x = []
    line_y = []

    for i2, body in enumerate(rigid_bodies):
        x.append(rigid_bodies[body][i]['pos_x'])
        y.append(rigid_bodies[body][i]['pos_z'])

        r = 0.15 # In meters
        m = math.tan(math.radians(rigid_bodies[body][0]['rot_y']))
        x_diff = r/math.sqrt(1 + m**2)

        min_x = x[i2] - x_diff
        max_x = x[i2] + x_diff

        min_y = y[i2] - y_diff
        max_y = y[i2] + y_diff

        line_x.append(min_x)
        line_x.append(max_x)

        line_y.append(min_y)
        line_y.append(max_y)

    
    for i3 in range(0, len(body_plot)):
        body_plot[i3].set_xdata(x)
        body_plot[i3].set_ydata(y)

        line_plot[i3].set_xdata(line_x)
        line_plot[i3].set_ydata(line_y)
    #print(i, rigid_bodies['Rigid Body 3:Marker1'][i]['time'])
    plot.pause(0.001)
'''
plot.show()
