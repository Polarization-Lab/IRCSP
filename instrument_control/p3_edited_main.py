# -*- coding: utf-8 -*-
"""
Created on 07/07/2022
@author: jaclynjohn
"""


def main():
    
    from P3_image1_capture import image1_capture
    from P3_image2_capture import image2_capture
    
    cont = True
    while cont:
        val = str(input("Enter Name : "))
        name = val + "C"
        
        try:
            image1_capture(name)
            

        except:
            print('error with camera 1 image aquisition')
            pass

        try:
 
            image2_capture(name)

        except:
            print('error with camera 2 image aquisition')
            pass

        cont =int(input("Continue? "))
        if cont == 0:
            cont = False
    