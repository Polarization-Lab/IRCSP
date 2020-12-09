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
from mono_control import initialize,shutter, changeWavelength

#choose the ROI
ymin = 178;
ymax = 183;
xmin = 155;
xmax = 160;

#initialize monochromator
instr = initialize()
shutter(instr,1)

#initialize camera
camera = Boson()

#choose wavelengths
samps    = 40;
waves    = np.linspace(6,14,samps);
response = np.zeros(samps);
err      = np.zeros(samps);

i =0;
while i <samps:
    changeWavelength(instr,waves[i]);
    image       = camera.grab();
    response[i] = np.mean(image[ymin:ymax,xmin:xmax]);
    err[i]      = np.std(image[ymin:ymax,xmin:xmax]);
    i = i+1;
    
#close camera
camera.close()

plt.errorbar(waves,response,yerr=err)
plt.xlabel('Wavelength [um]')
plt.ylabel('response')
plt.show()