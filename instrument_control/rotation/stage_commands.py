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
from   rotation.thorlabs_encoder import degree_to_hex2, degree_to_hex8,hex_to_degree
import time



'''for the ELL14 the encoder per pulse value is below'''
ELL14 = 262144
enum = ELL14 /360
pulsPerDeg = 398 + 2/9
deviceaddress = 0 ;

def open_port(com):
    ser = serial.Serial(com,timeout = 1)  # open serial port
    print(ser.name)         # check which port was really used
    ser.baudrate = 9600
    return ser

def home_motor(ser):
    #flush buffers
    ser.flushInput()
    ser.flushOutput()
    ser.write(b'0ho1')
    h = ser.readline()
    while h[0:3] != b'0PO':
        h = ser.readline()
    
def move_motor_absolute(ser,deg):
    ser.flushInput()
    ser.flushOutput()
    #move motor 
    angleCommand = degree_to_hex8(pulsPerDeg, deg)
    y = b'0ma' + angleCommand.encode('ascii') ;
    ser.write(y);

    #read motor's actual position
    h = ser.readline() 
    while h[0:3] != b'0PO':
        h = ser.readline() 
    h = h[3:11] #remove '0PO' header
    h = int(h,16)/pulsPerDeg  #convert to degree
    return(h)
    
def set_jog(ser,jog):
    #clear buffers
    ser.flushInput()
    ser.flushOutput()
    #move motor 
    angleCommand = degree_to_hex8(pulsPerDeg, jog)
    y = b'0sj' + angleCommand.encode('ascii') ;
    ser.write(y)
    ser.readline(y)

def set_velocity(ser,velocity):
    #this is broken"
    '''velocity is in % of maximum vekicuty'''
    ser.flushInput()
    ser.flushOutput()
    #move motor 
    angleCommand = degree_to_hex2(pulsPerDeg, velocity)
    y = b'0sv' + angleCommand.encode('ascii') ;
    ser.write(y)
    print(ser.readline())