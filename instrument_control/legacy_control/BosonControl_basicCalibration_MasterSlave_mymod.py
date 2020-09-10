# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 11:24:51 2019

@author: Scooby Doobie Doo
"""

# -*- coding: utf-8 -*-
"""
Boson Camera Control Script
Polarization Lab, SWIRP Project
Adriana Stohn 
01 May 2019
"""
from BosonSDK.ClientFiles_Python import Client_API as pyClient
from BosonSDKCopy.ClientFiles_Python import Client_API as pyClient2
import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image
import time


class Cam:
    def __init__(self,port) :
        self.port = port
    def make_port(self,inport):
        self.make_port = pyClient.Initialize(manualport=inport)
    def close_port(self):
        self.close_port = pyClient.Close(cam1.make_port)
    def get_serial(self):
        self.get_serial = pyClient.bosonGetCameraSN()
        return self.get_serial
    
    def set_gain(self,state):
        self.set_gain = pyClient.bosonSetGainMode(state)
    def set_bpr(self,state):
        self.set_bpr = pyClient.bprSetState(state)
    def set_scnr(self,state):
        self.set_scnr = pyClient.scnrSetEnableState(state)
    def set_tf(self,state):
        self.set_tf = pyClient.tfSetEnableState(state)
    def set_spnr(self,state):
        self.set_spnr = pyClient.spnrSetEnableState(state)

    def get_gainState(self):
        self.get_gainState = pyClient.bosonGetGainMode()
        return self.get_gainState
    def get_bprState(self):
        self.get_bprState = pyClient.bprGetState()
        return self.get_bprState
    def get_scnrState(self):
        self.get_scnrState = pyClient.scnrGetEnableState()
        return self.get_scnrState
    def get_scnrMaxCorr(self):
        self.get_scnrMaxCorr = pyClient.scnrGetMaxCorr()
        return self.get_scnrMaxCorr
    def get_tfState(self):
        self.get_tfState = pyClient.tfGetEnableState()
        return self.get_tfState
    def get_spnrState(self):
        self.get_spnrState = pyClient.spnrGetEnableState()
        return self.get_spnrState

    def take_image(self):
        self.take_image = pyClient.captureSingleFrame()
    def get_FPATemp(self):
        self.get_FPATemp = pyClient.bosonlookupFPATempDegCx10()
        return self.get_FPATemp
    def get_imSize(self):
        self.get_imSize = pyClient.memGetCaptureSize()
        return self.get_imSize
    def read_pixels(self,bufferNum,offset,sizeInBytes):
        self.pixels = pyClient.memReadCapture(bufferNum,offset,sizeInBytes)
        return self.pixels
    
    def get_syncMode(self):
        self.mode = pyClient.bosonGetExtSyncMode()
        return self.mode
    def disable_sync(self):
        self.disable_sync = pyClient.bosonSetExtSyncMode(pyClient.FLR_BOSON_EXT_SYNC_MODE_E.FLR_BOSON_EXT_SYNC_DISABLE_MODE)
    def set_asMaster(self):
        self.set_asMaster = pyClient.bosonSetExtSyncMode(pyClient.FLR_BOSON_EXT_SYNC_MODE_E.FLR_BOSON_EXT_SYNC_MASTER_MODE)
    
    
class Cam2:
    def __init__(self,port) :
        self.port = port
    def make_port(self,inport):
        self.make_port = pyClient2.Initialize(manualport=inport)
    def close_port(self):
        self.close_port = pyClient2.Close(cam2.make_port)
    def get_serial(self):
        self.get_serial = pyClient2.bosonGetCameraSN()
        return self.get_serial
    
    def set_gain(self,state):
        self.set_gain = pyClient2.bosonSetGainMode(state)
    def set_bpr(self,state):
        self.set_bpr = pyClient2.bprSetState(state)
    def set_scnr(self,state):
        self.set_scnr = pyClient2.scnrSetEnableState(state)
    def set_tf(self,state):
        self.set_tf = pyClient2.tfSetEnableState(state)
    def set_spnr(self,state):
        self.set_spnr = pyClient2.spnrSetEnableState(state)

    def get_gainState(self):
        self.get_gainState = pyClient2.bosonGetGainMode()
        return self.get_gainState
    def get_bprState(self):
        self.get_bprState = pyClient2.bprGetState()
        return self.get_bprState
    def get_scnrState(self):
        self.get_scnrState = pyClient2.scnrGetEnableState()
        return self.get_scnrState
    def get_scnrMaxCorr(self):
        self.get_scnrMaxCorr = pyClient2.scnrGetMaxCorr()
        return self.get_scnrMaxCorr
    def get_tfState(self):
        self.get_tfState = pyClient2.tfGetEnableState()
        return self.get_tfState
    def get_spnrState(self):
        self.get_spnrState = pyClient2.spnrGetEnableState()
        return self.get_spnrState

    def take_image(self):
        self.take_image = pyClient2.captureSingleFrame()
    def get_FPATemp(self):
        self.get_FPATemp = pyClient2.bosonlookupFPATempDegCx10()
        return self.get_FPATemp
    def get_imSize(self):
        self.get_imSize = pyClient2.memGetCaptureSize()
        return self.get_imSize
    def read_pixels(self,bufferNum,offset,sizeInBytes):
        self.pixels = pyClient2.memReadCapture(bufferNum,offset,sizeInBytes)
        return self.pixels
    
    def get_syncMode(self):
        self.mode = pyClient2.bosonGetExtSyncMode()
        return self.mode
    def disable_sync(self):
        self.disable_sync = pyClient2.bosonSetExtSyncMode(pyClient2.FLR_BOSON_EXT_SYNC_MODE_E.FLR_BOSON_EXT_SYNC_DISABLE_MODE)
    def set_asSlave(self):
        self.set_asMaster = pyClient2.bosonSetExtSyncMode(pyClient2.FLR_BOSON_EXT_SYNC_MODE_E.FLR_BOSON_EXT_SYNC_SLAVE_MODE)
    
    
    
"""OPEN CAMERA
"""


###CHANGES####
cam1 = Cam("COM5")
cam2 = Cam2("COM4")
#####################

try:
    cam1.make_port(cam1.port)
    cam2.make_port(cam2.port)
except:
    print('Something opening camera port.')
    sys.exit(1)

try:
    camSN = cam1.get_serial()
    print('Camera 1 serial number: '+str(camSN[1]))
    camSN2 = cam2.get_serial()
    print('Camera 2 serial number: '+str(camSN2[1]))
except:
    print('Something wrong getting camera general info. Closing cam port and exiting...')
    cam1.close_port()
    cam2.close_port()
    sys.exit(2)







#-----------------------------------------------------------
""" CAMERA CONFIGURATION
"""
print('\n\n---START CAMERA CONFIGURATION---')

#NUC filters
#   Filters that are not configurable here: FFC, temperature Correction, SFFC
gain = False #TRUE = HIGH GAIN, FALSE = LOW GAIN
bpr = False

#Spatial and Temporal Filtering
#   Filter that is not configurable here: SSN
scnr = False
tf = False
spnr = False 

#NUC Suite

if gain == False:
    cam1.set_gain(pyClient.FLR_BOSON_GAINMODE_E.FLR_BOSON_LOW_GAIN)
    cam2.set_gain(pyClient2.FLR_BOSON_GAINMODE_E.FLR_BOSON_LOW_GAIN)
else:
    cam1.set_gain(pyClient.FLR_BOSON_GAINMODE_E.FLR_BOSON_HIGH_GAIN)
    cam2.set_gain(pyClient2.FLR_BOSON_GAINMODE_E.FLR_BOSON_HIGH_GAIN)

if bpr == False:
    cam1.set_bpr(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    cam2.set_bpr(pyClient2.FLR_ENABLE_E.FLR_DISABLE)
else:
    cam1.set_bpr(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    cam2.set_bpr(pyClient2.FLR_ENABLE_E.FLR_ENABLE)


try:
    gainState1 = cam1.get_gainState()
    bprState1 = cam1.get_bprState()
    
    gainState2 = cam2.get_gainState()
    bprState2 = cam2.get_bprState()
    
    print('\nCamera 1 gain mode: ' + str(gainState1[1]))
    print('Camera 1 BPR State : ' + str(bprState1))
    
    print('Camera 2 gain mode: ' + str(gainState2[1]))
    print('Camera 2 BPR State : ' + str(bprState2))
    
except:
    print('Something wrong calling NUC correction states. Closing cam port and exiting...')
    cam1.close_port()
    cam2.close_port()
    sys.exit(3)
    
    
    

#    
###Telemetry junk  
##try:
##    pyClient.telemetrySetState(pyClient.FLR_ENABLE_E.FLR_DISABLE)
##    state = pyClient.telemetryGetState()
##    print('Telemetry status: ' + str(state))
##except:
##    print('Something bad with telemetry query.')
##    pyClient.Close(cam1)
##    sys.exit(1)
#        





#Spatial and temporal filtering Suite
if scnr == False:
    cam1.set_scnr(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    cam2.set_scnr(pyClient2.FLR_ENABLE_E.FLR_DISABLE)
else:
    cam1.set_scnr(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    cam2.set_scnr(pyClient2.FLR_ENABLE_E.FLR_ENABLE)

if tf == False:
    cam1.set_tf(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    cam2.set_tf(pyClient2.FLR_ENABLE_E.FLR_DISABLE)
else:
    cam1.set_tf(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    cam2.set_tf(pyClient2.FLR_ENABLE_E.FLR_ENABLE)

if spnr == False:
    cam1.set_spnr(pyClient.FLR_ENABLE_E.FLR_DISABLE)
    cam2.set_spnr(pyClient2.FLR_ENABLE_E.FLR_DISABLE)
else:
    cam1.set_spnr(pyClient.FLR_ENABLE_E.FLR_ENABLE)
    cam2.set_spnr(pyClient2.FLR_ENABLE_E.FLR_ENABLE)

try:
    scnrState1 = cam1.get_scnrState()
    scnrMaxCorr1 = cam1.get_scnrMaxCorr()
    tfState1 = cam1.get_tfState()
    spnrState1 = cam1.get_spnrState()
    
    scnrState2 = cam2.get_scnrState()
    scnrMaxCorr2 = cam2.get_scnrMaxCorr()
    tfState2 = cam2.get_tfState()
    spnrState2 = cam2.get_spnrState()
    
    print('\nCam 1 SCNR Status: ' + str(scnrState1))
    print('Cam 1 TF Status: ' + str(tfState1))
    print('Cam 1 SPNR Status: ' + str(spnrState1))
    
    print('Cam 2 SCNR Status: ' + str(scnrState2))
    print('Cam 2 TF Status: ' + str(tfState2))
    print('Cam 2 SPNR Status: ' + str(spnrState2))
    
    
except:
    print('Something bad with calling spatial and temporal filtering states')
    cam1.close_port()
    cam2.close_port()
    sys.exit(1)



#----------------------------------------------------------
"""SET UP MASTER SLAVE
"""

3


#-----------------------------------------------------------

"""IMAGE ACQUISITION FOR CALIBRATION
    -timer functionality
    -save .tiff images
    -save .txt of raw and corrected FPA temps for each capture
