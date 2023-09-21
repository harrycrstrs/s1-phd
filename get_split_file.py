# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 15:36:27 2021

@author: s1332488
"""

import sys
sys.path.append('/home/s1332488/code/S1/')
from snappyHelper import createP

INPUT = sys.argv[1]
TARGET = sys.argv[2]
SWATH = sys.argv[3]
FIRST = sys.argv[4]
LAST = sys.argv[5]

# Orbit files
im = createP('Apply-Orbit-File',INPUT)
# Split
im = createP('TOPSAR-Split',im,writeout=TARGET,
    firstBurstIndex=FIRST,lastBurst=LAST,selectedPolarisations='VV,VH',subswath=SWATH)