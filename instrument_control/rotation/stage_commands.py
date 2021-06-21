# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:14:16 2021
module of commands which interface with the Thorlabs ELL
@author: khart
"""

import serial
from thorlabs_encoder import degree_to_hex


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
    angleCommand = degree_to_hex(pulsPerDeg, deg)
    y = b'0ma' + angleCommand.encode('ascii') ;
    ser.write(y)
    
    #check motor location
    # = ser.read()
    #[j, pos ]= ;
    #pos = strtok(pos);
    #pos = hex2dec(pos) / pulsPerDeg;
    #print("\n Actual Position:", pos ," degrees\n");
  

def move_0(ser):
    ser.write(b'0ma00000000')
    print(ser.read())
    
def move_45(ser):
    ser.write(b'0ma00004600')
    print(ser.read())
    
def move_90(ser):
    ser.write(b'0ma00008C00')
    print(ser.read())

def move_135(ser):
    ser.write(b'0ma0000D200')
    print(ser.read())
    
 