# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 08:03:57 202
this script contains functions for basic IRCSP control
@author: khart
"""

from flirpy.camera.boson import Boson

camera = Boson()
image = camera.grab()
camera.close()