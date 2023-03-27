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

# Create camera object
cam = PiCamera()

# Camera warm-up time
sleep(2)
print("Camera is ready!")
#Capture the a sequence of dark images

cam.exposure_mode = "off"
g = cam.awb_gains

#disable auto white balance gain (I'm assuming AWB is a postprocessing algorithm)
cam.awb_mode = "off"
cam.awb_gains=g

#set a slow framerate
framerate=Fraction(1, 6),
sleep(30)

for i in range(-3,4):
    ss = int(1E3 * 10**(i))
    cam.shutter_speed = ss
    for j in range():
        with picamera.array.PiBayerArray(cam) as output:
            cam.capture(output, 'jpeg', bayer=True)
            np.save(f"intensityExposure{10**i}ms_{j}",output.array)

print("Photo captured and saved.")
# Close the camera object
cam.close()
