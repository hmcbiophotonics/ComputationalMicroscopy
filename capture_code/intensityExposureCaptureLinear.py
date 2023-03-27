# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:13:22 2023

@author: kevin
"""


# Import Libraries
from time import sleep
from picamera import PiCamera
from fractions import Fraction
import numpy as np
import picamera.array
import os
from datetime import datetime

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
framerate=Fraction(1, 6),
sleep(2)
print("Camera is Ready!")

# range parameters in for loop specifies range of exposure times.
for i in range(0,50):
    ss = int(1E3*(i+1))
    cam.shutter_speed = ss
    with picamera.array.PiBayerArray(cam, output_dims=2) as output:
        cam.capture(output, 'jpeg', bayer=True)
        np.save(os.path.join(path,f"intensityExposure{int(ss/1000)}ms"),output.array)

print("Photo captured and saved.")
# Close the camera object
cam.close()
