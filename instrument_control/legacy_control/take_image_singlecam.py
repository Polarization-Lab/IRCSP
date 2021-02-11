# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 16:16:50 2019

@author: khart
"""
from BosonSDK.ClientFiles_Python import Client_API as pyClient
from BosonSDKCopy.ClientFiles_Python import Client_API as pyClient2
import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image
import time
import argparse
from Cam1 import Camera1
from Cam2 import Camera2
import h5py 

def main(args):
   
    rootFileName = args.fp
    fileName = args.name
    avg = args.avg
    com = args.com
     
    cam1 = Camera1(com)
   

    try:
        cam1.make_port(cam1.port)
    except:
        print('Something opening camera port.')
        sys.exit(1)
    
    try:
        camSN = cam1.get_serial()
        print('Camera 1 serial number: '+str(camSN[1]))
       
    except:
        print('Something wrong getting camera general info. Closing cam port and exiting...')
        cam1.close_port()
        sys.exit(2)



    """ CAMERA CONFIGURATION"""
    print('\n\n---START CAMERA CONFIGURATION---')
    
    #NUC filters
    #   Filters that are not configurable here: FFC, temperature Correction, SFFC
    gain = args.gain 
    bpr = False
    
    #Spatial and Temporal Filtering
    #   Filter that is not configurable here: SSN
    scnr = False
    tf = False
    spnr = False 
    
    #NUC Suite
    
    if gain == False:
        cam1.set_gain(pyClient.FLR_BOSON_GAINMODE_E.FLR_BOSON_LOW_GAIN)
       
    else:
        cam1.set_gain(pyClient.FLR_BOSON_GAINMODE_E.FLR_BOSON_HIGH_GAIN)
    
    if bpr == False:
        cam1.set_bpr(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    else:
        cam1.set_bpr(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    
    
    try:
        gainState1 = cam1.get_gainState()
        bprState1 = cam1.get_bprState()
        
        
        print('\nCamera 1 gain mode: ' + str(gainState1[1]))
        print('Camera 1 BPR State : ' + str(bprState1))
        
        
    except:
        print('Something wrong calling NUC correction states. Closing cam port and exiting...')
        cam1.close_port()
        sys.exit(3)
        
    
    #Spatial and temporal filtering Suite
    if scnr == False:
        cam1.set_scnr(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    else:
        cam1.set_scnr(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    
    if tf == False:
        cam1.set_tf(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    else:
        cam1.set_tf(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    
    if spnr == False:
        cam1.set_spnr(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    else:
        cam1.set_spnr(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    
    try:
        scnrState1 = cam1.get_scnrState()
        scnrMaxCorr1 = cam1.get_scnrMaxCorr()
        tfState1 = cam1.get_tfState()
        spnrState1 = cam1.get_spnrState()
        
        print('\nCam 1 SCNR Status: ' + str(scnrState1))
        print('Cam 1 TF Status: ' + str(tfState1))
        print('Cam 1 SPNR Status: ' + str(spnrState1))
        
        
        
    except:
        print('Something bad with calling spatial and temporal filtering states')
        cam1.close_port()
        sys.exit(1)


    """IMAGE ACQUISITION FOR CALIBRATION
        -timer functionality
        -save .tiff images
        -save .txt of raw and corrected FPA temps for each capture
    """
    
    startAll = time.perf_counter()
    loopsToRun =    avg
    secondsToWait = 10
    
    
    fpaTempCorr1 = np.zeros((loopsToRun,2))
    fpaTempCorr2 = np.zeros((loopsToRun,2))
    
    
    
    print('\n\n---START TRIAL CAPTURES---\n')
    for n in range(loopsToRun):
        start = time.perf_counter()
    
   
    
        """Capture image (inferring AGC is off since gain state is fixed), dims now being read"""
        try:
            startIm = time.perf_counter()
            #cam1.take_image()
            pyClient.captureSingleFrame()
          
            print(str(startIm-start) + " seconds to execute both image commands")
            print('Cam 1: Finished Acquiring Image ' + str(n+1))
            print('Cam 2: Finished Acquiring Image ' + str(n+1))
            
        except Exception as e:
            print('Something went wrong during frame capture. Error code: {c}, Message, {m}'.format(c = type(e), m=str(e)))
            cam1.close_port()
            sys.exit(1)
            
            
            
        """Record FPA Temp"""
        fpaTempCorr1[n] = pyClient.bosonlookupFPATempDegCx10()
        print('\nFPA Temp: ' + str(fpaTempCorr1[n][1]/10) + ' C,')
       
        
        
        
            # get read size - output is a tuple
        try:
            #memGetSizeRet = cam1.get_imSize()
            memGetSizeRet = pyClient.memGetCaptureSize()
            
            # store capture size in bytes in new vars for later use
            capSizeinBytes = memGetSizeRet[1]
            pixRows = memGetSizeRet[2]
            pixCols = memGetSizeRet[3]
    
        except:
            print('Something went wrong during memGetCaptureSize() call. Exiting...')
            cam1.close_port()
            sys.exit(1)
       
        
        if n < 1:
            image1 = np.zeros((pixRows,pixCols),dtype = np.uint16,order='C')
            image2 = np.zeros((pixRows,pixCols),dtype = np.uint16,order='C')
        
        
        """Call image bytes from buffer"""
        #create np array of uint8 type
        image8b_1 = np.zeros((pixRows,2*pixCols),dtype = np.uint8,order='C')
        image8b_2 = np.zeros((pixRows,2*pixCols),dtype = np.uint8,order='C')
        image16b_1 = np.zeros((pixRows,pixCols),dtype = np.uint16,order='C')
        image16b_2 = np.zeros((pixRows,pixCols),dtype = np.uint16,order='C')
        bytesPerRead = 160
        readsPerRow = (pixCols*2)/bytesPerRead
        bufNum = 0
        
        for i in np.arange(0,pixRows,1):
                #pixRead_1 = cam1.read_pixels(bufferNum=bufNum,offset=4*i*bytesPerRead,sizeInBytes=bytesPerRead)  # output is a tuple
                pixRead_1 = pyClient.memReadCapture(bufferNum=bufNum,offset=4*i*bytesPerRead,sizeInBytes=bytesPerRead)  # output is a tuple
                image8b_1[i,0:bytesPerRead] = pixRead_1[1]
                
                #pixRead2_1 = cam1.read_pixels(bufferNum=bufNum,offset=((4*i+1)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
                pixRead2_1 = pyClient.memReadCapture(bufferNum=bufNum,offset=((4*i+1)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
                image8b_1[i,bytesPerRead:2*bytesPerRead] = pixRead2_1[1]
                
                #pixRead3_1 = cam1.read_pixels(bufferNum=bufNum,offset=((4*i+2)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
                pixRead3_1 = pyClient.memReadCapture(bufferNum=bufNum,offset=((4*i+2)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
                image8b_1[i,2*bytesPerRead:3*bytesPerRead] = pixRead3_1[1]
                
                #pixRead4_1 = cam1.read_pixels(bufferNum=bufNum,offset=((4*i+3)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
                pixRead4_1 = pyClient.memReadCapture(bufferNum=bufNum,offset=((4*i+3)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
    
                image8b_1[i,3*bytesPerRead:4*bytesPerRead] = pixRead4_1[1]
                
        print('Finished Reading Image from Cam 1 ' + str(n+1))        
     
        
    
        
        
        
        
        
        image16b_1 = image8b_1[:,:].view(np.uint16)    # assuming host and camera endianess match
        image16b_1 = image16b_1.view('<u2')                 # <- little endian u- unsigned 2- bytes
         
        image16b_2 = image8b_2[:,:].view(np.uint16)    # assuming host and camera endianess match
        image16b_2 = image16b_2.view('<u2')         
    
        image1 = image1 + image16b_1
        image2 = image2 + image16b_2
        
        end = time.perf_counter()
        print(str(round(end-start)) + " seconds to run one loop")
        
        if n == loopsToRun-1: #if on last loop, exit before wait time
            break;
        
        print('begin wait for ' + str(secondsToWait-round(end-start)) + ' seconds')
        time.sleep(secondsToWait-(end-start)) #wait for specified time, subtracting time for loop to run
    
    
    
    
    
    """ Save hdf5 files"""
    
    fpaTempCorr1 = fpaTempCorr1[:,1]/10
   
    f = h5py.File(fileName +".hdf5", "a") 
    dset1 = f.create_dataset("image1",data = image1)
    dset2 = f.create_dataset("image2",data = image2)
    t1 =  f.create_dataset("temp1",data = fpaTempCorr1)
    t2 =  f.create_dataset("temp2",data = fpaTempCorr2)
    f.close()

    
    cam1.close_port()
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-fp', type=str, default="", help='filepath')
    parser.add_argument('-name', type=str, default="test", help='angle of linear polarizer')
    parser.add_argument('-gain', type=bool, default=False, help='True = high gain')
    parser.add_argument('-avg', type=int, default=2, help='number of frames to average over')
    parser.add_argument('-com', type=str, default="COM5", help='camera COM port')
    args = parser.parse_args()
    main(args)
    args = parser.parse_args()
    main(args)