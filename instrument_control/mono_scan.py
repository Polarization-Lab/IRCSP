# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:37:39 2022

@author: jaclynjohn
"""

from flirpy.camera.boson import Boson
from mono_control import initialize, shutter, changeWavelength
import matplotlib.pyplot as plt
import numpy as np
import h5py


"""options for measurement"""
save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP1\\Fall2023\\pixel_reg\\'
meas_num = 3  #number of measurements to average over
frame_avg = 10

"""DO NOT CHANGE"""
camera1 = Boson(port='COM15') #reflected/rotated camera
camera2 = Boson(port='COM5') #transmission

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

#initialize monochromator
instr = initialize()
shutter(instr,1)


for w in np.linspace(7,13,120):
    changeWavelength(instr,w);
    ims1 = np.zeros((meas_num,256,320))
    ims2 = np.zeros((meas_num,256,320))

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
            im2[j,:,:] = camera2.grab(device_id = 3)
    
        im1 = np.mean(im1,axis = 0)
        im2 = np.mean(im2,axis = 0)
        ims1[i,:,:] = im1
        ims2[i,:,:] = im2

    #save
    #create hdf5 file

    fig, ax = plt.subplots(2,1)
    ax[0].imshow(im1[:,:])
    ax[1].imshow(im2[:,:])
    plt.show()
        
    hf = h5py.File(save_path + str(w) +'.h5', 'w')
    hf.create_dataset( 'imgs1',  data=ims1)
    hf.create_dataset('imgs2',  data=ims2)
    hf.create_dataset( 'temps1', data=t1s)
    hf.create_dataset('temps2', data=t2s)
    hf.create_dataset( 'wavelength', data=w)
    hf.close()
            


    
camera1.close()
camera2.close()
instr.close()
