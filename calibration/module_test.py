#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:56:21 2021

@author: kirahart
"""
import numpy as np
import pandas as pd
import h5py
import sys
import matplotlib.pyplot as plt
from statistics import mean
from scipy.optimize import curve_fit
import imageio
from pathlib import Path

from radiometric.LUT import pixel_registration
from radiometric.LUT import create_LUT_df

from NUC.NUC_functions import import_NUC, apply_NUC, get_slice, determine_slope, determine_dark, apply_DFC_to_df

path = '/Volumes/KESU/may19/polarized/'

ymin2 = 100; ymax2 = 150;
ymin1 = 125; ymax1 = 175;

ROI1= [0,319,0,255]
ROI2= [0,319,0,255]

FOV = 53.51 ;
HFOV = FOV/2;
angles = np.round(np.linspace(-HFOV,HFOV,ymax2-ymin2))