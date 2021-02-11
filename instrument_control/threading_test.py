# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 10:50:01 2021

@author: khart
"""

import cv2
import threading
from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print ("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

def take_image(previewName, camID, COM):   
    camera = Boson(port=COM)
    camera.setup_video(device_id = camID)
    camera.set_ffc_manual()
    temp = camera.get_fpa_temperature()
    im =camera.grab(device_id = camID)
    return(im)
    
class camThreadImage(threading.Thread):
    def __init__(self, previewName, camID,COM):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
        self.COM = COM
    def run(self):
        print ("Starting " + self.previewName)
        im = take_image(self.previewName, self.camID,self.COM)
        print(plt.imshow(im))

# Create two threads as follows
thread1 = camThreadImage("Camera 1", 1,"COM5")
thread2 = camThreadImage("Camera 2", 2,"COM6")
thread1.start()
thread2.start()