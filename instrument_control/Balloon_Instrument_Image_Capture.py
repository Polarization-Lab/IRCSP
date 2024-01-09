

from   flirpy.camera.boson import Boson 
from P3_readsensors import p3_readsensors
import matplotlib.pyplot as plt
import numpy as np
import h5py



save_path = 'C:\\Users\\khart\\Documents\\Summer2022Campaign\\Troubleshooting\\useful\\Balloon'
meas_num = 1  #number of measurements 
frames = 1

#run1 is good, need run 2 and 3 to start around 30C

"""DO NOT CHANGE"""
camera1 = Boson(port='COM16') #reflected/rotated camera
camera2 = Boson(port='COM15') #transmission


#set FFC to manual
camera1.set_ffc_manual() # set to manual 
camera2.set_ffc_manual()

cont = True
while cont:
    val = str(input("Enter Name : "))
    name = val #+ "C"
    
    t1s  = np.zeros(meas_num); #create empty arrays for variables 
    t2s  = np.zeros(meas_num);
    ims1 = np.zeros((meas_num,256,320))
    ims2 = np.zeros((meas_num,256,320))
    s1 = np.zeros((meas_num,256,320)) #standard deviation per pixel
    s2 = np.zeros((meas_num,256,320))
    
    for i in range(meas_num):
        # get FPA temperature for each measurement
        t1s[i] = camera1.get_fpa_temperature() 
        t2s[i] = camera2.get_fpa_temperature()
       # sensordata = p3_readsensors()
      #  Inside_temp = sensordata[2]
      #  Outside_temp = sensordata[5]

        
        im1 = np.zeros((frames,256,320))
        im2 = np.zeros((frames,256,320))
  
        
     #for loop will take x amount of frames 
    #note: frames are different than measurements, # of frames in 1 measurement   
        for j in range(frames):
            im1[j] = camera1.grab(device_id = 1)
            im2[j] = camera2.grab(device_id = 2)
            
    #averaging over the frames and getting standard deviation
        ims1[i,:,:] = np.mean(im1,axis = 0 )
        ims2[i,:,:] = np.mean(im2,axis = 0 )
        
    
        s1[i,:,:] = np.std(im1,axis = 0 )
        s2[i,:,:] = np.std(im2,axis = 0 )
        
       
        
        plt.imshow(ims1[0])
        plt.colorbar()
        #plt.clim(22800,23600)
        plt.title("Camera1 " + name)
        plt.show()
        plt.imshow(ims2[0])
        plt.title("Camera2 " + name)
        #plt.clim(22800,23600)
        plt.colorbar()
        plt.show()

        
        print("on measurement "+ str(i))
        print('cam 1 is ' + str(t1s[i]))
        print('cam 2 is ' + str(t2s[i]))
       # print('housing is ' + str(Inside_temp))

    
    #create hdf5 file
    hf = h5py.File(save_path + name + '.h5', 'w')
    hf.create_dataset('imgs1', data=im1)
    hf.create_dataset('imgs2', data=im2)
    hf.create_dataset('temps1', data=t1s)
    hf.create_dataset('temps2', data=t2s)
    hf.create_dataset('standev1', data=s1)
    hf.create_dataset('standev2',data=s2)
   # hf.create_dataset('inside temp', data = Inside_temp)
   # hf.create_dataset('outside temp', data = Outside_temp)
    hf.close()
    
    "ask if another measurement"
    cont =int(input("Continue? "))
    if cont == 0:
        cont = False
    
camera1.close()
camera2.close()

#beep to signal measurement end
#duration = 1000  # milliseconds
#freq = 440  # Hz
#winsound.Beep(freq, duration)
