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
name = "singleimage"
save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP1\\Calibration\\'
meas_num = 1  #number of measurements 
wait = 1
frames= 1

#run1 is good, need run 2 and 3 to start around 30C

"""DO NOT CHANGE"""
camera1 = Boson(port='COM5') #turn on camera
camera2 = Boson(port='COM6')

#set FFC to manual
camera1.set_ffc_manual() # set to manual 
camera2.set_ffc_manual()

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
    
   
    '''plot slice'''
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_ylabel('cam1',color=color)
    ax1.plot(ims1[i][:,10], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('cam2', color=color)  # we already handled the x-label with ax1
    ax2.plot(ims2[i][:,10], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    
    print("on measurement "+ str(i))
    print('cam 1 is ' + str(t1s[i]))
    print('cam 2 is ' + str(t2s[i]))
    time.sleep(wait)
    
    
camera1.close()
camera2.close()


'''plot slice'''
fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_ylabel('cam1', color=color)
ax1.plot(t1s,np.mean(ims1,axis = 1), color=color) #plotting average response with temp
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('cam2', color=color)  # we already handled the x-label with ax1
ax2.plot(t2s,np.mean(ims2,axis = 1),  color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('imgs1', data=ims1)
hf.create_dataset('imgs2', data=ims2)
hf.create_dataset('temps1', data=t1s)
hf.create_dataset('temps2', data=t2s)
hf.create_dataset('standev1', data=s1)
hf.create_dataset('standev2',data=s2)
hf.close()

#beep to signal measurement end
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
