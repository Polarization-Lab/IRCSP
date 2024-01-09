# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""

from flirpy.camera.boson import Boson
from P3_image1_capture import image1_capture 
from P3_image2_capture import image2_capture 
from P3_readsensors import p3_readsensors
import matplotlib.pyplot as plt
import numpy as np
import h5py



cont = True
while cont:
    name = str(input("Enter Name : "))

    image1_capture(name)
    image2_capture(name)    
   
    

    
    "ask if another measurement"
    cont =int(input("Continue? "))
    if cont == 0:
        cont = False
    


#beep to signal measurement end
#duration = 1000  #milliseconds
#freq = 440  # Hz
#winsound.Beep(freq, duration)
