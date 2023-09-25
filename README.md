# Motion Capture Post-Processing Overview
Post-processing repository to support LRAM/salp group. Motion capture sensors output to a csv file, the csv file is read by python, and then uses matplotlib to create frames that are compiled into a 120fps video using python-opencv.

# Usage
Edit parameters in the `main()` function of `MoCap_CSV_pipeline.py`. This allows you to enter the name of the created video, the relative path to the csv file, and motion capture sensor names that will be highlighted and connected with a line. View the `create_MoCap_Video` function to see optional inputs that control the range, domain, fps, sensor color, highlight color, and rigid body color.  While matplotlib is currently setup to graph on a 2D plane, the data transfer from the csv to python objects includes all three axis of positional data.  

# Example Output


https://github.com/thomazach/mocap-postprocessing/assets/86134403/de4c82f1-a93c-41a6-98d9-99fad3d3b349





https://github.com/thomazach/mocap-postprocessing/assets/86134403/b69eb922-49fc-4422-ba21-980497f4b6ea




# Data Handling and Transparency
### Missing Data
The motion capture setup being used can capture at 120fps. Having a large number of motion capture sensors at this refresh rate will sometimes cause sensor values to not have an entry in the csv. If this happens, the missing sensor will not be displayed for the frames(times) in which the data is missing. This can be seen as a "flickering" in videos. 

### Center of Mass Representation
The center of mass feature calculates the center of mass of all of the rigid bodies (not the motion capture sensors). It assumes:
- The mass of each rigid body is the same
- The rigid body center assigned by the motion capture system is a good approximation of the actual center of mass 

# Disclaimers/Issues
- This system was developed on windows 10 and has run into problems on other OS.
- Not optimized for perfomrance
   - Data stored throughout process, instead of being accessed on a per-frame basis
   - matplotlib is not built for 120 fps rendering
       - Doing a mass threading operation per-frame isn't possible because the center of mass feature requires all previous center of mass points from old frames to be placed in the next frame

