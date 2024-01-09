# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 15:47:10 2022

@author: khart
"""
from rotation.stage_commands import open_port, home_motor, move_motor_absolute
from flirpy.camera.boson import Boson
import numpy as np
import h5py
import sys
import os
from mono_control import initialize, shutter, changeWavelength

"""options for measurement"""
meas_num = 1 
wait = 1
frame_avg = 3

ymin = 0 #min 0
ymax = 256 #max 256
xmin = 0 #min 0
xmax = 320 #max 320

'''----INITIALIZE MONOCHROMATOR---'''
instr = initialize()
shutter(instr,1)

angle_step = 45;
angle_start = 0;
angle_stop = 135;
angles = list(range(angle_start,angle_stop+angle_step,angle_step));

COM_motor = 'COM13'


"""DO NOT CHANGE"""
camera1 = Boson(port='COM4')

#set FFC to manual
camera1.set_ffc_manual()

#choose wavelengths
wave_start = 7;
wave_stop = 13;
samps    = 20;
waves    = np.linspace(wave_start,wave_stop,samps); #units in microns
num_wvs = len(waves);
#can't see anything through monochromator below 7 um or past 13 um

'''----INITIALIZE MOTOR---'''
try:
    motor = open_port(COM_motor)
    home_motor(motor)
except:
    print('Could not connect to motor, exiting')
    sys.exit(1)
    
for j in range(num_wvs):
    
    changeWavelength(instr,waves[j]);
    wavename = str(waves[j]) + 'microns\\'
    save_path1 = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\Jaclyn\\mono_response\\' + wavename
    os.makedirs(save_path1)

    for a in range(angle_start,angle_stop+angle_step,angle_step):
    
        anglename = str(int(a)) +'deg.h5' #save h5 file as angle
        print('moving to ', a)
        h = move_motor_absolute(motor, a)
        print('actual angle is ',str(h), ' degree')
    
        ims1 = np.zeros((meas_num,256,320))
        temps2 = np.zeros(meas_num)
        std1 = np.zeros((meas_num,256,320))
        
        
        for i in range(meas_num):
            
            im1 = np.zeros((frame_avg,256,320))
            temps2[i] = camera1.get_fpa_temperature()
            for j in range(frame_avg):
    
                #take image
                im1[j,:,:] = camera1.grab(device_id = 1)
        
            ims1[i,:,:] = np.mean(im1,axis = 0 )
            std1[i,:,:] = np.std(im1,axis=0)
            im = ims1[i]
            
            
        #move motor
        print('completed '+ anglename)
        print('cam temp is ' + str(temps2[i]))
    
        #save
        #create hdf5 file
        hf = h5py.File(save_path1 + anglename, 'w')
        hf.create_dataset('imgs1',data=ims1)
        hf.create_dataset('std',data=std1)        
        hf.create_dataset('temp',data=temps2)
        hf.close()
        
'DARK FIELD'

shutter(instr,0)
save_path2 = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\Jaclyn\\mono_response\\darkfield\\'
os.makedirs(save_path2)
        
        
for aa in range(angle_start,angle_stop+angle_step,angle_step):
    
        anglename2 = str(int(aa)) +'deg.h5' #save h5 file as angle
        print('moving to ', aa)
        h = move_motor_absolute(motor, aa)
        print('actual angle is ',str(h), ' degree')
    
        ims2 = np.zeros((meas_num,256,320))
        temps2 = np.zeros(meas_num)
        std1 = np.zeros((meas_num,256,320))

    
        
        for i in range(meas_num):
        
            im2 = np.zeros((frame_avg,256,320))
            temps2 = camera1.get_fpa_temperature()
            for j in range(frame_avg):
    
                #take image
                im2[j,:,:] = camera1.grab(device_id = 1)
        
            ims2[i,:,:] = np.mean(im2,axis = 0 )
            std1[i,:,:] = np.std(im1,axis=0)
            im = ims2[i]
            
            
        #move motor
        print('completed '+ anglename2)
        print('cam temp is ' + str(temps2))
   
        #save
        #create hdf5 file
        hf = h5py.File(save_path2 + anglename2, 'w')
        hf.create_dataset('imgs',data=ims2)
        hf.create_dataset('temp',data=temps2)
        hf.create_dataset('std',data=std1)
        hf.close()
        
print('completed dark field')


camera1.close()
