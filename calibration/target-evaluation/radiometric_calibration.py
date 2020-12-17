# -*- coding: utf-8 -*-
"""

Created on Wed Dec  9 13:12:18 2020

@author: khart
"""
import numpy as np
import pandas as pd
import h5py
from statistics import mean
from scipy.optimize import curve_fit


def fp(x, A, B): # this is your 'straight line' y=f(x)
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
            j = int(round(fp(w,pa[0],pa[1])))
            values = array[i,j-1:j+1]
            value = np.mean(values)
            new[i,l] = value
    return(new)

def create_df(data_path, name):
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

def make_avg_df(path,name1,name2,cal_file1,cal_file2, waves,ymin1,ymax1,ymin2,ymax2):
    df1 = create_df(path,name1)
    df2 = create_df(path,name2)
    
    corrected_images1= []
    corrected_images2= []

    for i in range(len(df1)):
        c = pixel_registration(df1['images1'][i],cal_file1,waves,ymin1,ymax1)
        corrected_images1.append(c)

    for i in range(len(df2)):
        c = pixel_registration(df2['images1'][i],cal_file2,waves,ymin2,ymax2)
        corrected_images2.append(c)

    mean_ims1 = np.mean(corrected_images1,axis = 0)
    mean_ims2 = np.mean(corrected_images2,axis = 0)

    std_ims1  = np.std(corrected_images1,axis = 0)
    std_ims2  = np.std(corrected_images2,axis = 0)
    
    d =  {'ims1': list(mean_ims1),'s1': list(std_ims1), 'ims2':list(mean_ims2),'s2': list(std_ims2)}
    
    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()
    
    #create sum column
    df["totalrad"] = df['ims2']+df['ims1']
    df["totalstd"] = (df['s2']**2+df['s1']**2)**0.5
    return(df)

def f(x, A, B): # this is your 'straight line' y=f(x)
    return A*x**2 + B

def finv(y,A,B):
    return ((y-B)/A)**0.5