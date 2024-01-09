#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 09:07:46 2021

@author: kirahart

this script uses the thorlabs rotation stage to take polarized calibration measurements
it requires the IRCAM conda enviroment 
"""
from rotation.stage_commands import open_port, home_motor, move_motor_absolute

import sys


angle_step = 10;
angle_start = 0;
angle_stop = 360;

COM_motor = 'COM13'


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

    
    # for i in range(meas_num):
        
    #     image1_capture()
    #     image2_capture()
        

        

   # fig, ax1 = plt.subplots()
    
 #   color = 'tab:red'
 #   ax1.set_ylabel('cam1',color=color)
    #ax1.plot(np.mean(im1[120:125,90:190],0), color=color)
 #   ax1.plot(ims1[i][:,10], color=color)
    #ax1.set_ylim(23730,23780)
#    ax1.tick_params(axis='y', labelcolor=color)
    
#    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
  
#    color = 'tab:blue' 
#    ax2.set_ylabel('cam2', color=color)  # we already handled the x-label with ax1
#    #ax2.plot(np.mean(im2[110:140,100:200],0), color=color)
#    ax2.plot(ims2[i][:,10], color=color)
    #ax2.set_ylim(23990,23960)
#    ax2.tick_params(axis='y', labelcolor=color)
    
#    fig.tight_layout()  # otherwise the right y-label is slightly clipped
#    plt.show()
        

    
#camera1.close()
#camera2.close()

