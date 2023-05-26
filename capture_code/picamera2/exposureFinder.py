# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:13:22 2023

@author: kevin
"""
#NOTE: Image saturates out at ~162ms for the 16x16 array on the LEGO setup.

# Import Libraries
from time import sleep
from fractions import Fraction
import numpy as np
import os
import pprint
from datetime import datetime

from picamera2 import Picamera2, Preview

#exposure time in microseconds
EXP = 1000 

# Configure image capture folder path
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
cwd = os.getcwd()
path = os.path.join(cwd,dt_string)
    
# Create the directory 
try: 
    os.mkdir(path) 
except OSError as error: 
    print(error)  
    
# Create camera object
cam = Picamera2()

# print sensor modes
pprint.pprint(cam.sensor_modes)

still_config = cam.create_still_configuration(raw={"size": cam.sensor_resolution, "format": "SRGGB10"})
cam.configure(still_config)

#disable auto white balance gain (I'm assuming AWB is a postprocessing algorithm)
cam.set_controls({"AnalogueGain":1, "ColourGains":(1.0,1.0)})


#set a slow framerate
cam.start()
print("Camera is Ready!")

# range parameters in for loop specifies range of exposure times.
for i in range(1500,1800,10):
    # exposure time will be 100ms
    ss = int(1E2*i)
    cam.set_controls({"ExposureTime": ss})
    minerr = ss*.002
    print(ss)
    while (abs(int(cam.capture_metadata()["ExposureTime"]) - ss)) > minerr:
        print("Delta: ", int(cam.capture_metadata()["ExposureTime"]) - ss)
        print("Minerr:", minerr)
    print(f"Taking image at {float(i/10)} ms exposure...")
    raw=cam.capture_array("raw").view(np.uint16)
    metadata=cam.capture_metadata()
    print("actual exposure time: ", metadata["ExposureTime"])
    print("max: ", np.max(raw))
    if np.max(raw[1::2,1::2]) >= 1023:
        print(f"SATURATED OUT AT {float(i/10)} ms with MAX of {np.max(raw)}")
        break

print("done.")
# Close the camera object
cam.stop()
cam.close()

