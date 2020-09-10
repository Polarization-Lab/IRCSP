# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""


from flirpy.camera.boson import Boson
import matplotlib.pyplot as plt


camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')

#set up camera
camera1.setup_video()
camera2.setup_video()

#set FFC to manual
camera1.set_ffc_manual()
camera2.set_ffc_manual()

# get FPA temperature 
temp1 = camera1.get_fpa_temperature()
temp2 = camera2.get_fpa_temperature()

#take image
im1 =camera1.grab()
im2 =camera2.grab()
camera1.close()
camera2.close()

plt.imshow(im1)
plt.title('camera 1 '+ str(temp1))
plt.show()

plt.imshow(im2)
plt.title('camera 2 '+ str(temp2))
plt.show()