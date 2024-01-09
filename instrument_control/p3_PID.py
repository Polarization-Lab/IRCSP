"""
function that reads/writes to PID
assumes standard PID output of form "Tz=+19.00 P= 0.00 I= 0.00 D=20.00 T=-15...+30 Tr=+43.34 OC=1 PW=+100"
written by Grady Morrissey - 06/3/2022
"""

import serial
import time

def p3_PID(set_temp): #null input for simple lineread

    try:
        port_name = 'COM22'
        ser = serial.Serial(port=port_name, baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0)
        time.sleep(1)
        s = "<"+str(set_temp)+" 20 0 0 -15 30>"
        ser.write(s.encode())
    except:
        print ("PID write failed")
    