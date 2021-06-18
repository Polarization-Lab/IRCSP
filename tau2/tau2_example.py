# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flirpy.camera.tau import Tau
import numpy as np
import matplotlib.pyplot as plt
import time

#initialize camera
camera =Tau(port = "COM5")

#set camera to return 14 bit data
camera.set_cmos_mode(fourteen_bit = True)
camera.erase_snapshots()


buffer = 1078;

tfpa = camera.get_fpa_temperature()
thou = camera.get_housing_temperature()

print('TFPA = ' + str(tfpa) + 'C')
print('THousing = ' + str(thou) + 'C')

#take darkfield
camera.close_shutter()
camera.snapshot(frame_id= 1)

time.sleep(3)

#take image
camera.open_shutter()
camera.snapshot(frame_id= 2)

#read out data 
dark  = camera.retrieve_snapshot(frame_id=1)
image = camera.retrieve_snapshot(frame_id=2)
#camera.conn.close()