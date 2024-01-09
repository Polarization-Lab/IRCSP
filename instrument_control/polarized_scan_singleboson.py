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
camera1 = Boson(port='COM29')

#set FFC to manual
camera1.set_ffc_manual()

camera1.set_ffc_frame_threshold(0)
camera1.set_ffc_temperature_threshold(0)


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
    ims1 = np.zeros((meas_num,256,320))
    s1 = np.zeros((meas_num,256,320)) #standard deviation per pixel
    
    for i in range(meas_num):

        
        # get FPA temperature 
        t1s[i] = camera1.get_fpa_temperature()
        im1 = np.zeros((frame_avg,256,320))
        for j in range(frame_avg):
            #take image
            im1[j,:,:] = camera1.grab(device_id = 1)
        img1 = np.mean(im1,axis = 0)
        s1[i,:,:] = np.std(im1,axis = 0 )

        
    #move motor
    print('completed '+ name)
    print('camera is ' + str(t1s[i]))
   
    #save
    #create hdf5 file
    hf = h5py.File(save_path + name , 'w')

    ''' Potential Code, DO NOT RUN '''
  #  initial_aoi_count = 5
  #  degree_count = 4
  #
  #
  #  with h5py.File(''C:\\Users\\khart\\Documents\\IRCSP2_data\\Regolith\Highlands', "a") as hf:
  #     for aoi in range(aoi_range_values):
  #         aoi_group_name = f"AOI{aoi}"
  #         if aoi_group_name not in hf:
  #             aoi_group = hf.create_group(aoi_group_name)
  #         else:
  #             aoi_group = hf[aoi_group_name]
  #
  #         for degree in range(degree_range_values)
  #             degree_group_name = f"{degree}deg"
  #             if degree_group_name not in aoi_group:
  #                 degree_group = aoi_group.create_group(degree_group_name)
  #             else:
  #                 degree_group = aoi_group[degree_group_name]
  #             
  #             while True:
  #                 try:
  #                     new_image = camera.grab(device_id = 1)
  #                     if "raw_image" not in degree__group:
  #                         degree_group.create_dataset("raw_image", data=new_image, maxshape=(None, *new_image.shape), dtype="u2")
  #                         degree_group.create_dataset("mean", data=new_image, maxshape=(None, *new_image.shape), dtype="f4")
  #                         degree_group.create_dataset("standard_deviation", data=new_image, maxshape=(None, *new_image.shape), dtype="f4")
  #                     else:
  #                         raw_image = degree_group["raw_image"]
  #                         mean = degree_group["mean"]
  #                         std_dev = degree_group["standard_deviation"]
  #                         
  #                         current_image_count = raw_image.shape[0]
  #                         raw_image.resize(current_image_count + 1, axis = 0)
  #                         mean.resize(current_image_count + 1, axis = 0)
  #                         std_dev.resize(current_image_count + 1, axis = 0)
  #
  #                         raw_image[current_image_count, :, :] = new_image
  #                         mean[current_image_count, :, :] = np.mean(new_image)
  #                         std_dev[current_image_count, :, :] = np.std(new_image)
  #
  #                     print(f"Appended image to {hf}/{aoi_group_name}/{degree_group_name}")
  #                     time.sleep(.1)
  #
  #                 ''except KeyboardInterrupt:
  #                    break''
  #  camera.close()
  #
  #
  #     import serial
  #     import time
  #     serial_port = "/dev/ttyUSB0" -replace with actual serial port name
  #     ser = serial.Serial(serial_port, 9600, timeout = 1)
  #     
  #     def move_servo_to_position(position_degrees)
  #         #calculate and send the command to move servo
  #         command = f"MOVE {position_degrees}\r\n"
  #         ser.write(command.encode())
  #         ser.readline() #read and discard any response
  #
  #     def set_home_position():
  #         command = "SET HOME 90\r\n"
  #         ser.write(command.encode())
  #         ser.readline() #read and discard any response
  #
  #     while True:
  #         try:
  #             desired_position_degrees = float(input("Enter the desired position (degrees): "))
  #             move_servo_to_position(desired_position_degrees)
  #             time.sleep(''time to put motor to position'')
  #         except KeyboardInterrupt:
  #             print("Control interrupted")
  #             break
  #
  #     ser.close()
  
    hf.create_dataset('imgs1',  data=im1)
    hf.create_dataset('temps1', data=t1s)
    hf.create_dataset('standev1', data=s1)
    hf.close()
    
    
    plt.imshow(img1)
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
