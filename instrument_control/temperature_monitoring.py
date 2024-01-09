 # -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 12:03:59 2022

@author: jaclynjohn
"""

from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import numpy as np
import h5py
import time
from balloon_read_sensors import readsensors



"""DO NOT CHANGE"""
camera1 = Boson(port='COM15') #reflected/rotated camera
camera2 = Boson(port='COM5') #transmission


#set FFC to manual
camera1.set_ffc_manual() # set to manual 
camera2.set_ffc_manual()

i = 0;
cam1t = []
cam2t = []
active1 = []
active2 = []
mean1 = []
mean2 = []
housing = []
internalbme = []

ymin1 = 85; ymax1 = 150;
xmin1 = 125; xmax1 = 180;
ymin2 = 100; ymax2 = 150;
xmin2 = 160; xmax2 = 230;

while True:
    
    try:
        
        sensors = readsensors();
        therm = sensors[13]
        bme = sensors[2]
        t1 = camera1.get_fpa_temperature()
        t2 = camera2.get_fpa_temperature()
      #  im1 = camera1.grab(device_id = 1)
      #  im2 = camera2.grab(device_id = 2)
   #     a1 = np.mean(im1[ymin1:ymax1,xmin1:xmax1])
   #     a2 = np.mean(im2[ymin2:ymax2,xmin2:xmax2])
    #    m1 = np.mean(im1)
     #   m2 = np.mean(im2)
        
        
    except:
        pass
           
    i +=1
    
    try:
        cam1t.append(t1)
        cam2t.append(t2)
      #  active1.append(a1)
       # active2.append(a2)
        #mean1.append(m1)
        #mean2.append(m2)
        housing.append(therm)
        internalbme.append(bme)

    except: 
        pass
        
    print(t1)
    print(t2)
    print(housing)
    print(internalbme)
 #   print(a1)
  #  print(a2)
    plt.plot(cam1t,label = "Camera 1")
    plt.plot(cam2t,label = "Camera 2")
    plt.plot(housing, label = "thermistor")
    plt.plot(internalbme, label = "internal bme")
    plt.ylabel("Temperature [C]")
    plt.legend()
    plt.show()
 #   plt.plot(active1,'.',label = "Camera 1 Active Region")
  #  plt.plot(mean1,'.', label = "Camera 1 Entire Image")
   # plt.legend()
    #plt.show()
   # plt.plot(active2,'.',label = "Camera 2 Active Region")
   # plt.plot(mean2, '.',label = "Camera 2 Entire Image")
   # plt.ylabel("Mean Counts")
   # plt.legend()
   # plt.show()
    
    time.sleep(30)