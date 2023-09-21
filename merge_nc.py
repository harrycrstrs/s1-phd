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

def add_time(file):
    ds = xr.open_dataset(file,chunks={'lat':1000,'lon':1000})
    time = file.split('_')[4].split('T')[0]
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
    OUT = input('Name of output file --> ')
    print('merging '+str(len(ff))+' images')
    ref = xr.open_dataset(ff[0],chunks={'lat':1000,'lon':1000})
    LAT,LON,THETA = ref.lat, ref.lon, ref.projectedLocalIncidenceAngle_db
    datasets = [add_time(f) for f in ff]
    datasets = [ds.interp(lat=LAT,lon=LON) for ds in datasets]
    DS = xr.concat(datasets,dim='t')
    DS['theta'] = THETA
    DS.to_netcdf(OUT)
    
#------------------------------------------------------------------------

merge(glob.glob('*.nc'))