"""

startAll = time.perf_counter()
loopsToRun =    1
secondsToWait = 10
rootFileName = r'C:\Users\Scooby Doobie Doo\Documents\Other_Boson_Related_Files\MasterSlaveTest\\'
fileName = 'fore13000'

fpaTempCorr1 = np.zeros((loopsToRun,2))
fpaTempCorr2 = np.zeros((loopsToRun,2))

print('\n\n---START TRIAL CAPTURES---\n')
for n in range(loopsToRun):
    start = time.perf_counter()
    
    #print(mode1)
    #print (mode2)

    
    """Capture image (inferring AGC is off since gain state is fixed), dims now being read"""
    try:
        startIm = time.perf_counter()
        #cam1.take_image()
        pyClient.captureSingleFrame()
        pyClient2.captureSingleFrame()
        #cam1.take_image()
        #cam2.take_image()
        #cam1.take_image()
        print(str(startIm-start) + " seconds to execute both image commands")
        print('Cam 1: Finished Acquiring Image ' + str(n+1))
        print('Cam 2: Finished Acquiring Image ' + str(n+1))
        
    except Exception as e:
        print('Something went wrong during frame capture. Error code: {c}, Message, {m}'.format(c = type(e), m=str(e)))
        cam1.close_port()
        cam2.close_port()
        sys.exit(1)
        
        
        
    """Record FPA Temp"""
    #fpaTempCorr1[n] = cam1.get_FPATemp()
    fpaTempCorr1[n] = pyClient.bosonlookupFPATempDegCx10()
    #fpaTempCorr2[n] = cam2.get_FPATemp()
    fpaTempCorr2[n] = pyClient2.bosonlookupFPATempDegCx10()
    print('\nFPA Temp: ' + str(fpaTempCorr1[n][1]/10) + ' C,')
    print('\nFPA Temp: ' + str(fpaTempCorr2[n][1]/10) + ' C,')
    
    
    
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
        cam2.close_port()
        sys.exit(1)
    
    
    
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
 
    
    for i in np.arange(0,pixRows,1):
            #pixRead_2 = cam2.read_pixels(bufferNum=bufNum,offset=4*i*bytesPerRead,sizeInBytes=bytesPerRead)  # output is a tuple
            pixRead_2 = pyClient2.memReadCapture(bufferNum=bufNum,offset=4*i*bytesPerRead,sizeInBytes=bytesPerRead)  # output is a tuple

            image8b_2[i,0:bytesPerRead] = pixRead_2[1]
            
            #pixRead2_2 = cam2.read_pixels(bufferNum=bufNum,offset=((4*i+1)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
            pixRead2_2 = pyClient2.memReadCapture(bufferNum=bufNum,offset=((4*i+1)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
            image8b_2[i,bytesPerRead:2*bytesPerRead] = pixRead2_2[1]
            
            #pixRead3_2 = cam2.read_pixels(bufferNum=bufNum,offset=((4*i+2)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
            pixRead3_2 = pyClient2.memReadCapture(bufferNum=bufNum,offset=((4*i+2)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
            image8b_2[i,2*bytesPerRead:3*bytesPerRead] = pixRead3_2[1]
            
            #pixRead4_2 = cam2.read_pixels(bufferNum=bufNum,offset=((4*i+3)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
            pixRead4_2 = pyClient2.memReadCapture(bufferNum=bufNum,offset=((4*i+3)*bytesPerRead),sizeInBytes=bytesPerRead)  # output is a tuple
            image8b_2[i,3*bytesPerRead:4*bytesPerRead] = pixRead4_2[1]
            
    print('Finished Reading Image from Cam 2 ' + str(n+1))       
    
    
    
    
    
    
    image16b_1 = image8b_1[:,:].view(np.uint16)    # assuming host and camera endianess match
    image16b_1 = image16b_1.view('<u2')                 # <- little endian u- unsigned 2- bytes
     
    image16b_2 = image8b_2[:,:].view(np.uint16)    # assuming host and camera endianess match
    image16b_2 = image16b_2.view('<u2')         


    """Show image"""
#        fig = plt.figure(figsize=(20,8))
#        ax = fig.add_subplot(1,1,1)
#        cax = ax.matshow(image16b_1)
#        fig.colorbar(cax)
    
    fig, ax = plt.subplots()
    lines = ax.plot(image16b_1[121,:])
    #plt.ylim((11000,13000))
    #mplcursors.cursor(lines) # or just mplcursors.cursor()
    plt.show()
    
    """Show image"""
#        fig = plt.figure(figsize=(20,8))
#        ax = fig.add_subplot(1,1,1)
#        cax = ax.matshow(image16b_2)
#        fig.colorbar(cax)
    
    fig, ax = plt.subplots()
    lines = ax.plot(image16b_2[127,:])
  #  plt.ylim((22000,24000))
    #mplcursors.cursor(lines) # or just mplcursors.cursor()
    plt.show()
    
    """ Save image"""
    im1 = Image.fromarray(image16b_1)
    im1.save(rootFileName + fileName+str(n+1) + '_CAM1_' + str(n) + '.tiff')
    
    im2 = Image.fromarray(image16b_2)
    im2.save(rootFileName + fileName+str(n+1) + '_CAM2_' + str(n) + '.tiff')
    
    
    
    
    end = time.perf_counter()
    print(str(round(end-start)) + " seconds to run one loop")
    
    if n == loopsToRun-1: #if on last loop, exit before wait time
        break;
    
    print('begin wait for ' + str(secondsToWait-round(end-start)) + ' seconds')
    time.sleep(secondsToWait-(end-start)) #wait for specified time, subtracting time for loop to run






fpaTempCorr1 = fpaTempCorr1[:,1]/10
fpaTempCorr2 = fpaTempCorr2[:,1]/10
np.savetxt(rootFileName + fileName +'_CAM1_fpaTempCorr_degC',fpaTempCorr1)
np.savetxt(rootFileName + fileName +'_CAM2_fpaTempCorr_degC',fpaTempCorr2)


#--------------------------------------------------------





#--------------------------------------------------------
"""REMOVE MASTER SLAVE
"""

cam1.disable_sync()
cam2.disable_sync()

mode1 = cam1.get_syncMode()
mode2 = cam2.get_syncMode()
print(mode1)
print (mode2)




cam1.close_port()
cam2.close_port()