# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 16:56:25 2022

@author: khart
"""

from rotation.stage_commands import open_port, home_motor, move_motor_absolute
from flirpy.camera.boson import Boson
from balloon_read_sensors import readsensors
import matplotlib.pyplot as plt
import numpy as np
import time
import h5py
import sys
from P3_image1_capture import image1_capture
from P3_image2_capture import image2_capture


"""options for measurement"""


angle_step = 1;
angle_start = 0;
angle_stop = 360;

COM_motor = 'COM9'


'''----INITIALIZE MOTOR---'''
try:
    motor = open_port(COM_motor)
    home_motor(motor)
except:
    print('Could not connect to motor, exiting')
    sys.exit(1)

for a in range(angle_start,angle_stop,angle_step):

    name = str(int(a))+'deg.h5'
    print('moving to ', a)
    h = move_motor_absolute(motor, a)
    print('actual angle is ',str(h), ' degree')

    
    try:
          image1_capture(name)
          

    except:
        print('error with camera 1 image aquisition')
        pass

    try:
 
        image2_capture(name)

    except:
        print('error with camera 2 image aquisition')
        pass
