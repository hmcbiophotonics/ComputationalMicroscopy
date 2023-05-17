# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:13:22 2023

@author: kevin
"""
#NOTE: With center LED RED with brightness of .040, the captured image saturates out at 3.4ms.

# Import Libraries
from time import sleep
from picamera import PiCamera
from fractions import Fraction
import numpy as np
import picamera.array
import os
from datetime import datetime

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
cam = PiCamera()


cam.exposure_mode = "off"
g = cam.awb_gains

#disable auto white balance gain (I'm assuming AWB is a postprocessing algorithm)
cam.awb_mode = "off"
cam.awb_gains=g

#set a slow framerate
cam.framerate=Fraction(1, 10)
sleep(2)
print("Camera is Ready!")

# range parameters in for loop specifies range of exposure times.
for i in range(30,40):
    # exposure time will be 100ms
    ss = int(1E2*i)
    cam.shutter_speed = ss
    print(f"Taking image at {float(i/10)} ms exposure...")
    with picamera.array.PiBayerArray(cam, output_dims=2) as output:
        cam.capture(output, 'jpeg', bayer=True)
        if np.max(output.array[1::2,1::2]) >= 1023:
            print(f"SATURATED OUT AT {float(i/10)} ms with MAX of {np.max(output.array)}")
            break

print("done.")
# Close the camera object
cam.close()
