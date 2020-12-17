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


#choose the ROI
ymin = 100;
ymax = 250;
xmin = 100;
xmax = 200;



camera1     = Boson()
print(camera1.find_serial_device())
image1       = camera1.grab();
t1           = camera1.get_fpa_temperature()
camera1.close()

print('cam temp is '+ str(t1) + ' C')

plt.matshow(image1[xmin:xmax,ymin:ymax])
plt.colorbar()
plt.show()




