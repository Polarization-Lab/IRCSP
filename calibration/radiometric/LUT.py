# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 12:26:42 2020

@author: khart
"""

import numpy as np
import h5py
import pandas as pd
from math import exp
from scipy.optimize import curve_fit
from NUC.NUC_functions import apply_DFC_to_df, pixel_registration


def f(I, A, B):
    return A * I + B


def determine_reference(path, ref_name):
    """
    This function determines the reference temperature
    to be used by the two point NUC

    Parameters
    ----------
    path : str
        filepath to the LUT calibration data.
    ref_name : str
        name of h5 file where reference NUC is located

    Returns
    -------
    Tref1, T2ref
    """
    # first, determine reference temp for each camera
    df_ref = create_LUT_df(path, ref_name)

    tref1 = df_ref['temps1'].value_counts().idxmax()  # most common FPA temp
    tref2 = df_ref['temps2'].value_counts().idxmax()  # most common FPA temp

    print('Ref T1 is ' + str(tref1))
    print('Ref T2 is ' + str(tref2))
    return tref1, tref2


def create_LUT_df(data_path, name):
    """
    this script converts monochromator data to a pandas df
    requires filepath to .h5 data and filename
    returns df object
    """
    filename = data_path + name

    with h5py.File(filename, "r") as file:
        # List all groups
        # print("Keys: %s" % f.keys())
        keys = list(file.keys())
        num_keys = len(keys)

    # put monochromator data into panda dataframe
    with h5py.File(filename, "r") as file:
        # List all groups
        a_group_key = list(file.keys())[0]
        data = list(file[a_group_key])

    data_series = pd.Series(data)
    frame = {a_group_key: data_series}
    result = pd.DataFrame(frame)

    # now loop through the rest of the keys
    i = 1
    while i < num_keys:
        with h5py.File(filename, "r") as file:
            a_group_key = list(file.keys())[i]
            data = list(file[a_group_key])

        result[keys[i]] = pd.Series(data)
        i = i + 1

    return result


def get_slice(df, x, y):
    sli = []
    for i in range(len(df)):
        s = df[i]
        sli.append(s[y, x])
    return sli


def get_slice_avg(df, x):
    """returns slice averaged in the spatial dimension"""
    sli = []
    for i in range(len(df)):
        s = df[i]
        sli.append(np.mean(s[:, x]))


def planck(wav, T):
    # adjust units
    T = T + 273.15
    wav = wav * 1e-6

    h = 6.626e-34
    c = 3.0e+8
    k = 1.38e-23
    b = h * c / (wav * k * T)
    intensity = 1 / ((wav ** 5) * (exp(b) - 1.0)) / 1e7
    return intensity


def planck_array(wav, T):
    # adjust units
    T = T + 273.15
    wav = wav * 1e-6

    h = 6.626e-34
    c = 3.0e+8
    k = 1.38e-23
    a = 2.0 * h * c ** 2
    b = h * c / (wav * k * T)
    intensity = a / ((wav ** 5) * (np.exp(b) - 1.0)) / 1e7
    return intensity


def calc_rad_coef(df, waves):
    """do pixel by pixel fit and determine A and B coefficients"""
    spec = len(df['ims1'][1][1])
    spat = len(df['ims1'][1])


    # preallocate coefficient arrays
    A1 = np.zeros([spat, spec])
    B1 = np.zeros([spat, spec])
    A2 = np.zeros([spat, spec])
    B2 = np.zeros([spat, spec])
    At = np.zeros([spat, spec])
    Bt = np.zeros([spat, spec])

    for i in range(spat):
        for j in range(spec):
            # calculate spectral radiances at each temperature
            Ts = np.array(df['BB_temps'])
            w = waves[j]  # select wavelenth
            Is = []  # preallocate array
            for T in Ts:
                spectral_radiance = planck(w, T)
                Is.append(spectral_radiance)
            Is = np.array(Is)

            # import responses
            rs1 = get_slice(df['ims1'], j, i)
            rs2 = get_slice(df['ims2'], j, i)
            [a1, b1], cov1 = curve_fit(f, Is, rs1)
            [a2, b2], cov2 = curve_fit(f, Is, rs2)
            [at, bt], covt = curve_fit(f, Is, np.add(rs1, rs2))
            A1[i, j] = a1
            B1[i, j] = b1
            A2[i, j] = a2
            B2[i, j] = b2
            At[i, j] = at
            Bt[i, j] = bt
    return [A1, B1], [A2, B2], [At, Bt]


def calculate_transmission(df, waves):
    gamma1 = []
    gamma2 = []

    for i in range(len(df)):
        T = df['BB_temps'][i]
        Lbb = planck_array(waves, T)
        C1 = np.mean(df['ims1'][i], axis=0)
        C2 = np.mean(df['ims2'][i], axis=0)

        g1 = 1 - (Lbb / np.max(Lbb) - C1 / np.max([C1, C2]))
        g2 = 1 - (Lbb / np.max(Lbb) - C2 / np.max([C1, C2]))

        gamma1.append(g1)
        gamma2.append(g2)

    gamma1 = np.mean(gamma1, axis=0)
    gamma2 = np.mean(gamma2, axis=0)

    return gamma1, gamma2


def build_LUT(waves, A1, A2, B1, B2):
    temps = np.linspace(0, 80, 91)

    lut1 = np.zeros([len(waves), len(temps)])
    lut2 = np.zeros([len(waves), len(temps)])

    for t in range(len(temps)):
        ls1 = []
        ls2 = []
        for s in range(25):
            for w in range(len(waves)):
                I = planck(waves[w], temps[t])
                l1 = f(I, A1[s], B1[s]) - B1[s]
                ls1.append(l1)
                l2 = f(I, A2[s], B2[s]) - B2[s]
                ls2.append(l2)
            lut1[:, t] = np.mean(ls1, 0)
            lut2[:, t] = np.mean(ls2, 0)


def finv(R, A, B):
    return (R - B) / A


def applyNUC_to_LUT(TEMPS, path, D1, D2, tref1, tref2, M1, M2, cal_file1, waves, ymin1, ymax1, cal_file2, ymin2, ymax2):
    # apply pixel registration and NUC to full dataset
    mean_ims1 = []
    mean_ims2 = []
    std_ims1 = []
    std_ims2 = []
    t1s = []
    t2s = []

    for i in TEMPS:
        # will create a df and print the names of the keys in the original hdf5 file
        df_i = create_LUT_df(path, str(round(i)) + 'C.h5')

        # apply 2 point NUC, this df cooresponds to Cij
        df = apply_DFC_to_df(df_i, D1, D2, tref1, tref2, M1, M2)

        corrected_images1 = []
        corrected_images2 = []

        for i in range(len(df)):
            # load image
            rn = df['imgs1'][i]

            # apply pixel registration, this returns C lambda, phi
            T = df['temps1'][i]
            t1s.append(T)
            cn = pixel_registration(rn, cal_file1, waves, ymin1, ymax1)
            corrected_images1.append(cn)

        for i in range(len(df)):
            # load image
            rn = df['imgs2'][i]

            # apply pixel registration
            T = df['temps2'][i]
            t2s.append(T)
            cn = pixel_registration(rn, cal_file2, waves, ymin2, ymax2)
            corrected_images2.append(cn)

        mean_ims1.append(np.mean(corrected_images1, axis=0))
        mean_ims2.append(np.mean(corrected_images2, axis=0))

        std_ims1.append(np.std(corrected_images1, axis=0))
        std_ims2.append(np.std(corrected_images2, axis=0))

    d = {'BB_temps': TEMPS, 'ims1': list(mean_ims1), 's1': list(std_ims1), 'ims2': list(mean_ims2),
         's2': list(std_ims2)}
    df = pd.DataFrame.from_dict(d, orient='index')
    df = df.transpose()
    return df


def save_LUT(save_path, name, A1, A2, At, B1, B2, Bt, gamma1, gamma2):
    # create hdf5 file
    hf = h5py.File(save_path + name + '.h5', 'w')
    hf.create_dataset('/A1', data=A1)
    hf.create_dataset('/B1', data=B1)
    hf.create_dataset('/A2', data=A2)
    hf.create_dataset('/B2', data=B2)
    hf.create_dataset('/At', data=At)
    hf.create_dataset('/Bt', data=Bt)

    hf.create_dataset('/gamma1', data=gamma1)
    hf.create_dataset('/gamma2', data=gamma2)
    hf.close()
