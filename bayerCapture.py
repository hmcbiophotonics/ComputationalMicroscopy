# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 20:30:27 2023

@author: kevin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 20:22:37 2023

@author: kevin
"""

import picamera
import picamera.array
import numpy as np
from datetime import datetime


dirPath = "Z:\\"

now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dt_string = "img " +dt_string
with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as output:
        camera.capture(output, 'jpeg', bayer=True)
        np.save("bayer", output.array)
        print(output.array.shape)