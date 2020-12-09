# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:19 2020
requires pyvisa
installed in flirpy enviroment
@author: khart
"""
import pyvisa
import time

def initialize():
    rm = pyvisa.ResourceManager()
    instr = rm.open_resource('USB0::0x1FDE::0x0006::1001::INSTR');
    #set units to micron
    instr.write('units um')
    print('units set to : ' +instr.query('Units?'))
    return(instr)


    
def changeWavelength(instr,value):
    """
    changes the monochromator wavelength
    units in micron
    """
    instr.write('units um')
    com = 'gowave ' + str(value);
    instr.write(com)
    #print(instr.query('system:error?'))
    time.sleep(1)
    print('wavelength set to : ' + instr.query('gowave?'))
        
    
def shutter(instr,value):
    """
    changes the shutter
    1 is open, 0 is closed
    """
    if value == 1:
        com = 'shutter ' + str(value);
    if value == 0:
        com = 'shutter ' + str(value);
    instr.write(com)
    time.sleep(1)
    print('shutter is : ' + instr.query('shutter?'))
    
instr = initialize() 
shutter(instr,1)
changeWavelength(instr, 8)  
