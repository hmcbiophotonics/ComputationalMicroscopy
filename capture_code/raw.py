#!/usr/bin/python3

# Configure a raw stream and capture an image from it.
import time
import numpy as np

from picamera2 import Picamera2, Preview

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

still_config = picam2.create_still_configuration(raw={"size": picam2.sensor_resolution, "format": "SBGGR10"})
print(f"CONFIG: {picam2.sensor_resolution}")
#print(picam2.sensor_modes[3])
print(preview_config)
picam2.configure(preview_config)

picam2.start()
time.sleep(2)

raw = picam2.capture_array("raw")
raw=raw.view(np.uint16)
#raw.reshape(picam2.sensor_resolution)
print(raw.shape)
print(type(raw))
print(picam2.stream_configuration("raw"))

