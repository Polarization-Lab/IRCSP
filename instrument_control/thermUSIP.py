# -*- coding: utf-8 -*-
"""
This script will aquire and save polarized data 
Created on Mon Jun 21 13:04:03 2021
@author: khart
"""

from flirpy.camera.boson import Boson
from rotation.stage_commands import open_port, home_motor, move_motor_absolute
import numpy as np
import matplotlib.pyplot as plt
import os.path
import h5py
import time
import sys


'''USER INPUT'''
COM_cam = 'COM4'
COM_motor = 'COM9'
pol_angles = [0,45,90,135]
path = 'C:\\Users\\khart\\Documents\\IRCAM_data\\tests\\'
name = 'poltest.h5'
user_notes = 'Data was taken by : Kira'


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

'''----PROMPT FOR FFC, IMAGE NUMBER---'''
#Ask user if an initical ffc is requested
ffc = input('would you like to do an initial ffc? [y,n] \n')

if ffc in ['Y', 'y', 'Yes', 'yes', 'YES']:
    print('Initiating FFC')
    cam.do_ffc()

#Ask user how many images and at what intervals 
num = int(input('frames per analyzer position? \n'))

#check file path exists
if os.path.exists(path):
    print('\n saving data to ' , path)
else:
    print('path not found, closing camera')
    cam.close()
    sys.exit(1)

'''----INITIALIZE MOTOR---'''
try:
    motor = open_port(COM_motor)
    home_motor(motor)
except:
    print('Could not connect to motor, exiting')
    sys.exit(1)

'''---PREALLOCATE ARRAYS---'''
na = len(pol_angles)

#preallocate file size
images = np.zeros((na,256,320))
temps  = np.zeros((na))
actual_angles  = np.zeros(na)

'''---IMAGE AQUISITION LOOP---'''

for j in range(na):
    print('moving to ', pol_angles[j])
    h = move_motor_absolute(motor, pol_angles[j])
    actual_angles[j]  = h 
    ims = np.zeros((num,256,320))
    for i in range(num):
        ims[i,:,:] = cam.grab(device_id = 1)
    
    images[j,:,:] =np.mean(ims,axis = 0)
    temps[j]      = cam.get_fpa_temperature()
    print('actual angle is ',str(h), ' degree')

'''---DISPLAY RADIOMETRIC IMAGE---'''
plt.imshow(np.mean(images,axis = 0))
plt.title("Image Average")
plt.colorbar()
plt.show()

'''----SAVE AS HDF5 FILE---'''
#create hdf5 file
hf = h5py.File(path + name , 'w')
hf.create_dataset('imgs',   data=images)
hf.create_dataset('temps',  data=temps)
hf.create_dataset('set_angels',  data=pol_angles)
hf.create_dataset('actual_angles', data = actual_angles)
hf.attrs['user_notes'] = user_notes
hf.attrs['ffc'] = ffc
hf.close()

'''---CLOSE COM PORTS---'''
cam.close()
home_motor(motor)
motor.close()

