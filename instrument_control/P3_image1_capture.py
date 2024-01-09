# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:46:32 2022

@author: jaclynjohn
"""


from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import h5py
import numpy as np
import time 
import os

#from datetime import datetime


def get_timestamp():
    t = time.localtime()
    return time.strftime('%H.%M.%S', t)


def image1_capture(angle):
    
    frame_avg = 10
    #save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Flights\\Flight_02_07122022\\'
    #save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Calibration\\mono\\'

    save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Calibration\\6.9.2023\\mod_test3\\'

    """DO NOT CHANGE"""
    camera1 = Boson(port='COM6') #reflected/rotated camera

    #set FFC to manual
    camera1.set_ffc_manual() 

    img1 = np.zeros((256,320))
    im1 = np.zeros((frame_avg,256,320))
    
    t1 = camera1.get_fpa_temperature()
    
    print('cam 1 FPA temperature is ' + str(t1) + 'C')

    for j in range(frame_avg):

            #take image
  #      timestamp = get_timestamp() #take time at start of measurement 
        
        im1[j,:,:] = camera1.grab(device_id = 1)
            
    img1[:,:] = np.mean(im1,axis = 0 )

    plt.imshow(img1[:,:])
    plt.show()
   # plt.plot(np.mean(img1[145:147,100:150],axis = 0))
   # plt.ylim(23450,23620)
   # plt.show()
    
        
   # with h5py.File(save_path + 'Camera1_Capture_' + str(count) + '.h5', 'w') as h5:
    with h5py.File(save_path + str(angle) + str('deg') + '_Camera1.h5', 'w') as h5:    
 #      # h5.attrs["timestamp2"] = timestamp
        h5["image2"] = im1
        h5["temp2"] = t1  
        print('Camera1 file saved')

           
    camera1.close()

    
    

        
        