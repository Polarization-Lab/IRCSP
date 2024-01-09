# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 14:54:52 2023

@author: khart
"""

import os, datetime, time, h5py
from flirpy.camera.boson import Boson
import numpy as np


def take_image():
    """take_image: The function will create a Operating System timestamp variable (OS_time), configure
                the 2 IRCSP cameras to take an image (image1 & image2) and store the FPA temperatures
                (temp1 & temp2) into an HDF5 File format with a unique naming convention.
    Parameters:
                filename - the filename of the HDF5 file.
    Returns: HDF5 file with 2 FLIR Boson Images, 2 FPA Temperatures & OS_time string.
    """

    # Time/Speed Test - Start
   # start = datetime.datetime.now()

   # save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\'
    #Create Timestamp for File Creation Tracking
    try:
        now = datetime.datetime.now()
        OS_time = now.strftime("%H.%M.%S")

        camera1 = Boson(port='COM3')
    #    camera2 = Boson(port='COM16')

        #set FFC to manual
        camera1.set_ffc_manual()
     #   camera2.set_ffc_manual()

        #get FPA temperature
        temp1 = camera1.get_fpa_temperature()
      #  temp2 = camera2.get_fpa_temperature()
        print(temp1)
      #  print(temp2)

        #Take Image
        frames = 10
        
        
        im1 = np.zeros((frames,256,320))
      #  im2 = np.zeros((frames,256,320))
  
        
     #for loop will take x amount of frames 
    #note: frames are different than measurements, # of frames in 1 measurement   
        for j in range(frames):
            im1[j] = camera1.grab(device_id = 1)
       #     im2[j] = camera2.grab(device_id = 2)
            

        
    except:
        print('error in image aquisition')
        #Close Camera
        camera1.close()
       # camera2.close()
        time.sleep(5)
    
    finally:
        # Open as Read-Write ("a" - creates file if doesn't exist)
        hf = h5py.File(save_path + str("Capture") + OS_time + '.h5', 'w')
        hf.create_dataset('imgs1', data=im1)
        hf.create_dataset('imgs2', data=im1)
        hf.create_dataset('temps1', data=temp1)
        hf.create_dataset('temps2', data=temp2)
        hf.attrs["OS_time"] = OS_time
        hf.close()

        #Close Camera
        camera1.close()
        camera2.close()


        #Time/Speed Test - Finish
        finish = datetime.datetime.now()

        #Adjust Sleep for File Creation Rate - (File/Seconds)
