# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 13:51:56 2021

@author: khart
"""
import cv2
from flirpy.camera.boson import Boson
import numpy as np

#ask user to input correct COM port
COM = input("What is the COM PORT? \n ")
print("Attempting to open ", COM)

with Boson(port = COM) as camera:
    while True:
        img = camera.grab(device_id = 1).astype(np.float32)

        # Rescale to 8 bit
        img = 255*(img - img.min())/(img.max()-img.min())

        cv2.imshow('Boson', img.astype(np.uint8))
        if cv2.waitKey(1) == 27:
            break  # esc to quit
        
cv2.destroyAllWindows()
 