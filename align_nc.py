# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:33:16 2021

@author: Harry Carstairs

This script merges .nc files into temporal datacube.
The result is a net CDF file where TIME is one of the dimensions.

Call this script inside the folder where the unmerged net CDF files are.
"""

import xarray as xr
from datetime import datetime
import glob
import numpy as np

def add_time(file):
    ds = xr.open_dataset(file)
    time = file.split('_')[4].split('T')[0]
    print(time)
    time = datetime.strptime(time,'%Y%m%d')
    ds = ds.assign_coords(t=time)

    vars = list(ds.var())
    VV = [v for v in vars if 'VV' in v][0]
    VH = [v for v in vars if 'VH' in v][0]
    ds = ds.rename({VV:'VV',VH:'VH'})
    ds['VH'] = ds.VH.expand_dims('t')
    ds['VV'] = ds.VV.expand_dims('t')
    ds = ds.drop('metadata'); ds = ds.drop('projectedLocalIncidenceAngle_db')
    return ds

def merge(ff):
    ff.sort()
    print('aligning '+str(len(ff))+' images')
    with xr.open_dataset(ff[0]) as ref:
        LAT,LON,THETA = ref.lat, ref.lon, ref.projectedLocalIncidenceAngle_db
    i=1
    for f in ff:
        print('Image ',str(i))
        ds = add_time(f).interp(lat=LAT,lon=LON)
        ds.to_netcdf('S1_tile'+str(i)+'_BS.nc')
        print('**************')
        i+=1
    
#------------------------------------------------------------------------

merge(glob.glob('*.nc'))

