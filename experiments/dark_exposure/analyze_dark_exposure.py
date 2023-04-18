# -*- coding: utf-8 -*-
"""
Created on Mon March  27 19:59:52 2023

plots image with scale bar

@author: kevin kim <kekim@hmc.edu>
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
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    exposure = np.zeros(50)
    intensity = np.zeros(50)
    
    # the range parameter must match exactly of the parameter in the for loop in intensityExposureCaptureLinear.py
    for i in range(0,50):
        tot=0
        exposure[i] = (i+1)
        filename = f"darkExposure{(i+1)}ms.npy"
        bayerData = np.load(filename, allow_pickle=True)
            
        # unpack the 2D bayer array data into the respective R,B,G channels.
        rgb = np.zeros(bayerData.shape + (3,), dtype=bayerData.dtype)
        
        rgb[0::2, 0::2, 0] = bayerData[0::2, 0::2] # Red
        rgb[1::2, 0::2, 1] = bayerData[1::2, 0::2] # Green
        rgb[0::2, 1::2, 1] = bayerData[0::2, 1::2] # Green
        rgb[1::2, 1::2, 2] = bayerData[1::2, 1::2] # Blue

        # extract green channel
        g = rgb[:,:,1]
        
        # remove all zeros and reshape into 2d Matrix
        g = g.flatten()[1::2].reshape(1232,3280)

        
        # strip RHS for green channel
        g = np.delete(g, np.s_[1640:3280],axis=1)
    
        intensity[i] = np.mean(g)
        
        # every 10 images show the raw image data
        if (i%10 == 0):
            showImage(g, f"Exposure: {i+1}ms")
    
    # plot intensity vs exposure time graph
    plt.scatter(exposure, intensity, label="measured intensity")
    plt.legend()
    plt.xlabel("t (exposure time [ms])")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs exposure time")
    plt.show()
    
# Function to analyzes image sets with constant exposure time
def analyzeConst():
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    exposure = np.zeros(50)
    intensity = np.zeros(50)
    stddev = np.zeros(50)
    avg = 0
    
    # the range parameter must match exactly of the parameter in the for loop in intensityExposureCaptureLinear.py
    for i in range(0,50):
        tot=0
        exposure[i] = (i)
        filename = f"darkExposure{(i)}.npy"
        bayerData = np.load(filename, allow_pickle=True)
            
        # unpack the 2D bayer array data into the respective R,B,G channels.
        rgb = np.zeros(bayerData.shape + (3,), dtype=bayerData.dtype)
        
        rgb[0::2, 0::2, 0] = bayerData[0::2, 0::2] # Red
        rgb[1::2, 0::2, 1] = bayerData[1::2, 0::2] # Green
        rgb[0::2, 1::2, 1] = bayerData[0::2, 1::2] # Green
        rgb[1::2, 1::2, 2] = bayerData[1::2, 1::2] # Blue

        # extract green channel
        g = rgb[:,:,1]
        
        # remove all zeros and reshape into 2d Matrix
        g = g.flatten()[1::2].reshape(1232,3280)

        
        # strip RHS for green channel
        g = np.delete(g, np.s_[1640:3280],axis=1)
    
        intensity[i] = np.mean(g)
        #stddev[i] = np.std(g)
        # every 10 images show the raw image data
        if (i%10 == 0):
            showImage(g, f"set: {i}")
            
    
    mean = np.mean(intensity)
    print(mean)
    # plot intensity vs exposure time graph
    plt.scatter(exposure, intensity, label="measured intensity")
    plt.axhline(y = mean, color = 'r', linestyle = '-', label="mean intensity")
    #plt.errorbar(exposure,intensity,yerr=stddev,ecolor='r',elinewidth=1, label="std. dev error")
    plt.legend()
    
    plt.xlabel("t (image set)")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs image set")
    plt.show()
    
analyzeConst()
