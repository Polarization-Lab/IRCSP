# -*- coding: utf-8 -*-
"""
single_cam_mono_sweep
Created on Wed Dec  9 13:12:18 2020

This script will sweep over wavelength on the monochomator
for a single measurement configuration.

This includes image capture for a single camera (no MS)
And a single polarization state (unpol, H,V, ect)
Output will be saved as a hdf5 file 
Uses flirpy, make sure enviroment is open
uses python-usbtmc

@author: khart
"""
from flirpy.camera.boson import Boson
import matplotlib.pyplot as plt 
import numpy as np
import h5py
import time


#initialize camera
camera1 = Boson(port = "COM5")
camera2 = Boson(port = "COM6")

print(camera1.find_video_device())
print(camera2.find_video_device())
    
#close camera
camera1.close()
camera2.close()

