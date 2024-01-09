# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:21:54 2022

@author: jaclyn
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:37:39 2022

@author: jaclynjohn
"""

from flirpy.camera.boson import Boson
from mono_control import initialize, shutter, changeWavelength
import matplotlib.pyplot as plt
import numpy as np
import h5py
from P3_image1_capture import image1_capture
from P3_image2_capture import image2_capture
import sys
import time



waves =np.linspace(7,13,30);

#initialize monochromator
instr = initialize()
shutter(instr,1)

for w in np.linspace(7,13,120):
    changeWavelength(instr,w);
    
    image1_capture(w)
    image2_capture(w)
              


