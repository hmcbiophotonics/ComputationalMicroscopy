

# Import Libraries
from time import sleep
from picamera import PiCamera
from fractions import Fraction
import numpy as np
import picamera.array
import os
from datetime import datetime
import adafruit_dotstar as dotstar
import board
# pixel show function
def showPixel(x,y):
    N_dots = 8*8
    dots = dotstar.DotStar(board.SCK, board.MOSI, N_dots, brightness = 0.040)
    led_idx = int(8*x + y)
    dots[led_idx] = (255,0,0)
xloc=[2, 3, 4, 4, 3, 2, 2, 3, 4, 5, 5, 5, 5, 4, 3, 2, 1, 1, 1, 1, 1, 2, 3,
 4, 5, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4,
 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1,0] 
yloc = [3, 3, 3, 4, 4, 4, 2, 2, 2, 2, 3, 4, 5, 5, 5, 5, 5, 4, 3, 2, 1, 1, 1, 1, 1,
 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7,7]

arraysize=8
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
for i in range(0,arraysize**2):
    showPixel(xloc[i],yloc[i])
    # exposure time will be 100ms
    cam.shutter_speed = int(1E2*(33))
    with picamera.array.PiBayerArray(cam, output_dims=2) as output:
        cam.capture(output, 'jpeg', bayer=True)
        np.save(os.path.join(path,f"bayerCapture_{i}"),output.array)

print("Photo captured and saved.")
# Close the camera object
cam.close()
