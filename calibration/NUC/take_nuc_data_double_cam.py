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


save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\NUC\\dec15\\'
name = '2imtest'

#choose the ROI
ymin = 0;
ymax = 250;
xmin = 0;
xmax = 320;


#choose wavelengths
samps    = 5;
temp1 = np.zeros(samps);temp2 = np.zeros(samps)
avgs1 = np.zeros(samps);avgs2 = np.zeros(samps)
images1   = [];images2   = []

i =0;
while i <samps:
    camera1     = Boson(port = "COM5")
    print(camera1.find_serial_device())
    image1       = camera1.grab();
    t1           = camera1.get_fpa_temperature()
    camera1.close()
    
    camera2 = Boson(port = "COM6")
    image2       = camera2.grab();
    print(camera2.find_serial_device())
    t2           = camera2.get_fpa_temperature()
    camera2.close()
   
    print('sample #'+str(i)+' temp1 is '+str(t1)+' C,  '+'temp2 is '+str(t2)+' C')
    images1.append(image1)
    temp1[i]        = t1
    avgs1[i]        = np.mean(image1)
    images2.append(image2)
   
    temp2[i]        = t2
    avgs2[i]        = np.mean(image2)
    
    i = i+1;
    if i <samps:
        time.sleep(1)
    
plt.plot(temp1,avgs1)
plt.plot(temp2,avgs2)
plt.show()


#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('images1',     data=images1)
hf.create_dataset('temp1',       data=temp1)
hf.create_dataset('images2',     data=images2)
hf.create_dataset('temp2',       data=temp2)
hf.close()

