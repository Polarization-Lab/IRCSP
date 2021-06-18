# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:14:16 2021
module of commands which interface with the Thorlabs ELL
@author: khart
"""

import serial


'''for the ELL14 the encoder per pulse value is below'''
ELL14 = 262144
enum = ELL14 /360


def open_port(com):
    ser = serial.Serial(com)  # open serial port
    print(ser.name)         # check which port was really used
    ser.baudrate = 9600
    return ser

def home_motor(ser):
    ser.write(b'0ho1')
    print(ser.read())

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
    
 