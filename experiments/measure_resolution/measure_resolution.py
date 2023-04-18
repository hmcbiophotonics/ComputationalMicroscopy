# -*- coding: utf-8 -*-
"""
Created on Wed April 5 19:59:52 2023

Plots pixel intensity over a linear slice of image.

@author: kevin kim <kekim@hmc.edu>
"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import matplotlib.patches as patches

import numpy as np

def showImage(arr, title):
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    fig.colorbar(im, ax=ax)
    fig.suptitle(title)
    plt.show()
def showImageBox(arr, title,x,y,w,h):
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    fig.colorbar(im, ax=ax)
    fig.suptitle(title)
    rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)

    plt.show()
    
def showImageWithSlice(arr,x,y, title):
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    fig.colorbar(im, ax=ax)
    fig.suptitle(title)
    plt.axvline(x=x,color='red')
    plt.axhline(y=y,color='red')
    plt.show()
    
def showLine(pix, val, xlabel, ylabel, title):
    plt.plot(pix, val, label="intensity")
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(np.arange(0,max(pix),25)) 
    plt.grid(color='r', linestyle='-', linewidth=.1)
    plt.xlim([0, max(pix)+0.5])
    plt.ylim([0, max(val)+0.5])

    plt.show()

def measure():
    
    # crop parameters
    
    # upper left crop corner X coord
    CROPX = 900 
    
    # upper left crop corner Y coord
    CROPY = 400
    
    # crop width
    CROPW = 300
    
    # crop height
    CROPH = 300
    
    # define indices of "line slices" 
    
    # y value of horizontal slice 
    H_IDX = 225
    
    # x value of vertical slice
    V_IDX = 140
    
    filename = f"bayerCapture_0.npy"
    bayerData = np.load(filename, allow_pickle=True)
        
    print(bayerData.shape)
    # unpack the 2D bayer array data into the respective R,B,G channels.
    rgb = np.zeros(bayerData.shape + (3,), dtype=bayerData.dtype)
    
    
    rgb[0::2, 0::2, 0] = bayerData[0::2, 0::2] # Red
    rgb[1::2, 0::2, 1] = bayerData[1::2, 0::2] # Green
    rgb[0::2, 1::2, 1] = bayerData[0::2, 1::2] # Green
    rgb[1::2, 1::2, 2] = bayerData[1::2, 1::2] # Blue

    # extract color channel
    r = rgb[:,:,0]
    g = rgb[:,:,1]
    b = rgb[:,:,2]
    
    bcnt = np.sum(b!=0)
    rcnt = np.sum(r!=0)
    gcnt = np.sum(g!=0)
    
    # remove all zeros and reshape into 2d Matrix
    r = rgb[:,:,0]
    r = r.flatten()[0::2].reshape(1232,3280)
    r = np.delete(r, np.s_[1640:3280],axis=1)
    
    # CENTER CROP'
    rcrop = r[CROPY:CROPY+CROPH,CROPX:CROPX+CROPW]
    showImageBox(r, "Cropped Image",CROPX,CROPY,CROPW,CROPH)
    
    # These arrays hold x,y values used to plot intensity vs exposure. Their sizes must be adjusted accordingly.
    h_pix = np.arange(rcrop.shape[1])
    h_val = rcrop[H_IDX]
    print(h_val.shape)
    print(g.shape[0])
    
    v_pix = np.arange(rcrop.shape[0])
    v_val = rcrop[:,V_IDX]
    
    showLine(h_pix,h_val, "x [px]", "intensity", f"y = {H_IDX}")
    showLine(v_pix,v_val, "y [px]", "intensity", f"x = {V_IDX}")
    showImageWithSlice(rcrop,V_IDX,H_IDX,"Image with line slices")
    
   
measure()
