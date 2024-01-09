#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 09:07:46 2021

@author: kirahart

this script uses the thorlabs rotation stage to take polarized calibration measurements
it requires the IRCAM conda enviroment 
"""
from rotation.stage_commands import open_port, home_motor, move_motor_absolute
from flirpy.camera.boson import Boson
from mono_control import initialize, shutter, changeWavelength
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py
import sys


"""options for measurement"""
save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Calibration\\'
meas_num = 3  #number of measurements to average over
frame_avg = 10

angle_stop =350;
angle_start = 0;
angle_step = 35;

COM_motor = 'COM13'

"""DO NOT CHANGE"""
camera1 = Boson(port='COM6') #reflected/rotated camera
camera2 = Boson(port='COM5') #transmission

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

#initialize monochromator
instr = initialize()
shutter(instr,1)

'''----INITIALIZE MOTOR---'''
try:
    motor = open_port(COM_motor)
    home_motor(motor)
except:
    print('Could not connect to motor, exiting')
    sys.exit(1)

angles = np.linspace(angle_start,angle_stop,angle_step)
for w in np.linspace(7.5,10,120):
    changeWavelength(instr,w);
    ims1 = np.zeros((angle_step,meas_num,256,320))
    ims2 = np.zeros((angle_step,meas_num,256,320))
    for aa in range(len(angles)) :
        a = angles[aa]
        name = str(int(a))
        print('moving to ', a)
        h = move_motor_absolute(motor, a)
        print('actual angle is ',str(h), ' degree')
    
        t1s  = np.zeros(meas_num);
        t2s  = np.zeros(meas_num);
        
        for i in range(meas_num):
            
            # get FPA temperature 
            t1s[i] = camera1.get_fpa_temperature()
            t2s[i] = camera2.get_fpa_temperature()
            im1 = np.zeros((frame_avg,256,320))
            im2 = np.zeros((frame_avg,256,320))
            for j in range(frame_avg):
    
                #take image
                im1[j,:,:] = camera1.grab(device_id = 1)
                im2[j,:,:] = camera2.grab(device_id = 2)
        
            im1 = np.mean(im1,axis = 0)
            im2 = np.mean(im2,axis = 0)
            ims1[aa,i,:,:] = im1
            ims2[aa,i,:,:] = im2
    
        #move motor
        print('completed '+ name)
     
        #save
        #create hdf5 file
        fig, ax = plt.subplots(2,1)
        ax[0].imshow(im1[100:190,105:195])
        ax[1].imshow(im2[80:170,130:220])
        plt.show()
            
    hf = h5py.File(save_path + str(w) +'.h5', 'w')
    hf.create_dataset( 'imgs1',  data=ims1)
    hf.create_dataset('imgs2',  data=ims2)
    hf.create_dataset( 'temps1', data=t1s)
    hf.create_dataset('temps2', data=t2s)
    hf.create_dataset( 'angle_start', data=angle_start)
    hf.create_dataset( 'angle_stop', data=angle_stop)
    hf.create_dataset( 'angle_step', data=angle_step)
    hf.create_dataset( 'wavelength', data=w)
    hf.close()
            


    
camera1.close()
camera2.close()
instr.close()
motor.close()
