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

def create_NUC_df(data_path, name):
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
    
    
    #put data into panda dataframe    
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

def collapse_df(df):
    '''this function collapses the df by FPA temp
    returns a list of the averages images and the FPA temps present in the df""
    '''
    values = df['temp1'].unique()
    images1=[]
    for i in range(len(values)):
        inds = df.index[df['temp1'] == values[i]]
        im = np.zeros([256,320])
        for j in inds:
            im = im + df['images1'][j]
        im = im/len(inds)
        images1.append(np.around(im,decimals =0))
    return(values,images1)    



def compile_NUC_matrix_input(df):
    '''
    this function will prepare NUC averaged data for NUC_coef()
    df should be averages df from collapse df
    returns and determines reference  temperature 
    returns arrays T adn r for NUC_coef()
    '''
    #find FPA temp with most instances, this is the reference temp
    T_ref = (df['temps1'].value_counts().index.tolist())[0]

    #find BB temps which have a FPA measurement at T_ref
    bbs = np.array(df.query('temps1=='+str(T_ref))['bbtemp'])

    #find unique temps that have more than one FPA temp
    Ts =np.array(df.bbtemp.value_counts().loc[lambda x: x>1].index)

    #find common list of BB temps with at least 2 members and T_ref
    ts = np.intersect1d(Ts,bbs)

    #make new df
    for i in range(len(ts)):
        dfs = df.loc[df['bbtemp'] == ts[i]]

        #select T-ref first, then other temp 
        T1 = np.array(dfs.loc[dfs['temps1'] == T_ref]['temps1'])[0]
        T2 = np.array(dfs.loc[dfs['temps1'] != T_ref]['temps1'])[0]
        r1 = np.array(dfs.loc[dfs['temps1'] == T_ref]['images1'])[0]
        r2 = np.array(dfs.loc[dfs['temps1'] != T_ref]['images1'])[0]
        tfpas = [T1,T2]
        responses = [r1,r2]
        if i == 0:
            tFPAS = tfpas;
            rs = responses
        else:
            tFPAS = np.concatenate((tFPAS, tfpas), axis=0)
            rs = np.concatenate((rs, responses), axis=0)
        
    return(T_ref, tFPAS, rs)       



def calc_NUC_coef(tFPAS,rs,x,y):
    '''this function calculates the cal. coef for a given pizzel
    takes input calculated using  compile_NUC_matrix_input''' 
    i = 0;
    matrix = [];
    delta_r = [];
    while i <len(tFPAS):
        T1 = tFPAS[i]
        T2 = tFPAS[i+1]
        r1 = (rs[i])[y][x]
        r2 = (rs[i+1])[y][x]
        T12 = T1 - T2;
        r12 = r1-r2

        row = [r1*T12,T12]

        matrix.append(row)
        delta_r.append(r12)

        i = i +2

    #now compute psuedo inverse    
    matinv = np.linalg.pinv(matrix)

    #now compute m,b
    [m , b ] = np.matmul(matinv, delta_r)
    return(m,b)

def import_NUC(cal_path):
    '''imports calibration coefficients stored in hdf5'''
    hf = h5py.File(cal_path, 'r')
    m1 = np.array(hf['m1']);
    b1 = np.array(hf['b1']);
    T_ref1 = np.array(hf['T_ref1']);
    m2 = np.array(hf['m2']);
    b2 = np.array(hf['b2']);
    T_ref2 = np.array(hf['T_ref2']);
    return(m1,b1,T_ref1,m2,b2,T_ref2)

def rc(r,T,m,b,T_ref):
    ''''this is the NUC correction function'''
    return((r+b*(T_ref-T))/(1-m*(T_ref-T)))

def apply_NUC(image,T,m,b,T_ref):
    '''this function applies the NUC to an image'''
    r_c =  np.zeros([256,320]); 
    for i in range(320):
        for j in range(256):
            r = image[j,i]
            M = m[j,i]
            B = b[j,i]
            ic =  rc(r,T,M,B,T_ref)
            r_c[j,i] = ic
    return(r_c)        
