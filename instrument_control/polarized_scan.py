#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 09:07:46 2021

@author: kirahart

this script uses the thorlabs rotation stage to take polarized calibration measurements
it requires the IRCAM conda enviroment 
"""
import thorlabs_apt as apt
from flirpy.camera.boson import Boson
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time
import h5py


"""options for measurement"""
save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\NUC\\may19\\polarized\\'
meas_num = 10  #number of measurements to average over
wait = .1 #time between samples 

angle_step = 1;
angle_start = 0;
angle_stop = 360;

"""DO NOT CHANGE"""
camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

#SET UP MOTOR
motor = apt.Motor(83830282)

#set velocity parameters to be maximum
[minv,a, v] = motor.get_velocity_parameters()
[maxa,maxv] = motor.get_velocity_parameter_limits()

print('homing motor')
motor.set_velocity_parameters(minv,maxa,maxv)
motor.move_home(True)

for a in range(angle_start,angle_stop,angle_step):

    name = str(int(a))+'deg.h5'
    print('starting '+ name)

    t1s  = np.zeros(meas_num);
    t2s  = np.zeros(meas_num);
    ims1 = np.zeros((meas_num,256,320))
    ims2 = np.zeros((meas_num,256,320))
    
    for i in range(meas_num):
        # get FPA temperature 
        t1s[i] = camera1.get_fpa_temperature()
        t2s[i] = camera2.get_fpa_temperature()
        
        
        #take image
        im1 = camera1.grab(device_id = 1)
        im2 = camera2.grab(device_id = 2)
    
    
        ims1[i,:,:] = im1
        ims2[i,:,:] = im2
    
        time.sleep(wait)
        
    #move motor
    print('completed '+ name)
    print('cam 1 is ' + str(t1s[i]))
    print('cam 2 is ' + str(t2s[i]))
    motor.move_by(angle_step) 
    
    #save
    #create hdf5 file
    hf = h5py.File(save_path + name , 'w')
    hf.create_dataset('imgs1',  data=ims1)
    hf.create_dataset('imgs2',  data=ims2)
    hf.create_dataset('temps1', data=t1s)
    hf.create_dataset('temps2', data=t2s)
    hf.close()
    
    '''plot slice'''
    fig, ax1 = plt.subplots()
    
    color = 'tab:red'
    ax1.set_ylabel('cam1',color=color)
    ax1.plot(np.mean(im1[135:165,100:200],0), color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    
    color = 'tab:blue' 
    ax2.set_ylabel('cam2', color=color)  # we already handled the x-label with ax1
    ax2.plot(np.mean(im2[110:140,100:200],0), color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
        
    time.sleep(5)
    
camera1.close()
camera2.close()
