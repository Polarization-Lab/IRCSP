
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:37:39 2022

@author: jaclynjohn
"""

from flirpy.camera.boson import Boson
from mono_control import initialize, shutter, changeWavelength
import matplotlib.pyplot as plt
import numpy as np
from rotation.stage_commands import open_port, home_motor, move_motor_absolute
import h5py
from P3_image1_capture import image1_capture
from P3_image2_capture import image2_capture
import sys
import time


angle_step = 1;
angle_start = 0;
angle_stop = 360;
#waves =np.linspace(7,13,30);

#initialize monochromator
#instr = initialize()
#shutter(instr,1)

COM_motor = 'COM9'

'''----INITIALIZE MOTOR---'''
try:
    motor = open_port(COM_motor)
    home_motor(motor)
except:
    print('Could not connect to motor, exiting')
    sys.exit(1)

 
for a in range(angle_start,angle_stop,angle_step):
#while True:

    angle = str(int(a))
    print('moving to ', a)
    h = move_motor_absolute(motor, a)
    print('actual angle is ',str(h), ' degree')
   
    image1_capture(angle)
    image2_capture(angle)
              


