# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 11:24:49 2021

@author: khart
"""
from flirpy.camera.boson import Boson
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import h5py




#initialize camera
camera = Boson()
camera.set_ffc_manual()
wait = 5
frames = 100

def take_image(frames):
    image = np.zeros([frames,256,320])
    for i in range(frames):
        im = camera.grab(device_id = 1)
        image[i] = im
    return(np.mean(image,axis= 0))    

plt.imshow(take_image(3))

camera.close()