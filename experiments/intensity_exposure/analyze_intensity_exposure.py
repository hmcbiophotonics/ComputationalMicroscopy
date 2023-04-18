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
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    exposure = np.zeros(50)
    intensity = np.zeros(50)
    stddev = np.zeros(50)
    
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
        
        # remove all zeros and reshape into 2d Matrix
        g = g[g!=0].reshape(1232,3280)
        
        # strip RHS for green channel
        g = np.delete(g, np.s_[1640:3280],axis=1)
        intensity[i] = np.mean(g)
        stddev[i] = np.std(g)
        
        # every 10 images show the raw image data
        if (i%10 == 0):
            showImage(g, f"Exposure: {i+1}ms")
    
    # plot intensity vs exposure time graph
    plt.scatter(exposure, intensity, label="measured intensity")
    xanalytic = np.arange(35)
    yanalytic = xanalytic*1.15+64
    
    #plt.plot(xanalytic,yanalytic, color='red', label="y=1.15x+65")
    plt.errorbar(exposure,intensity,yerr=stddev,ecolor='r',elinewidth=1, label="std. dev error")
    plt.legend()
    plt.xlabel("t (exposure time [ms])")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs exposure time (diffuser)")
    plt.show()
    
def analyzeLinR():
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    exposure = np.zeros(100)
    intensity = np.zeros(100)
    stddev = np.zeros(100)
    
    # the range parameter must match exactly of the parameter in the for loop in intensityExposureCaptureLinear.py
    for i in range(0,100):
        tot=0
        exposure[i] = (i+1)
        filename = f"intensityExposure{10+(i+1)}ms.npy"
        bayerData = np.load(filename, allow_pickle=True)
            
        # unpack the 2D bayer array data into the respective R,B,G channels.
        rgb = np.zeros(bayerData.shape + (3,), dtype=bayerData.dtype)
        rgb[0::2, 0::2, 0] = bayerData[0::2, 0::2] # Red
        rgb[1::2, 0::2, 1] = bayerData[1::2, 0::2] # Green
        rgb[0::2, 1::2, 1] = bayerData[0::2, 1::2] # Green
        rgb[1::2, 1::2, 2] = bayerData[1::2, 1::2] # Blue

        # extract red channel
        g = rgb[:,:,0]     
        g = g.flatten()[0::2].reshape(1232,3280)
        g = np.delete(g, np.s_[1640:3280],axis=1)
        intensity[i] = np.mean(g)
        stddev[i] = np.std(g)
        

        if (np.max(g[300:800,600:1200])>=1023):
            print(f"{filename} has SATURATED")
        # every 10 images show the raw image data
        if (i%10 == 0):
            showImage(g, f"Exposure: {i+1}ms")
    
    # plot intensity vs exposure time graph
    plt.scatter(exposure, intensity, label="measured intensity")
    xanalytic = np.arange(35)
    yanalytic = xanalytic*1.15+64
    
    #plt.plot(xanalytic,yanalytic, color='red', label="y=1.15x+65")
    plt.errorbar(exposure,intensity,yerr=stddev,ecolor='r',elinewidth=1, label="std. dev error")
    plt.legend()
    plt.xlabel("t (exposure time [ms])")
    plt.ylabel("mean intensity of green channel")
    plt.title("intensity vs exposure time (diffuser)")
    plt.show()
    
    
    
def analyzeLinCropR(cropx,cropy):
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    exposure = np.zeros(100)
    intensity = np.zeros(100)
    stddev = np.zeros(100)
    
    # the range parameter must match exactly of the parameter in the for loop in intensityExposureCaptureLinear.py
    for i in range(0,100):
        tot=0
        exposure[i] = (i+1)
        filename = f"intensityExposure{10+(i+1)}ms.npy"
        bayerData = np.load(filename, allow_pickle=True)
            
        # unpack the 2D bayer array data into the respective R,B,G channels.
        rgb = np.zeros(bayerData.shape + (3,), dtype=bayerData.dtype)
        rgb[0::2, 0::2, 0] = bayerData[0::2, 0::2] # Red
        rgb[1::2, 0::2, 1] = bayerData[1::2, 0::2] # Green
        rgb[0::2, 1::2, 1] = bayerData[0::2, 1::2] # Green
        rgb[1::2, 1::2, 2] = bayerData[1::2, 1::2] # Blue

        # extract red channel
        g = rgb[:,:,0]
        g = g.flatten()[0::2].reshape(1232,3280)
        g = np.delete(g, np.s_[1640:3280],axis=1)

        
        # strip RHS for green channel
       # g = np.delete(g, np.s_[1640:3280],axis=1)
        
        #crop
        y,x = g.shape
        startx = x//2-(cropx//2)
        starty = y//2-(cropy//2)    
        g=g[starty:starty+cropy,startx:startx+cropx]
        
        intensity[i] = np.mean(g)
        stddev[i] = np.std(g)
        gcrop=g[300:800,600:1200]
        
        if (np.max(g)>=1023):
            print(f"{filename} has SATURATED")
        
        # every 10 images show the raw image data
        if (i%10 == 0):
            showImage(g, f"Exposure: {10+(i+1)}ms")
    
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
analyzeLinR()
