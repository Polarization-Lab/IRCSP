# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:26:42 2020

@author: khart
"""

import numpy as np
import h5py
import pandas as pd

def f(x, A, B): # this is your 'straight line' y=f(x)
    return A*x + B

def pixel_registration(array,cal_file,waves,ymin,ymax):
    #import cal file
    cal =  h5py.File(cal_file, "r")
    ROI =  list(cal['ROI'])
    pa  =  list(cal['fitparams'])
    
    array=array[ymin:ymax,ROI[0]:ROI[1]]
    
    new = np.zeros([len(array),len(waves)])
    for i in range(len(array)):
        for l in range(len(waves)):    
            w=  waves[l]
            j = int(round(f(w,pa[0],pa[1])))
            values = array[i,j-1:j+1]
            value = np.mean(values)
            new[i,l] = value
    return(new)

def create_LUT_df(data_path, name):
    """
    this script converts monochromator data to a pandas df
    requires filepath to .h5 data and filename
    returns df object
    """
    filename = data_path + name
    
    with h5py.File(filename, "r") as f:
        # List all groups
        #print("Keys: %s" % f.keys())
        keys = list(f.keys())
        num_keys = len(keys)
    
    
    #put monochromator data into panda dataframe    
    with h5py.File(filename, "r") as f:
        # List all groups
        a_group_key = list(f.keys())[0]
        data = list(f[a_group_key])

    data_series = pd.Series(data)
    frame = {a_group_key : data_series}
    result = pd.DataFrame(frame) 
    
    #now loop through the rest of the keys
    i = 1
    while i < num_keys:
        with h5py.File(filename, "r") as f:
            a_group_key = list(f.keys())[i]
            data = list(f[a_group_key])
        
        result[keys[i]] = pd.Series(data) 
        i = i +1

    return(result)


def get_slice(df,x,y):
    sli = []
    for i in range(len(df)):
        s = df[i]
        sli.append(s[y,x])
    return(sli)

def get_slice_avg(df,x):
    '''returns slice averaged in the spatial dimension'''
    sli = []
    for i in range(len(df)):
        s = df[i]
        sli.append(np.mean(s[:,x]))