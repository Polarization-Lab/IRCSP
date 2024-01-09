# -*- coding: utf-8 -*-
"""
Created on Wed May 11 15:46:32 2022
@author: jaclynjohn
"""


from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import h5py
import numpy as np
import time 

#from datetime import datetime


def P3_image_capture():
    
    """DO NOT CHANGE"""
    camera1 = Boson(port='COM6')
    camera2 = Boson(port='COM5')

    #set FFC to manual
    camera1.set_ffc_manual() 
    camera2.set_ffc_manual()

    img1 = np.zeros((256,320))
    img2 = np.zeros((256,320))
    
    t1 = camera1.get_fpa_temperature()
    t2 = camera2.get_fpa_temperature()
    
    print('cam 1 at ' + str(t1))
    print('cam 2 at ' + str(t2))

            #take image
    img1[:,:] = camera1.grab(device_id = 1)
    img2[:,:] = camera2.grab(device_id = 2)

    plt.imshow(img1[:,:])
    plt.show()
    plt.imshow(img2[:,:])
    plt.show()
    
    
    return img1,img2,t1,t2
           
    camera1.close()
    camera2.close()
    
    