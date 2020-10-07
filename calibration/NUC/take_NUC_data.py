# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 09:51:32 2020
This script will aquire the data required to preform a non uniformity correction
Output data will be saved as an HDF5 file
@author: khart
"""

#add instrument control directory to path
import os
os.chdir('C:\\Users\\khart\\Documents\\IRCSP\\instrument_control\\')
from take_image import take_image
import numpy as np
import h5py
import time


avg = 5;        #number of images to averave over
wait = 60 * 1 ; #time to wait between aquisitions in sec
meas_num = 10   #number of measurements 
name = "test4" 
save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\NUC\\'


#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')

#preallocate space
temp1 = np.zeros(meas_num)
temp2 = np.zeros(meas_num)
ims1 = np.zeros((meas_num,256,320))
ims2 = np.zeros((meas_num,256,320))

i = 0
while i < meas_num:
    [fpaTemp1, fpaTemp2 , image1 , image2] = take_image(avg)
    ims1[i,:,:] = image1
    ims2[i,:,:] = image2
    temp1[i]    = fpaTemp1
    temp2[i]    = fpaTemp2
    
    print("begin wait for "+ str(wait)+" seconds")
    time.sleep(wait)
    i = i+1
 
hf.create_dataset('imgs1', data=ims1)
hf.create_dataset('imgs2', data=ims2)
hf.create_dataset('temps1', data=temp1)
hf.create_dataset('temps2', data=temp2)
hf.close()