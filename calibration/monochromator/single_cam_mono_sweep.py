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
from mono_control import initialize,shutter, changeWavelength

save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\mono_data\\'
name = 'cam1_test'

#choose the ROI
ymin = 0;
ymax = 250;
xmin = 0;
xmax = 320;

#initialize monochromator
instr = initialize()
shutter(instr,1)

#initialize camera
camera = Boson()

#choose wavelengths
samps    = 80;
waves    = np.linspace(6,14,samps);
response = np.zeros(samps);
err      = np.zeros(samps);
images   = [];

i =0;
while i <samps:
    changeWavelength(instr,waves[i]);
    image       = camera.grab();
    images.append(image)
    response[i] = np.mean(image[ymin:ymax,xmin:xmax]);
    err[i]      = np.std(image[ymin:ymax,xmin:xmax]);
    i = i+1;
    
#close camera
camera.close()

plt.plot(waves,response,'.')
plt.xlabel('Wavelength [um]')
plt.ylabel('response')
plt.show()

#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('images',     data=images)
hf.create_dataset('response',   data=response)
hf.create_dataset('std',        data=err)
hf.create_dataset('wavelengths',data=waves)
hf.close()

