# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 09:40:34 2023

@author: jaclyn
"""

from   flirpy.camera.boson import Boson 
from balloon_read_sensors import readsensors
import matplotlib.pyplot as plt
import numpy as np
import h5py
import time
from TEC_set_temp import changetemp

#cam1 35.1
#cam2 34.7


"""options for measurement"""

save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP1\\Fall2023\\acktar\\'
meas_num = 1  #number of measurements 
frames = 10
#run1 is good, need run 2 and 3 to start around 30C

"""DO NOT CHANGE"""
camera1 = Boson(port='COM15') #reflected/rotated camera
camera2 = Boson(port='COM5') #transmission

temps = [18.0,18.5,19.0,19.5,20.0,20.5,21.0,21.5,22.0,22.5,23.0,23.5,24.0,24.5,25.0];

#set FFC to manual
camera1.set_ffc_manual() # set to manual 
camera2.set_ffc_manual()

k=236;

for t in range(len(temps)):
    changetemp(temps[t])
    print('TEC changed to ' + str(temps[t]))
    for n in range(30):
        name = 'Capture' + str(k)
        
        t1s  = np.zeros(meas_num); #create empty arrays for variables 
        t2s  = np.zeros(meas_num);
        ims1 = np.zeros((meas_num,256,320))
        ims2 = np.zeros((meas_num,256,320))
        s1 = np.zeros((meas_num,256,320)) #standard deviation per pixel
        s2 = np.zeros((meas_num,256,320))
        
        
        for i in range(meas_num):
            # get FPA temperature for each measurement
            t1s[i] = camera1.get_fpa_temperature() 
            t2s[i] = camera2.get_fpa_temperature()
            sensors = readsensors();
            therm = sensors[13]
            bme = sensors[2]            
            
            im1 = np.zeros((frames,256,320))
            im2 = np.zeros((frames,256,320))
      
    
         #for loop will take x amount of frames 
        #note: frames are different than measurements, # of frames in 1 measurement   
            for j in range(frames):
                im1[j] = camera1.grab(device_id = 1)
                im2[j] = camera2.grab(device_id = 2)
                
        #averaging over the frames and getting standard deviation
            ims1[i,:,:] = np.mean(im1,axis = 0 )
            ims2[i,:,:] = np.mean(im2,axis = 0 )
            
        
            s1[i,:,:] = np.std(im1,axis = 0 )
            s2[i,:,:] = np.std(im2,axis = 0 )
           
            
            plt.imshow(ims1[0])
            plt.colorbar()
           # plt.clim(23700,23900)
            plt.title("Camera1 " + name)
            plt.show()
            plt.imshow(ims2[0])
            plt.title("Camera2 " + name)
         #   plt.clim(23100,23400)
            plt.colorbar()
            plt.show()
    
            
            print('cam 1 is ' + str(t1s[i]))
            print('cam 2 is ' + str(t2s[i]))
    
        #create hdf5 file
        hf = h5py.File(save_path + name + '.h5', 'w')
        hf.create_dataset('imgs1', data=im1)
        hf.create_dataset('imgs2', data=im2)
        hf.create_dataset('temps1', data=t1s)
        hf.create_dataset('temps2', data=t2s)
        hf.create_dataset('standev1', data=s1)
        hf.create_dataset('standev2',data=s2)
        hf.create_dataset('therm', data=therm)
        hf.create_dataset('housing',data=bme)
        hf.close()
        
        k = k + 1
        time.sleep(10)
    
       
    
camera1.close()
camera2.close()

#beep to signal measurement end
#duration = 1000  # milliseconds
#freq = 440  # Hz
#winsound.Beep(freq, duration)








