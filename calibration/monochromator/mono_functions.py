# -*- coding: utf-8 -*-
"""
contains functions relevant to monochromator calibration

note df funct. should work for any hdf5 file
@author: khart
"""
import numpy as np
import h5py
import pandas as pd

def create_mono_df(data_path, name):
    """
    this script converts monochromator data to a pandas df
    requires filepath to .h5 data and filename
    returns df object
    """
    filename = data_path + name
    
    with h5py.File(filename, "r") as f:
        # List all groups
        print("Keys: %s" % f.keys())
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
    
 def locate_max(df, image_number, ROI):
     '''
     located the index of the maximum response in each row in the given ROI
     image number is index of desired array in data set 
     df is data frame made using create_mono_df
     '''
