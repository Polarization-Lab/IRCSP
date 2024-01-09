# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 10:58:47 2022

@author: jaclyn
"""
from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import h5py
import numpy as np



#ROI 
ymin = 0 #min 0
ymax = 256 #max 256
xmin = 0 #min 0
xmax = 320 #max 320
meas_num = 10
wait = 1

"""DO NOT CHANGE"""
camera1 = Boson(port='COM4')



#set FFC to manual
camera1.set_ffc_manual() 


im1 = camera1.grab(device_id = 1)
t1 = camera1.get_fpa_temperature()

    
camera1.close()

plt.imshow(im1)

plt.title('Image 1')
plt.colorbar()
print('temp = ',t1)

plt.show()
