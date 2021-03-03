# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 09:48:34 2021
testing camera threading
@author: khart
"""
from flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import threading
import time

camera1 = Boson(port='COM5')
camera2 = Boson(port='COM6')

print(camera1.find_serial_device())
print(camera2.find_serial_device())

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

class camThread(threading.Thread):
    def __init__(self, previewName, com):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = com
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, com):
    cam = Boson(port = com)
    print(cam.find_serial_device())
    cam.close()

# Create two threads as follows
thread1 = camThread("Camera 1", 'COM5')
thread2 = camThread("Camera 2", 'COM6')
thread1.start()
thread2.start()