# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 13:52:34 2024

this script uses the thorlabs rotation stage to take polarized calibration measurements

"""
from rotation.stage_commands import open_port, home_motor, move_motor_absolute
from flirpy.camera.boson import Boson
from balloon_read_sensors import readsensors
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py
import sys


"""options for measurement"""
save_path = 'C:\\Users\\khart\\Documents\\wiregrid-emission\\Tungsten\\10V\\'
meas_num = 1  
#wait = 1
frame_avg = 5

angle_step = 45;
angle_start = 0;
angle_stop = 360;

COM_motor = 'COM13' 

"""DO NOT CHANGE"""
camera1 = Boson(port='COM6') #reflected/rotated camera
camera2 = Boson(port='COM5') #transmission

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

camera1.set_ffc_frame_threshold(0)
camera1.set_ffc_temperature_threshold(0)
camera2.set_ffc_frame_threshold(0)
camera2.set_ffc_temperature_threshold(0)

'''----INITIALIZE MOTOR---'''
try:
    motor = open_port(COM_motor)
    home_motor(motor)
except:
    print('Could not connect to motor, exiting')
    sys.exit(1)

for a in range(angle_start,angle_stop,angle_step):

    name = str(int(a))+'deg.h5'
    print('moving to ', a)
    h = move_motor_absolute(motor, a)
    print('actual angle is ',str(h), ' degree')

    t1s  = np.zeros(meas_num);
    t2s  = np.zeros(meas_num);
    ims1 = np.zeros((meas_num,256,320))
    ims2 = np.zeros((meas_num,256,320))
    s1 = np.zeros((meas_num,256,320)) #standard deviation per pixel
    s2 = np.zeros((meas_num,256,320))
    
    for i in range(meas_num):
        #sensordata = readsensors()
        #housing_temp = sensordata[12]
        
        # get FPA temperature 
        t1s[i] = camera1.get_fpa_temperature()
        t2s[i] = camera2.get_fpa_temperature()
        im1 = np.zeros((frame_avg,256,320))
        im2 = np.zeros((frame_avg,256,320))
        for j in range(frame_avg):
            #take image
            im1[j,:,:] = camera1.grab(device_id = 1)
            im2[j,:,:] = camera2.grab(device_id = 2)
        img1 = np.mean(im1,axis = 0)
        img2 = np.mean(im2,axis = 0)
        s1[i,:,:] = np.std(im1,axis = 0 )
        s2[i,:,:] = np.std(im2,axis = 0 )
      #  ims1[i,:,:] = im1
      #  ims2[i,:,:] = im2
        
        
    #move motor
    print('completed '+ name)
    print('cam 1 is ' + str(t1s[i]))
    print('cam 2 is ' + str(t2s[i]))
  #  print("thermistor at " + str(housing_temp))
   
    #save
    #create hdf5 file
    hf = h5py.File(save_path + name , 'w')
    
    hf.create_dataset('imgs1',  data=im1)
    hf.create_dataset('imgs2',  data=im2)
    hf.create_dataset('temps1', data=t1s)
    hf.create_dataset('temps2', data=t2s)
    hf.create_dataset('standev1', data=s1)
    hf.create_dataset('standev2',data=s2)
    hf.close()
    
    
    plt.imshow(img1)
    plt.title("Camera 1")
    plt.colorbar()
    plt.show()
    plt.imshow(img2)
    plt.title("Camera 2")
    plt.colorbar()
    plt.show()
    
    
   # fig, ax1 = plt.subplots()
    
 #   color = 'tab:red'
 #   ax1.set_ylabel('cam1',color=color)
    #ax1.plot(np.mean(im1[120:125,90:190],0), color=color)
 #   ax1.plot(ims1[i][:,10], color=color)
    #ax1.set_ylim(23730,23780)
#    ax1.tick_params(axis='y', labelcolor=color)
    
#    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
  
#    color = 'tab:blue' 
#    ax2.set_ylabel('cam2', color=color)  # we already handled the x-label with ax1
#    #ax2.plot(np.mean(im2[110:140,100:200],0), color=color)
#    ax2.plot(ims2[i][:,10], color=color)
    #ax2.set_ylim(23990,23960)
#    ax2.tick_params(axis='y', labelcolor=color)
    
#    fig.tight_layout()  # otherwise the right y-label is slightly clipped
#    plt.show()
        

    
camera1.close()
camera2.close()