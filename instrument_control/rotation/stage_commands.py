# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:14:16 2021
module of commands which interface with the Thorlabs ELL
documentation for the thorlabs APT can be found
https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=ELL

this code has been designed to work based on ELL14 
but can be extrapolated to other ELLx devices by modifying the 
value for encoder pulses vs. movements

Utilizes functions adapted from Matlab by Atkin Hyatt

@author: khart
"""

import serial
from thorlabs_encoder import degree_to_hex2, degree_to_hex8,hex_to_degree
import time



'''for the ELL14 the encoder per pulse value is below'''
ELL14 = 262144
enum = ELL14 /360
pulsPerDeg = 398.222222222;
deviceaddress = 0 ;

def open_port(com):
    ser = serial.Serial(com)  # open serial port
    print(ser.name)         # check which port was really used
    ser.baudrate = 9600
    return ser

def home_motor(ser):
    ser.write(b'0ho1')
    print(ser.read())
    
def move_motor_absolute(ser,deg):
    #move motor 
    angleCommand = degree_to_hex8(pulsPerDeg, deg)
    y = b'0ma' + angleCommand.encode('ascii') ;
    print(y)
    ser.write(y)
<<<<<<< HEAD
    print(ser.read())
=======
    time.sleep(.05)
>>>>>>> f4f15bd83acff9a9701b3cacdfd7cbb8a4615129
    
    #read motor's actual position
    ser.write(b'0gp')
    h = ser.read(y)
   
    h = h[3:] #remove '0PO' header
    h = hex_to_degree(pulsPerDeg,h)  #convert to degree
    return(h)
    
def set_jog(ser,jog):
    #move motor 
    angleCommand = degree_to_hex8(pulsPerDeg, jog)
    y = b'0sj' + angleCommand.encode('ascii') ;
    ser.write(y)
    ser.read(y)

def set_velocity(ser,velocity):
    #this is broken"
    '''velocity is in % of maximum vekicuty'''
    #move motor 
    angleCommand = degree_to_hex2(pulsPerDeg, velocity)
    y = b'0sv' + angleCommand.encode('ascii') ;
    ser.write(y)
    ser.read(y)