# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:33:16 2021

@author: Harry Carstairs

This script adds a new BS layer into a temporal datacube.
The result is a net CDF file where TIME is one of the dimensions.

Assumes the main netcdf file does NOT begin with "S1"

Call this script inside the folder where the main and unmerged netCDF files are.
"""

import xarray as xr
from datetime import datetime
import glob

def add_time(file):
    ds = xr.open_dataset(file)
    time = file.split('_')[4].split('T')[0]
    time = datetime.strptime(time,'%Y%m%d')
    ds = ds.assign_coords(t=time)

    vars = list(ds.var())
    VV = [v for v in vars if 'VV' in v][0]
    VH = [v for v in vars if 'VH' in v][0]
    ds['VV'] = ds[VV].expand_dims('t')
    ds['VH'] = ds[VH].expand_dims('t')
    ds = ds.drop(VV); ds = ds.drop(VH); ds = ds.drop('metadata'); ds = ds.drop('projectedLocalIncidenceAngle_db')
    return ds

def merge(ff):
    MAIN = input('Name of main file --> ')
    print('merging '+str(len(ff))+' images')
    ref = xr.open_dataset(MAIN)
    LAT,LON,THETA = ref.lat, ref.lon, ref.theta
    datasets = [add_time(f) for f in ff]
    datasets = [ref]+[ds.interp(lat=LAT,lon=LON) for ds in datasets]
    DS = xr.merge(datasets)
    DS['theta'] = THETA
    OUT = MAIN.split('.')[0]+'_updated.nc'
    DS.to_netcdf(OUT)
    
#------------------------------------------------------------------------

merge(glob.glob('S1*.nc'))

