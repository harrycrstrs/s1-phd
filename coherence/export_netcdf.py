# -*- coding: utf-8 -*-
"""
Created on 7th October 2021

Short script to convert from BEAM-DIMAP to NetCDF
BEAM-DIMAP is the best form for SNAP, whereas NetCDF is easy to work on in Python
To use this script, call it inside a folder of .dim images
$python export_netcdf.py 

@author: Harry Carstairs
"""

import sys
import os
sys.path.append('/home/s1332488/.snap/snap-python')
from snappy import GPF
from snappy import HashMap
from snappy import ProductIO as io
import glob

aoi = 'POLYGON ((12.24259248791666899 -0.12785363430965335,12.24259248791666899 -0.16050013350314909,12.30306056704971596 -0.16050013350314909 ,12.30306056704971596 -0.12785363430965335,12.24259248791666899 -0.12785363430965335 ))'

def createP(function, inputProduct, writeout=False, **kwargs):
    # pythonic version of GPF.createProduct()
    # function is string of SNAP operator
    # inputProduct is SNAP product object
    # kwargs contains any parameters to pass to the operator
    p = HashMap()
    for arg in kwargs:
        p.put(arg,kwargs.get(arg))
    result = GPF.createProduct(function,p,inputProduct)
    if writeout != False:
        io.writeProduct(result,writeout,'NetCDF4-BEAM')
    else:
        return result

files = glob.glob('S1*.dim')

for f in files:  
    target = f.split('.')[0]+'.nc'
    if not os.path.exists(target):
        image = io.readProduct(f)
        image = createP('Subset',image,writeout=target,geoRegion=aoi)
