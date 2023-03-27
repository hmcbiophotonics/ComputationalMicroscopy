# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 19:59:52 2023

plots image with scale bar

@author: kevin
"""


import matplotlib.pyplot as plt
fig, ax = plt.subplots(nrows=1,ncols=1)
im_data = plt.imread(f"hello_raspberry.jpg")
him = ax.imshow(im_data)

