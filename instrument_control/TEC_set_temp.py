# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 12:55:20 2022

@author: jaclynjohn
"""

from mecom import MeCom, ResponseException, WrongChecksum
from example import MeerstetterTEC


self = MeCom
MeCom.channel = 1
MeCom.session = MeCom

def changetemp(temp):
    MeerstetterTEC.set_temp(self,temp)

    