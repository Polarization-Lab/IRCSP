# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 09:50:57 2020

@author: khart
"""

from flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import numpy as np
import h5py


"""options for measurement"""
name = "180"
save_path = 'C:\\Users\\khart\\Documents\\IRCSP2_data\\NUC\\apr06\\boson\\'
camera1 = Boson(port='COM4')

print(camera1.find_serial_device())

#set FFC to manual
camera1.set_ffc_manual()

# get FPA temperature 
temp1 = camera1.get_fpa_temperature()

imgs1 = []
for i in range(50):
#take image
    im1 =camera1.grab()
    imgs1.append(im1)

camera1.close()

im1 = np.mean(imgs1,0)

plt.imshow(im1)
plt.title('camera 1 '+ str(temp1))
plt.colorbar()
plt.show()

#create hdf5 file
hf = h5py.File(save_path + name + '.h5', 'w')
hf.create_dataset('im1', data=im1)
hf.close()

