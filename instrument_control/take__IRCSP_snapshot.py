# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""

from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py
import winsound



"""options for measurement"""
name = "45Ge"
save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\LAB_MEAS\\jun282021\\NACL_r\\'
meas_num = 10  #number of measurements 
wait = .1




"""DO NOT CHANGE"""
camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

ims1 = np.zeros((meas_num,256,320))
ims2 = np.zeros((meas_num,256,320))

for i in range(meas_num):
    # get FPA temperature 
   
    
    #take image
    im1 = camera1.grab(device_id = 1)
    im2 = camera2.grab(device_id = 2)


    ims1[i,:,:] = im1
    ims2[i,:,:] = im2

   
    print("on measurement "+ str(i))
    time.sleep(wait)

t1s = camera1.get_fpa_temperature()
t2s = camera2.get_fpa_temperature()    
    
camera1.close()
camera2.close()


    

print(t1s)
print(t2s)

ims1= np.mean(ims1,axis = 0)
ims2= np.mean(ims2,axis = 0)

plt.imshow(im1)
plt.show()

#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('imgs1', data=ims1)
hf.create_dataset('imgs2', data=ims2)
hf.create_dataset('temps1', data=t1s)
hf.create_dataset('temps2', data=t2s)
hf.close()

#beep to signal measurement end
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
