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
from mono_control import initialize, shutter, changeWavelength



#choose the ROI
#choose image area where monochromator slit is 
ymin = 85 #min 0
ymax = 140 #max 256
xmin = 120 #min 0
xmax = 175 #max 320

#initialize monochromator
instr = initialize()
shutter(instr,1)

save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\Jaclyn\\mono_response\\spectral\\'
name = 'response'

#initialize camera
camera = Boson(port='COM4') #turn on camera
#COM4 is single FLIR boson camera

#choose wavelengths
samps    = 100;
waves    = np.linspace(7,13,samps); #units in microns
#can't see anything through monochromator below 7 um or past 13 um
response = np.zeros(samps);
err      = np.zeros(samps);
temps    = np.zeros(samps);
images   = [];

i =0;
while i <samps:
    changeWavelength(instr,waves[i]);
    image       = camera.grab(device_id = 1);
    temps[i] = camera.get_fpa_temperature()
    print('cam temp is ' + str(temps[i]))
    images.append(image)
    response[i] = np.mean(image[ymin:ymax,xmin:xmax]);
    err[i]      = np.std(image[ymin:ymax,xmin:xmax]);
    i = i+1;
    

plt.plot(waves,response,'.')
plt.xlabel('Wavelength [um]')
plt.ylabel('response')
plt.show()

#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('images',     data=images)
hf.create_dataset('temps',data=temps)
hf.create_dataset('std',        data=err)
hf.create_dataset('wavelengths',data=waves)

hf.close()

'DARK FIELD'

shutter(instr,0)

save_path2 = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\Jaclyn\\mono_response\\spectral\\'
name2 = 'darkfield'


#choose wavelengths
samps    = 100;
waves    = np.linspace(7,13,samps); #units in microns
#can't see anything through monochromator below 7 um or past 13 um
darkfieldresponse = np.zeros(samps);
err      = np.zeros(samps);
temps    = np.zeros(samps);
images   = [];

i =0;
while i <samps:
    changeWavelength(instr,waves[i]);
    image       = camera.grab(device_id = 1);
    temps[i] = camera.get_fpa_temperature()
    print('cam temp is ' + str(temps[i]))
    images.append(image)
    darkfieldresponse[i] = np.mean(image[ymin:ymax,xmin:xmax]);
    err[i]      = np.std(image[ymin:ymax,xmin:xmax]);
    i = i+1;
    
#close camera
camera.close()

plt.plot(waves,darkfieldresponse,'.')
plt.xlabel('Wavelength [um]')
plt.ylabel('response')
plt.show()

#create hdf5 file
hf = h5py.File(save_path2 + name2 + '.h5', 'w')
hf.create_dataset('images',     data=images)
hf.create_dataset('std',        data=err)
hf.create_dataset('wavelengths',data=waves)

hf.close()

