# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 19:59:52 2023

plots image with scale bar

@author: kevin
"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import numpy as np

def showImage(arr, title):
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    fig.colorbar(im, ax=ax)
    fig.suptitle(title)
    plt.show()

def analyzeExp():
    exposure = np.zeros(7)
    intensity = np.zeros(7)
    
    for i in range(-3,4):
        tot=0
        exposure[i+3] = 10**i
        for j in range(10):
            filename = f"intensityExposure{10**i}ms_{j}.npy"
            bayerData = np.load(filename, allow_pickle=True)
            g = bayerData[:,:,1]
            tot = tot + np.mean(g)
        intensity[i+3] = tot/10
    
    print(exposure)
    print(intensity)
    plt.scatter(exposure, intensity, label="measured intensity")
    plt.legend()
    plt.xlabel("t (exposure time [ms])")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs exposure time")
    plt.show()
    
def analyzeLin():
    exposure = np.zeros(50)
    intensity = np.zeros(50)
    
    # the range parameter must match exactly of the parameter in the for loop in intensityExposureCaptureLinear.py
    for i in range(0,50):
        tot=0
        exposure[i] = (i+1)
        filename = f"intensityExposure{(i+1)}ms.npy"
        bayerData = np.load(filename, allow_pickle=True)
            
        # unpack the 2D bayer array data into the respective R,B,G channels.
        rgb = np.zeros(bayerData.shape + (3,), dtype=bayerData.dtype)
        
        rgb[0::2, 0::2, 0] = bayerData[0::2, 0::2] # Red
        rgb[1::2, 0::2, 1] = bayerData[1::2, 0::2] # Green
        rgb[0::2, 1::2, 1] = bayerData[0::2, 1::2] # Green
        rgb[1::2, 1::2, 2] = bayerData[1::2, 1::2] # Blue

        # extract green channel
        g = rgb[:,:,1]
        
        # remove all zeros
        g = g[g!=0].reshape(1232,3280)
        g = np.delete(g, np.s_[1640:3280],axis=1)
    
        intensity[i] = np.mean(g)
        if (i%10 == 0):
            showImage(g, f"Exposure: {i+1}ms")
    
    print(exposure)
    print(intensity)
    plt.scatter(exposure, intensity, label="measured intensity")
    plt.legend()
    plt.xlabel("t (exposure time [ms])")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs exposure time")
    plt.show()
    
analyzeLin()
