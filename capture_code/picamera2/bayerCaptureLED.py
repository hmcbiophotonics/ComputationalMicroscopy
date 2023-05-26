

# Import Libraries
from time import sleep
from fractions import Fraction
import numpy as np
import os
import pprint
from datetime import datetime
import unicornhathd

from picamera2 import Picamera2, Preview
import adafruit_dotstar as dotstar
import board
# pixel show function
def showPixel(x,y):
    
    unicornhathd.clear()
    unicornhathd.set_pixel(x,y,255,0,0)
    unicornhathd.show()

# LED position vectors
xloc = [ 7,  8,  9,  9,  8,  7,  7,  7,  8,  9, 10, 10, 10, 10,  9,  8,  7,  6,
  6,  6,  6,  6,  7,  8,  9, 10, 11, 11, 11, 11, 11, 11, 10,  9,  8,  7,
  6,  5,  5,  5,  5,  5,  5,  5,  6,  7,  8,  9, 10, 11, 12, 12, 12, 12,
 12, 12, 12, 12, 11, 10,  9,  8,  7,  6,  5,  4,  4,  4,  4,  4,  4,  4,
  4,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 13, 13, 13, 13, 13, 13, 13,
 13, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  3,  3,  3,  3,  3,  3,
  3,  3,  3,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 14, 14, 14,
 14, 14, 14, 14, 14, 14, 14, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,
  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  4,  5,  6,
  7,  8,  9, 10, 11, 12, 13, 14, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,
 15, 15, 15, 15, 14, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,
  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  3,  4,  5,
  6,  7,  8,  9, 10, 11, 12, 13, 14]

yloc=[ 7,  7,  7,  8,  8,  8,  7,  6,  6,  6,  6,  7,  8,  9,  9,  9,  9,  9,
  8,  7,  6,  5,  5,  5,  5,  5,  5,  6,  7,  8,  9, 10, 10, 10, 10, 10,
 10, 10,  9,  8,  7,  6,  5,  4,  4,  4,  4,  4,  4,  4,  4,  5,  6,  7,
  8,  9, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10,  9,  8,  7,  6,  5,
  4,  3,  3,  3,  3,  3,  3,  3,  3,  3,  3,  4,  5,  6,  7,  8,  9, 10,
 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 10,  9,  8,  7,  6,
  5,  4,  3,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  3,  4,  5,
  6,  7,  8,  9, 10, 11, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13,
 13, 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  1,  1,  1,  1,
  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10,
 11, 12, 13, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14,
 13, 12, 11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1,  0,  0,  0,  0,  0,
  0,  0,  0,  0,  0,  0,  0,  0,  0] 

# LED array size
arraysize=15

# exposure time in microseconds
EXP = 160000

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

# configure raw capture
still_config = cam.create_still_configuration(raw={"size": cam.sensor_resolution, "format": "SRGGB10"})
cam.configure(still_config)

# set exposure time
cam.set_controls({"ExposureTime": int(EXP)})

# disable auto white balance gain (I'm assuming AWB is a postprocessing algorithm)
cam.set_controls({"AnalogueGain":1, "ColourGains":(1.0,1.0)})

# start the camera
cam.start()

# range parameters in for loop specifies range of exposure times.
for i in range(0,arraysize**2):
    print(f"Image {i} out of {arraysize**2}")
    
    #  show pixel
    showPixel(xloc[i],yloc[i])
    
    # wait briefly for pixel to be shown
    sleep(.01)

    # capture raw bayer array
    raw=cam.capture_array("raw").view(np.uint16)
    
    # save the image
    np.save(os.path.join(path,f"bayerCapture_{i}"),raw)

print(f"written to folder {path}")

# Close the camera object
cam.stop()
cam.close()
