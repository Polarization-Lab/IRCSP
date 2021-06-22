#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 14:32:52 2021
this module contains functions which
will parse numeric input into the required format:
    ASCII long type (32-bit) 2's compliment hexidecimal

documentation for the thorlabs APT can be found
https://www.thorlabs.com/software_pages/viewsoftwarepage.cfm?code=ELL

this code has been designed to work based on ELL14 
but can be extrapolated to other ELLx devices by modifying the 
value for encoder pulses vs. movements

Utilizes functions adapted from Matlab by Atkin Hyatt

@author: kirahart
"""
import struct

def degree_to_hex8(pulsPerDeg, deg):
    '''
    pulsPerDeg - number of pulses per degree, 398 + 2/9 for ELL14
    Deg = angular value of desired degree location

    Returns
    -------
    angleCommand (8 bytes).

    '''
    pulses = round(pulsPerDeg * deg);
    angleCommand = format(pulses,"08X")
    return(angleCommand)

def degree_to_hex2(pulsPerDeg, deg):
    '''
    pulsPerDeg - number of pulses per degree, 398 + 2/9 for ELL14
    Deg = angular value of desired degree location

    Returns
    -------
    angleCommand (2 bytes).

    '''
    pulses = round(pulsPerDeg * deg);
    angleCommand = format(pulses,"02X")
    return(angleCommand)

def float32_bit_pattern(value):
    return sum(b << 8*i for i,b in enumerate(struct.pack('f', value)))

def int_to_binary(value, bits):
    return bin(value).replace('0b', '').rjust(bits, '0')


def float_bin(my_number, places = 3):
    my_whole, my_dec = str(my_number).split(".")
    my_whole = int(my_whole)
    res = (str(bin(my_whole))+".").replace('0b','')
 
    for x in range(places):
        my_dec = str('0.')+str(my_dec)
        temp = '%1.20f' %(float(my_dec)*2)
        my_whole, my_dec = temp.split(".")
        res += my_whole
    return res
 
 
def IEEE754(n) :
    # identifying whether the number
    # is positive or negative
    sign = 0
    if n < 0 :
        sign = 1
        n = n * (-1)
    p = 30
    
    if isinstance(n, float):
        # convert float to binary
        dec = float_bin (n, places = p)
    else:
        dec = int_to_binary(n, 32)
 
    dotPlace = dec.find('.')
    onePlace = dec.find('1')
    # finding the mantissa
    if onePlace > dotPlace:
        dec = dec.replace(".","")
        onePlace -= 1
        dotPlace -= 1
    elif onePlace < dotPlace:
        dec = dec.replace(".","")
        dotPlace -= 1
    mantissa = dec[onePlace+1:]
 
    # calculating the exponent(E)
    exponent = dotPlace - onePlace
    exponent_bits = exponent + 127
 
    # converting the exponent from
    # decimal to binary
    exponent_bits = bin(exponent_bits).replace("0b",'')
 
    mantissa = mantissa[0:23]
 
    # the IEEE754 notation in binary    
    final = str(sign) + exponent_bits.zfill(8) + mantissa
 
    # convert the binary to hexadecimal
    hstr = '%0*X' %((len(final) + 3) // 4, int(final, 2))
    return(hstr)

def signed_step_to_hex(step,encoder):
    value = int(step*encoder);
    hstr  = hex(value)
    return(hstr[2:])
 
    