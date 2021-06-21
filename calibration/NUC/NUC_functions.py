# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:26:42 2020

@author: khart
"""

import numpy as np
import h5py
import pandas as pd
from scipy.optimize import curve_fit

def f(T, A, B): # this is your 'straight line' y=f(x)
    return A*T + B

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
    values1 = df['temps1'].unique()
    images1=[]
    for i in range(len(values1)):
        inds = df.index[df['temps1'] == values1[i]]
        im = np.zeros([256,320])
        for j in inds:
            im = im + df['imgs1'][j]
        im = im/len(inds)
        images1.append(np.around(im,decimals =0))
        
    values2 = df['temps2'].unique()
    images2=[]
    for i in range(len(values2)):
        inds = df.index[df['temps2'] == values2[i]]
        im = np.zeros([256,320])
        for j in inds:
            im = im + df['imgs2'][j]
        im = im/len(inds)
        images2.append(np.around(im,decimals =0))    
    return(values1,images1,values2,images2)    

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

def get_slice(df,x,y):
    '''this takes a slice of a IRCSP DF at index x, y'''
    sli = []
    for i in range(len(df)):
        s = df[i]
        sli.append(s[y,x])
    return(sli)

def get_slice_avg(df,x):
    '''this takes the  average of a df slice'''
    sli = []
    for i in range(len(df)):
        s = df[i]
        sli.append(np.mean(s[:,x]))
    return(sli)

def determine_slope(df_ref,ROI1,ROI2):
    '''uses referense measurement to detemine FPA. temp scaling
    df_ref is the reference data imported from the hdf5 file
    ROI are arrays [xmin,xmax,ymin,ymax]
    requires scipy curve_fit and numpy'''
    
   
    A1 = np.zeros([256,320]) #slope
    B1 = np.zeros([256,320]) #offset
    
    for i in range(ROI1[0],ROI1[1]):
        for j in range(ROI1[2],ROI1[3]):
            temps = df_ref['temps1']
            response = get_slice(df_ref['imgs1'],i,j)
            [a,b],cov = curve_fit(f, temps,  response)
            A1[j,i] = a
            B1[j,i] = b
            
    A2 = np.zeros([256,320]) #slope
    B2 = np.zeros([256,320]) #offset
    
    for i in range(ROI2[0],ROI2[1]):
        for j in range(ROI2[2],ROI2[3]):
            temps = df_ref['temps2']
            response = get_slice(df_ref['imgs2'],i,j)
            [a,b],cov = curve_fit(f, temps,  response)
            A2[j,i] = a
            B2[j,i] = b
            
    return(A1,A2)        

def determine_dark(df_dark,df_ref,A1,A2):
    '''uses the reference temperature to NUC correct the dark field images'''
    
    tref1 =  df_ref['temps1'].value_counts().idxmax() #most common FPA temp
    tref2 =  df_ref['temps2'].value_counts().idxmax() #most common FPA temp
    
    '''determine offset in camera 1 '''
    offsets = [];
    for i in range(len(df_dark)):
        corr = (tref1 - df_dark['temps1'][i])*A1
        offset = (df_dark['imgs1'][i]- corr)
        offsets.append(offset)
    offset1 = np.mean(offsets, axis =0)    
    
    '''determine offset in camera 1 '''
    offsets = [];
    for i in range(len(df_dark)):
        corr = (tref2 - df_dark['temps2'][i])*A1
        offset = (df_dark['imgs2'][i]- corr)
        offsets.append(offset)
    offset2 = np.mean(offsets, axis =0)    
    
    return(tref1,tref2,offset1,offset2)

def DFC(im,t,tref,offset,A):
    dark_corr = offset + (tref-t)*A
    return(im-dark_corr)

def apply_DFC_to_df(df,offset1,offset2,tref1,tref2,A1,A2):
    '''applies the DFC to all images in a df'''
    imgs1 = []; temps1 = []
    imgs2 = []; temps2 = []
    for i in range(len(df)):
        im1  = df['imgs1'][i]
        t1   = df['temps1'][i]
        im1c =DFC(im1,t1,tref1,offset1,A1)# take offset
        im1c = im1c + (tref1-t1)*A1 #rescale gain
        
        im2  = df['imgs2'][i]
        t2   = df['temps2'][i]
        im2c =DFC(im2,t2,tref2,offset2,A2) 
        im2c = im2c + (tref2-t2)*A2 #rescale gain

        imgs1.append(im1c);temps1.append(t1)
        imgs2.append(im2c);temps2.append(t2)
        
    data_corrected = {'imgs1': imgs1,'imgs2': imgs2,'temps1': temps1, 'temps2' : temps2}
    df_corrected = pd.DataFrame.from_dict(data_corrected)
    return(df_corrected)

def correct_and_collapse_df(df,cal_file1,cal_file2,ROI1,ROI2,waves):
    '''applies pixel registration to df
    then takes average of all images in df
    dfs shouls already have NUC and DFC applied'''
    corrected_images1= [] ;
    corrected_images2= [] ; 

    for i in range(len(df)):
        #first without NUC correction
        r = df['imgs1'][i];
        cn = pixel_registration(r,cal_file1,waves,ROI1[2],ROI1[3])
        corrected_images1.append(cn)

        #first without NUC correction
        r = df['imgs2'][i];
        cn = pixel_registration(r,cal_file2,waves,ROI2[2],ROI2[3])
        corrected_images2.append(cn)

    im1 = np.mean(corrected_images1,axis =0)    
    im2 = np.mean(corrected_images2,axis =0)    
    return(im1,im2)

def save_NUC_coef(M1,M2, tref1, tref2, ROI1, ROI2, save_path, name):
    
    """
    This function dsaves the computed NUC as an .h5

    Parameters
    ----------
    save_path : str
        filepath to thecalibration files
    name : str
        name of NUC calibration file

    Returns
    -------
    None
    """
    #create hdf5 file
    hf = h5py.File(save_path + name + '.h5', 'w')
    
    #drift with FPA temps
    hf.create_dataset('/M1',     data= M1)
    hf.create_dataset('/M2',     data= M2)
    hf.create_dataset('/Tref1',  data= tref1)
    hf.create_dataset('/Tref2',  data= tref2)
    #metadata
    hf.create_dataset('/ROI1',  data= ROI1)
    hf.create_dataset('/ROI2',  data= ROI2)
    hf.close()
    