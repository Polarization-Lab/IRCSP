# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""

from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import threading 

camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')



print(camera1.find_video_device())
print(camera2.find_video_device())



#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

# get FPA temperature 
temp1 = camera1.get_fpa_temperature()
temp2 = camera2.get_fpa_temperature()

#take image
im1 =camera1.grab(device_id = 1)
im2 =camera2.grab(device_id = 2)
camera1.close()
camera2.close()

plt.imshow(im1)
plt.title('camera 1 '+ str(temp1))
plt.show()

plt.imshow(im2)
plt.title('camera 2 '+ str(temp2))
plt.show()