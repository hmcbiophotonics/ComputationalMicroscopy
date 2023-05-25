# -*- coding: utf-8 -*-
"""
Created on Tue May 16 18:08:41 2023

@author: kevin
"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import numpy as np
import scipy.io


    
def convert(cropx,cropy):
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    exposure = np.zeros(100)
    intensity = np.zeros(100)
    stddev = np.zeros(100)
    imstack = np.zeros((1232,1640,64))
    
    # the range parameter must match exactly of the parameter in the for loop in intensityExposureCaptureLinear.py
    for i in range(0,63):
        tot=0
        exposure[i] = (i+1)
        filename = f"bayerCapture_{i}.npy"
        bayerData = np.load(filename, allow_pickle=True)
            
        # unpack the 2D bayer array data into the respective R,B,G channels.
        im_red = bayerData[1::2,1::2]
        imstack[:,:,i]=im_red
        
    scipy.io.savemat('test.mat', {'imlow_HDR': imstack})
    # plot intensity vs exposure time graph
    plt.scatter(exposure, intensity, label="measured intensity")
    xanalytic = np.arange(50)
    yanalytic = xanalytic*14.5+64
    
    plt.errorbar(exposure,intensity,yerr=stddev,ecolor='r',elinewidth=1, label="std. dev error")
    plt.plot(xanalytic,yanalytic, color='purple', label="y=14.5x+65", zorder=3)
    plt.legend()
    plt.xlabel("t (exposure time [10 ms])")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs exposure time (diffuser)")
    plt.show()
convert(512,512)
