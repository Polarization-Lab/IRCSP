# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:26:42 2020

@author: khart
"""

import numpy as np
import pandas as pd

# import IRCSP modules
from radiometric.LUT import create_LUT_df, determine_reference

from NUC.NUC_functions import determine_dark, apply_DFC_to_df
from NUC.NUC_functions import pixel_registration


def make_polarized_df(path, ikey, tkey, cal_file, waves, view_angle, ymin, ymax, angles, D1, D2, tref1, tref2, M1, M2):
    # apply pixel registration and NUC to full dataset
    mean_ims1 = []
    std_ims1 = []
    t1s = []

    # load and apply NUC and pixel registration
    for i in angles:
        # will create a df and print the names of the keys in the original hdf5 file
        df_i = create_LUT_df(path, str(round(i)) + 'deg.h5')

        # apply 2 point NUC, this df corresponds to Cij
        df = apply_DFC_to_df(df_i, D1, D2, tref1, tref2, M1, M2)

        corrected_images1 = []
        for j in range(len(df)):
            # load image
            rn = df[ikey][j]
            rn[rn <= 0] = 0  # threshold

            # apply pixel registration, this returns C lambda, phi
            T = df[tkey][j]
            t1s.append(T)
            cn = pixel_registration(rn, cal_file, waves, ymin, ymax)
            corrected_images1.append(cn)

        mean_ims1.append(np.mean(corrected_images1, axis=0))
        std_ims1.append(np.std(corrected_images1, axis=0))

    # determine size of data set
    arange = len(mean_ims1)
    srange = len(view_angle)
    lrange = len(waves)

    # preallocate arrays
    wavelength = np.array(np.zeros(arange * srange * lrange))
    spatial = np.array(np.zeros(arange * srange * lrange))
    mean = np.array(np.zeros(arange * srange * lrange))
    std = np.array(np.zeros(arange * srange * lrange))
    aolp = np.array(np.zeros(arange * srange * lrange))

    a = 0
    s = 0
    l = 0
    while a < arange:
        s = 0
        l = 0
        while s < srange:
            l = 0
            while l < lrange:
                index = lrange * srange * a + lrange * s + l

                aolp[index] = angles[a]
                wavelength[index] = waves[l]
                spatial[index] = s
                mean[index] = mean_ims1[a][s, l]
                std[index] = std_ims1[a][s, l]

                l += 1
            s += 1
        a += 1

    # make pandas df
    dict1 = {'aolp': aolp, 'wavelength': wavelength, 'spatial': spatial, 'mean': mean, 'std': std}
    cam = pd.DataFrame(dict1)

    return cam
