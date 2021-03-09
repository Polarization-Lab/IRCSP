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
name = "cool_down60"
save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\NUC\mar02\\'
wait = 30 ; #time to wait between aquisitions in sec
meas_num = 100  #number of measurements 




"""DO NOT CHANGE"""
camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()


t1s  = np.zeros(meas_num);
t2s  = np.zeros(meas_num);
r1s  = np.zeros(meas_num);
r2s  = np.zeros(meas_num);
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

    r1s[i] = np.mean(im1[100:150,125:175])
    r2s[i] = np.mean(im2[100:150,100:150])
    
    print("on measurement "+ str(i))
    print('cam 1 is ' + str(t1s[i]))
    print('cam 2 is ' + str(t2s[i]))
    time.sleep(wait)
    
camera1.close()
camera2.close()

plt.plot(t1s,r1s, '.', label = "Cam1")
plt.plot(t2s,r2s, '.', label = "Cam2")
plt.xlabel('FPA temp [C]')
plt.ylabel('avg. response over active area')
plt.title('scan temp v.s. response ')
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
