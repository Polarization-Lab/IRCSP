
from   flirpy.camera.boson import Boson 
import matplotlib.pyplot as plt
import h5py
import numpy as np
import time 

#from datetime import datetime

def get_timestamp():
    t = time.localtime()
    return time.strftime('%H.%M.%S', t)

def image2_capture(angle):
        
    frame_avg = 10
    #save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Flights\\Flight_02_07122022\\'
  #  save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Calibration\\mono\\'
  
    save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\IRCSP2\\Calibration\\6.9.2023\\mod_test3\\'


    """DO NOT CHANGE"""
    camera2 = Boson(port='COM5') #transmission

    #set FFC to manual
    camera2.set_ffc_manual()

    img2 = np.zeros((256,320))
    im2 = np.zeros((frame_avg,256,320))

    
    t2 = camera2.get_fpa_temperature()
    
    print('cam 2 FPA temperature is ' + str(t2) + 'C')

    for j in range(frame_avg):
    #take image
       # timestamp = get_timestamp() #take time at start of measurement 
        im2[j,:,:] = camera2.grab(device_id = 2)
          
    img2[:,:] = np.mean(im2,axis = 0 )


    plt.imshow(img2)
    plt.show()
    #plt.plot(np.mean(img2[131:133,95:160],axis = 0))
    #plt.show()
    
    
   # with h5py.File(save_path + 'Camera2_Capture_' + str(count) + '.h5', 'w') as h5:
    with h5py.File(save_path + str(angle) + str('deg') + '_Camera2.h5', 'w') as h5:    
#       # h5.attrs["timestamp2"] = timestamp
        h5["image2"] = im2
        h5["temp2"] = t2
        print('Camera2 file saved')
    
    camera2.close()
    
    

        
        