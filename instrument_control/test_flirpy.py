# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""

from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import threading 
import numpy as np
import time


"""options for measurement"""
name = "dark3"
save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\NUC\\dec15\\'





"""DO NOT CHANGE"""
camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

scansize = 100;
t1s = np.zeros(scansize);
t2s = np.zeros(scansize);
r1s = np.zeros(scansize);
r2s = np.zeros(scansize);

for i in range(scansize):
    # get FPA temperature 
    t1s[i] = camera1.get_fpa_temperature()
    t2s[i] = camera2.get_fpa_temperature()
    
    #take image
    im1 =camera1.grab(device_id = 1)
    im2 =camera2.grab(device_id = 2)
    
    r1s[i] = np.mean(im1[100:150,125:175])
    r2s[i] = np.mean(im2[100:150,100:150])
    
    time.sleep(1)
    
camera1.close()
camera2.close()

plt.plot(t1s,r1s, '.', label = "Cam1")
plt.plot(t2s,r2s, '.', label = "Cam2")
plt.xlabel('FPA temp [C]')
plt.ylabel('avg. response over active area')
plt.title('ambient temp warm up ')
plt.show()


