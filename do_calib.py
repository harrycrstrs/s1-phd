# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 09:42:33 2021

@author: s1332488
"""

import sys
sys.path.append('/home/s1332488/code/S1/')
from snappyHelper import createP
import os.path as path

INPUT = sys.argv[1]
OUTPUT = '../calib/'+INPUT.split('.')[0] + '_calib.dim'

if not path.exists(OUTPUT):
    createP('Calibration',
            INPUT,
            writeout=OUTPUT)