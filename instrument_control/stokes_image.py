# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 11:24:49 2021

@author: khart
"""
from flirpy.camera.boson import Boson
import rotation.stage_commands as stg
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py

"""options for measurement"""
name = "face5"
save_path = 'C:\\Users\\khart\\Documents\\IRCAM_data\\jun072021\\'


#SET UP MOTOR
ser = stg.open_port('COM9')
stg.home_motor(ser)


#initialize camera
camera = Boson(port='COM4')
camera.set_ffc_manual()
wait = .5
frames = 100

def take_image(frames):
    image = np.zeros([frames,256,320])
    for i in range(frames):
        im = camera.grab(device_id = 1)
        image[i] = im
    return(np.mean(image,axis= 0))    


#measurement sequence
I0 = take_image(frames)
stg.move_45(ser)
time.sleep(wait)
plt.imshow(I0)
plt.show()

I45 = take_image(frames)
stg.move_90(ser)
time.sleep(wait)
plt.imshow(I45)
plt.show()

I90 = take_image(frames)
stg.move_135(ser)
time.sleep(wait)
plt.imshow(I90)
plt.show()

I135 = take_image(frames)
plt.imshow(I135)
plt.show()

camera.close()
ser.close()

S0 = (I0 + I45 + I90 +I135)/4
S1 = I0 - I90
S2 = I45 - I135

plt.imshow(S0)
plt.colorbar()
plt.show()

plt.imshow(S1/S0)
plt.colorbar()
plt.show()

plt.imshow(S2/S0)
plt.colorbar()
plt.show()

#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('I0',    data=I0)
hf.create_dataset('I45',   data=I45)
hf.create_dataset('I90',   data=I90)
hf.create_dataset('I135',  data=I135)
hf.close()
