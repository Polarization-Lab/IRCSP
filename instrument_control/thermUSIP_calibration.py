# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 13:04:03 2021
@author: khart
"""

from flirpy.camera.boson import Boson
import numpy as np
import matplotlib.pyplot as plt
import os.path
import h5py
import time
import sys


'''USER INPUT'''
COM_cam = 'COM4'
COM_motor = 'COM9'
path = 'C:\\Users\\khart\\Documents\\IRCAM_data\\tests\\'
name = 'poltest.h5'

'''---INITIALIZE CAMERA---'''
#open camera object and set FFC to manual 
try:
    cam = Boson(COM_cam)
    cam.setup_video(device_id = 1)
    cam.set_ffc_manual()
    temp = cam.get_fpa_temperature()
    print('The FPA temp is ',temp, ' C')
except: 
    print('Could not open COM port, check camera is not in use')
    sys.exit(1)
    
#Ask user if an initical ffc is requested
ffc = input('would you like to do an initial ffc? [y,n] \n')

if ffc in ['Y', 'y', 'Yes', 'yes', 'YES']:
    print('Initiating FFC')
    cam.do_ffc()

#Ask user how many images and at what intervals 
num = int(input('How many images to take? \n'))
wait = float(input('How long to wait between images [s]? \n'))

user_notes = input('User Notes: \n')

#preallocate file size
images = np.zeros((num,256,320))
temps  = np.zeros((num))

for i in range(num):
    images[i,:,:] = cam.grab(device_id = 1)
    temps[i]      = cam.get_fpa_temperature()
    print('on image ',str(i+1), ' of ', str(num))
    time.sleep(wait)    
cam.close()

'''---DISPLAY RADIOMETRIC IMAGE---'''
plt.imshow(np.mean(images,axis = 0))
plt.title("Image Average")
plt.colorbar()
plt.show()

#save
#create hdf5 file
hf = h5py.File(path + name , 'w')
hf.create_dataset('imgs',   data=images)
hf.create_dataset('temps',  data=temps)
hf.attrs['user_notes'] = user_notes
hf.attrs['ffc'] = ffc
hf.attrs['wait'] = wait
hf.close()

