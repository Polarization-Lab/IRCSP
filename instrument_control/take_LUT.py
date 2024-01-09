# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""

from   flirpy.camera.boson import Boson 
#from P3_readsensors import p3_readsensors
from balloon_read_sensors import readsensors
import matplotlib.pyplot as plt
import numpy as np
import h5py
import time
#from TEC_set_temp import changetemp

#cam1 35.1
#cam2 34.7

def get_timestamp():
    t = time.localtime()
    return time.strftime('$H.$M.$S.',t)


"""options for measurement"""

save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP1\\Fall2023\\LUT3\\'
meas_num = 1  #number of measurements 
frames = 10
#run1 is good, need run 2 and 3 to start around 30C

"""DO NOT CHANGE"""
camera1 = Boson(port='COM15') #reflected/rotated camera
camera2 = Boson(port='COM5') #transmission
#camera3 = Boson(port='COM4') #transmission


#set FFC to manual
camera1.set_ffc_manual() # set to manual 
camera2.set_ffc_manual()
#camera3.set_ffc_manual()
xmin1 = 100; xmax1 = 190; #active region
ymin1 = 90; ymax1 = 150;
xmin2 = 90; xmax2 = 180;
ymin2 = 100; ymax2 = 160;

#k=0;
cont = True
while cont:
    name = str(input("Enter Name : "))
 #   name = 'Capture' + str(k)
    
    t1s  = np.zeros(meas_num); #create empty arrays for variables 
    t2s  = np.zeros(meas_num);
    t3s  = np.zeros(meas_num);
    ims1 = np.zeros((meas_num,256,320))
    ims2 = np.zeros((meas_num,256,320))
   # ims3 = np.zeros((meas_num,256,320))
    s1 = np.zeros((meas_num,256,320)) #standard deviation per pixel
    s2 = np.zeros((meas_num,256,320))
   # s3 = np.zeros((meas_num,256,320))
    
    
    for i in range(meas_num):
        # get FPA temperature for each measurement
        t1s[i] = camera1.get_fpa_temperature() 
        
        t2s[i] = camera2.get_fpa_temperature()
#        t3s[i] = camera3.get_fpa_temperature()

        sensors = readsensors();
        
#        therm = sensors[12]
 #       bmetemp = sensors[2]
  #      bmehum = sensors[1]

        
        im1 = np.zeros((frames,256,320))
        im2 = np.zeros((frames,256,320))
 #       im3 = np.zeros((frames,256,320))
 
        
     #for loop will take x amount of frames 
    #note: frames are different than measurements, # of frames in 1 measurement   
        for j in range(frames):
            im1[j] = camera1.grab(device_id = 1)
            im2[j] = camera2.grab(device_id = 2)
 #           im3[j] = camera3.grab(device_id = 3)
       
    #averaging over the frames and getting standard deviation
        ims1[i,:,:] = np.mean(im1,axis = 0 )
        ims2[i,:,:] = np.mean(im2,axis = 0 )
 #       ims3[i,:,:] = np.mean(im3,axis = 0 )
    
    
        s1[i,:,:] = np.std(im1,axis = 0 )
        s2[i,:,:] = np.std(im2,axis = 0 )
  #      s3[i,:,:] = np.std(im3,axis = 0 )

        timestamp = get_timestamp()
       
        
        plt.imshow(ims1[0])
        plt.colorbar()
       # plt.clim(23700,23900)
        plt.title("Camera1 " + name)
        plt.show()
        plt.imshow(ims2[0])
        plt.title("Camera2 " + name)
       # plt.clim(23100,23400)
        plt.colorbar()
        plt.show()
       # plt.imshow(im2[0])
       # plt.title("Context " + name)
       # plt.clim(23100,23400)
       # plt.colorbar()
        #plt.show()


        
        print('cam 1 is ' + str(t1s[i]))
        print('cam 2 is ' + str(t2s[i]))
        #print('cam 3 is ' + str(t3s[i]))

       # print('housing is ' + str(Inside_temp))

    
    #create hdf5 file
    hf = h5py.File(save_path + name + '.h5', 'w')
    hf.create_dataset('imgs1', data=im1)
    #hf.create_dataset('imgs2', data=im3)
    hf.create_dataset('imgs3', data=im2)

    hf.create_dataset('temps1', data=t1s)
    hf.create_dataset('temps2', data=t2s)
    hf.create_dataset('temps3', data=t3s)

    hf.create_dataset('standev1', data=s1)
   #hf.create_dataset('standev2',data=s3)
    hf.create_dataset('standev3',data=s2)

 #   hf.create_dataset('thermistor',data=therm)
 #   hf.create_dataset('bmetemp',data=bmetemp)
 #   hf.create_dataset('bmehum',data=bmehum)
    hf.attrs["OS_time"] = timestamp
    hf.close()
    
    "ask if another measurement"
    cont =int(input("Continue? "))
    if cont == 0:
        cont = False
  #  k = k + 1
   # time.sleep(20)

        
    
camera1.close()
camera2.close()
#camera3.close()

#beep to signal measurement end
#duration = 1000  # milliseconds
#freq = 440  # Hz
#winsound.Beep(freq, duration)
