import csv
import cv2
import matplotlib
matplotlib.use('agg')
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from matplotlib import pyplot as plot

def get_all_marker_tags(path_to_csv):
    # Takes in csv file path, returns a list of all unique marker tags
    with open(path_to_csv, newline='') as f:
        reader_obj = list(csv.reader(f))
    
    marker_tags = []
    for marker_name in reader_obj[3]:
        if (marker_name not in marker_tags) and ("Unlabeled" not in marker_name):
            marker_tags.append(marker_name)
    
    while("" in marker_tags):
        marker_tags.remove("")
    
    return marker_tags


def create_marker_data(path_to_csv, marker_tag, highlight_tag, marker_color, highlight_color, rigid_body_color):
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
                    color = highlight_color
                elif ':' not in marker_tag:
                    color = rigid_body_color
                else:
                    color = marker_color

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
                if any(marker_tag == tag for tag in highlight_tag):
                    color = highlight_color
                elif ':' not in marker_tag:
                    color = rigid_body_color
                else:
                    color = marker_color


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

                ## color data:
                if any(marker_tag == tag for tag in highlight_tag):
                    color = highlight_color
                elif ':' not in marker_tag:
                    color = rigid_body_color
                else:
                    color = marker_color

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
                if any(marker_tag == tag for tag in highlight_tag):
                    color = highlight_color
                elif ':' not in marker_tag:
                    color = rigid_body_color
                else:
                    color = marker_color


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
                       fps=120,
                       marker_color='#606060', highlight_color='#000000', rigid_body_color='#FF0000', do_system_COM=False):

    '''
    Outputs a video file of the specified format in the same directory as this file. Blocks for a long time, python be like that. 

    Inputs:
        filename:
            String: Name of the video you want to create. Be sure to include a file type in the string.
            Example: "sample_csv_data.mp4"
        path_to_csv:
            String: /path/to/data.csv   Absolute file path recommended.
        marker_tags:
            List of strings: The names of each motion sensor or rigid body. 
                            Example:
                                marker_tags = [ 
                                    'Rigid Body 1', 
                                    'Rigid Body 2', 
                                    'Rigid Body 3',
                                    'Rigid Body 1:Marker1',
                                    'Rigid Body 1:Marker4',
                                    'Rigid Body 2:Marker1', 
                                    'Rigid Body 2:Marker2', 
                                    'Rigid Body 3:Marker5', 
                                    'Rigid Body 3:Marker6'
                                ]
        start_end_links_tags:
            List of strings: The names of the markers which will be highlighted and connected by a line. Same format as marker_tags. 
                             The list is order sensitive, the lines are drawn in the order they appear in the array
    Optional Inputs (In order of importance):
        Range:
            List of floats: Default is [-0.75, 0.2]. Controls the size of the y axis in matplotlib. Use to fit the system in the displayed axis. Defualt units are in meters.
        domain:
            List of floats: Default is [-1, 1]. Controls the size of the y axis in matplotlib. Use to fit the system in the displayed axis. Defualt units are in meters
        do_system_COM:
            bool: Graphs the system's approximate center of mass if true. WARNING: This makes the graphing take a SUPER long time, since showing a trail involves plotting THOUSANDS OF POINTS PER FRAME for later frames
        fps:
            int: The fps at which the animation will play. If this argument equals the fps of the motion capture software, the animation speed will be the same as real life.
                 Changing it can be used for scuffed slowmo / timelapse
        marker_color:
            Color of any non-special motion cap sensor. Can be any matplotlib compatible color input.
        highlight_color:
            Color of sensors specifed in start_end_links_tags. Can be any matplotlib compatible color input.
        rigid_body_color:
            Color of the center of masses displayed at the links, and the system center of mass if it is drawn.
        
        If color outputs are left unspecified, they will default to colors that are mostly conventional with LRAM linkage visualizations. 

    '''
    ### Call the create marker data function to create a dictionary database
    rigid_bodies = {}
    for tag in marker_tags:
        rigid_bodies[tag], data_length = create_marker_data(path_to_csv, tag, start_end_links_tags, marker_color, highlight_color, rigid_body_color)

    links_rigid_body = []
    for tag in marker_tags:
        if not ':' in tag:
            links_rigid_body.append(tag)

    if do_system_COM:
        COM_cords = []
        for i in list(range(0, data_length - 1)):
            COM_x = []
            COM_y = []
            for link_tag in links_rigid_body:
                COM_x.append(rigid_bodies[link_tag][i]['pos_z'])
                COM_y.append(rigid_bodies[link_tag][i]['pos_x'])
            center_of_mass_x = sum(COM_x) / len(links_rigid_body)
            center_of_mass_y = sum(COM_y) / len(links_rigid_body)
            COM_cords.append([center_of_mass_x, center_of_mass_y])

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
    body_plots = []

    # Dont ask, i hate matplotlib
    for body in rigid_bodies:
        if any(center_of_mass == body for center_of_mass in links_rigid_body):
            body_plots.append(ax.plot(rigid_bodies[body][0]['pos_z'], rigid_bodies[body][0]['pos_x'], c=rigid_bodies[body][0]['color'], linestyle='', marker='.', markersize=13))
        else:
            body_plots.append(ax.plot(rigid_bodies[body][0]['pos_z'], rigid_bodies[body][0]['pos_x'], c=rigid_bodies[body][0]['color'], linestyle='', marker='.'))

    linkage = ax.plot([rigid_bodies[ends][0]['pos_z'] for ends in start_end_links_tags], [rigid_bodies[ends][0]['pos_x'] for ends in start_end_links_tags], c=highlight_color)

    if do_system_COM:
        ax.plot(COM_cords[0][0], COM_cords[0][1], c=rigid_body_color, marker='.', markersize=3)

    plot.legend(['MoCap Sensor', 'MoCap Sensor at link end/start', 'MoCap Rigid Body Position (COM)'], loc='lower right')
    legend = ax.get_legend()
    legend.legend_handles[0].set_color(marker_color)
    legend.legend_handles[1].set_color(highlight_color)
    legend.legend_handles[2].set_color(rigid_body_color)

    # Draw so that we can save each frame as an image
    plot.draw()

    # Store first frame of video
    video_data.append(np.frombuffer(f.canvas.tostring_rgb(), dtype=np.uint8))
    video_data[0] = video_data[0].reshape(f.canvas.get_width_height()[::-1] + (3,))

    print("Generating")
    for i in list(range(1, data_length-1)):

        alive = i % 100
        if alive == 0:
            print(f"Progress: %{i/data_length * 100:.1f}")
        

        for i2, (body_plot, body) in enumerate(zip(body_plots, rigid_bodies)):
            for i3 in range(0, len(body_plot)):
                body_plot[i3].set_xdata(rigid_bodies[body][i]['pos_z'])
                body_plot[i3].set_ydata(rigid_bodies[body][i]['pos_x'])
        
        for i2 in range(0, len(linkage)):
            linkage[i2].set_xdata([rigid_bodies[ends][i]['pos_z'] for ends in start_end_links_tags])
            linkage[i2].set_ydata([rigid_bodies[ends][i]['pos_x'] for ends in start_end_links_tags])

        if do_system_COM:
            ax.plot(COM_cords[i][0], COM_cords[i][1], c=rigid_body_color, marker='.', markersize=3)

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

def main():
    ###      Example Inputs      ###
    file_name = 'video_motion_capture.mp4'
    path_to_csv = 'CSV MoCap Data\Take_2023-07-06_12.25.47_AM.csv'

    start_end_links_tags = [
        'Rigid Body 3:Marker6', 
        'Rigid Body 3:Marker2',
        'Rigid Body 2:Marker4', 
        'Rigid Body 1:Marker3'
    ]
    ### Function Call ###
    marker_tags = get_all_marker_tags(path_to_csv)
    print(f"{marker_tags=}")
    create_MoCap_Video(file_name, path_to_csv, marker_tags, start_end_links_tags, do_system_COM=False) # Creates video with specifications in directory shared with this file

if __name__ == "__main__":
    main()
