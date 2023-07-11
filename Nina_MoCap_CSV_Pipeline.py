import csv
import cv2
import matplotlib
matplotlib.use('agg')
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from matplotlib import pyplot as plot


def create_marker_data(path_to_csv, marker_tag, highlight_tag=None):
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
    if ':' in marker_tag:
        for frame in list(range(7, data_length+7)):
            try:
                # time data:
                time = float(reader_obj[frame][1])

                # color data:
                if any(marker_tag == tag for tag in highlight_tag):
                    color = 'r'
                elif ':' not in marker_tag:
                    color = 'y'
                else:
                    color = 'b'

                # rot_y data:
                y_rotation = float("NaN")

                # pos_x data:
                x_position = float(reader_obj[frame][column_num])

                # pos_y data: 
                y_position = float(reader_obj[frame][column_num + 1])

                # pos_z data:
                z_position = float(reader_obj[frame][column_num + 2])
            except ValueError:
                # time data:
                time = float('NaN')

                # color data:
                if marker_tag == highlight_tag:
                    color = 'r'
                elif ':' not in marker_tag:
                    color = 'y'
                else:
                    color = 'b'

                # rot_y data:
                y_rotation = float('NaN')

                # pos_x data:
                x_position = float('NaN')

                # pos_y data: 
                y_position = float('NaN')

                # pos_z data:
                z_position = float('NaN')

            data_frame.append(dict({'time': time, 'color': color, 'rot_y': y_rotation, 'pos_x': x_position, 'pos_y': y_position, 'pos_z': z_position}))
    else:
            
            
        for frame in list(range(7, data_length+7)):

            try:
                # time data:
                time = float(reader_obj[frame][1])

                # color data:
                if marker_tag == highlight_tag:
                    color = 'r'
                elif ':' not in marker_tag:
                    color = 'y'
                else:
                    color = 'b'

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

                # color data:
                if marker_tag == highlight_tag:
                    color = 'r'
                elif ':' not in marker_tag:
                    color = 'y'
                else:
                    color = 'b'

                # rot_y data:
                y_rotation = float('NaN')

                # pos_x data:
                x_position = float('NaN')

                # pos_y data: 
                y_position = float('NaN')

                # pos_z data:
                z_position = float('NaN')
            
            data_frame.append(dict({'time': time, 'color': color, 'rot_y': y_rotation, 'pos_x': x_position, 'pos_y': y_position, 'pos_z': z_position}))

    return data_frame, data_length

def create_MoCap_Video(file_name, 
                       path_to_csv, 
                       marker_tags, 
                       start_end_links_tags, 
                       Range=[-0.75, 0.2], 
                       domain=[-1, 1],
                       fps=120
):

    ### Call the create marker data function to create a dictionary database
    rigid_bodies = {}
    for tag in marker_tags:
        rigid_bodies[tag], data_length = create_marker_data(path_to_csv, tag, start_end_links_tags)
    
    ### Graphing
    f = plot.figure(1)
    f.set_size_inches(10, 7)
    plot.clf()

    ax = f.add_subplot(1, 1, 1)
    plot.title(f"MoCap Post Processing from: .{path_to_csv}")
    plot.xlabel("Z Postion (meters)")
    plot.ylabel("X Postion (meters)")


    plot.axis('equal')
    plot.box('on')
    ax.set_ylim(Range[0], Range[1])
    ax.set_xlim(domain[0], domain[1])

    video_data = [] # Stores sequenced image data
    x = [] # is pos_z since mocap uses y as vertical axis
    y = [] # is pos_x to place the linkage how its expected (left to right motion)
    body_plots = []

    # Dont ask, i hate matplotlib
    for body in rigid_bodies:
        if any(center_of_mass == body for center_of_mass in ['Rigid Body 1', 'Rigid Body 2', 'Rigid Body 3']):
            body_plots.append(ax.plot(rigid_bodies[body][0]['pos_z'], rigid_bodies[body][0]['pos_x'], c=rigid_bodies[body][0]['color'], linestyle='', marker='.', markersize=13))
        else:
            body_plots.append(ax.plot(rigid_bodies[body][0]['pos_z'], rigid_bodies[body][0]['pos_x'], c=rigid_bodies[body][0]['color'], linestyle='', marker='.'))

    linkage = ax.plot([rigid_bodies[ends][0]['pos_z'] for ends in start_end_links_tags], [rigid_bodies[ends][0]['pos_x'] for ends in start_end_links_tags], c='r')

    plot.legend(['MoCap Sensor', 'MoCap Sensor at link end/start', 'MoCap Rigid Body Position (COM)'], loc='lower right')
    legend = ax.get_legend()
    legend.legend_handles[0].set_color('blue')
    legend.legend_handles[1].set_color('red')
    legend.legend_handles[2].set_color('yellow')

    plot.draw() # Draw so that we can save each frame as an image

    # Store first frame of video
    video_data.append(np.frombuffer(f.canvas.tostring_rgb(), dtype=np.uint8))
    video_data[0] = video_data[0].reshape(f.canvas.get_width_height()[::-1] + (3,))

    print("Generating")
    for i in list(range(1, data_length-1)):

        alive = i % 500
        if alive == 0:
            print("")
            print("Generating", end=" ")
        
        if i % 85 == 0:
            print(".", end=" ")

        for i2, (body_plot, body) in enumerate(zip(body_plots, rigid_bodies)):
            for i3 in range(0, len(body_plot)):
                body_plot[i3].set_xdata(rigid_bodies[body][i]['pos_z'])
                body_plot[i3].set_ydata(rigid_bodies[body][i]['pos_x'])
        
        for i2 in range(0, len(linkage)):
            linkage[i2].set_xdata([rigid_bodies[ends][i]['pos_z'] for ends in start_end_links_tags])
            linkage[i2].set_ydata([rigid_bodies[ends][i]['pos_x'] for ends in start_end_links_tags])

        plot.draw() # Update the matplotlib figure

        # Add the new frame to the list of frames
        video_data.append(np.frombuffer(f.canvas.tostring_rgb(), dtype=np.uint8))
        video_data[i] = video_data[i].reshape(f.canvas.get_width_height()[::-1] + (3,))
        video_data[i] = video_data[i][:,:,::-1]
    
    # Assemble the video
    height, width, layers = video_data[1].shape #? No idea from stackoverflow

    # Create a videowriter object and feed it the images in the video_data list
    video=cv2.VideoWriter(file_name, -1, fps, (width,height))
    for images in video_data:
        video.write(images)

    cv2.destroyAllWindows()
    video.release()

###      Example Inputs      ###
file_name = '6-28-23 02.03.29 PM MoCapVideo.mp4'
path_to_csv = 'CSV MoCap Data/Take 2023-06-28 02.03.29 PM.csv'
marker_tags = [ 
    'Rigid Body 1', 
    'Rigid Body 2', 
    'Rigid Body 3',
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
    'Rigid Body 3:Marker6'
]
start_end_links_tags = [
    'Rigid Body 3:Marker6', 
    'Rigid Body 3:Marker2',
    'Rigid Body 2:Marker4', 
    'Rigid Body 1:Marker3'
]

### Function Call ###
create_MoCap_Video(file_name, path_to_csv, marker_tags, start_end_links_tags) # Creates video with specifications in directory shared with this file
