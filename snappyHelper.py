# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 09:44:58 2021

@author: s1332488
"""

import sys
sys.path.append('/home/s1332488/.snap/snap-python')
from snappy import ProductIO
from snappy import GPF
from snappy import HashMap

def createP(function, inputProduct, writeout=False, **kwargs):
    # pythonic version of GPF.createProduct()
    # function is string of SNAP operator
    # inputProduct is SNAP product object
    # kwargs contains any parameters to pass to the operator
    if type(inputProduct) == str:
        inputProduct = ProductIO.readProduct(inputProduct)
    p = HashMap()
    for arg in kwargs:
        p.put(arg,kwargs.get(arg))
    result = GPF.createProduct(function,p,inputProduct)
    if writeout != False:
        ProductIO.writeProduct(result,writeout,'BEAM-DIMAP')
    else:
        return result