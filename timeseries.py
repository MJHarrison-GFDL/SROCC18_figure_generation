
# coding: utf-8

# ** Figures 2.1.1-2.1.5 for the IPCC Special Report on Oceans and Cryosphere in a Changing Climate **
#
# 2.1.1 (B) Plan-view CMIP5 RCP4.5 mean heat 0-700m, (2013 to 2017) - (2000 to 2004)
# 2.1.1 (C) Plan-view CMIP5 RCP8.5 mean heat 0-700m, (2081 to 2100) - (1986 to 2005)
# ( The time-series line plots in 2.1.1 D & E can wait.)
#
# 2.1.3 (D) Plan-view CMIP5 mean salinity 0-100m, (1996 to 2015) - (1966 to 1985)
# 2.1.3 (E) Plan-view CMIP5 RCP8.5 mean salinity 0-100m, (CMIP6 RCP8.5; (2081 to 2100) - (1986 to 2005))
#
#
# 2.1.5 Zonal basin mean changes (8 of 12 panels - T & S priority, density as time permits)
# (2081 to 2100) - (1986 to 2005)
#

from midas.rectgrid import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy
import netCDF4 as nc
import numpy as np
import dataset
import sys,os
import hashlib
import glob
import argparse

#####################

parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str,help='model name',default=None)
parser.add_argument('--ztop',type=float,help='starting depth',default=0.)
parser.add_argument('--zbot',type=float,help='starting depth',default=0.)
args=parser.parse_args()

rho_ocean=1.035e3
cp_ocean=3982.

def load_tracer(flist,grid,field):
    S=[]
    for f in flist:
        S.append(state(f,grid=grid,fields=[field],verbose=False))
    return S

def load_basin(path):
    f=nc.Dataset(path)
    basin=f.variables['basin']
    return basin

def depths_and_basin_codes(path='GEBO_08_v2.nc',target=None,out_path='depths.nc'):
    grid=quadmesh(path,var='depth',cyclic=True)
    D=state(path,grid=grid,fields=['depth'],verbose=False)
    D2=D.horiz_interp('depth',target=target)
    D2.depth=-D2.depth
    D2.write_nc(out_path,['depth'],format='NETCDF3_CLASSIC')
    execfile('make_basin_mask.py')
    basin=nc.Dataset('basin_codes.nc').variables['basin'][:]
    return D2.depth,basin


def load_file_list(R):
    flist=[]
    for r in R:
        flist.append(r['file'])
    return flist

def  load_woa(woa_path='woa.r360x180.nc'):
#woa_path='/archive/gold/datasets/obs/WOA05_pottemp_salt.nc'
    grid_woa = quadmesh(woa_path,var='thetao',cyclic=True)
    if not os.path.isfile('obs.r360x180.nc'):
        WOA=state(woa_path,grid=grid_woa,fields=['thetao','so'],verbose=False)
        WOA.time_avg('thetao',vol_weight=False)
        WOA.rename_field('thetao_tav','thetao')
        WOA.time_avg('so',vol_weight=False)
        WOA.rename_field('so_tav','so')
        WOA.write_nc('obs.r360x180.nc',['thetao','so'])
    else:
        WOA=state('obs.r360x180.nc',grid=grid_woa,fields=['thetao','so'],verbose=False)
    return grid_woa, WOA

def load_depth_basin():
#These files were used to generate the depth and basin files
#GEBCO_path='/archive/gold/datasets/topography/GEBCO_08_v2.nc'
#depth,basin=depths_and_basin_codes(GEBCO_path,grid_woa)
    depth=nc.Dataset('woa_depths.r360x180.nc').variables['depth'][:]
    basin=nc.Dataset('basin_codes.r360x180.nc').variables['basin'][:]
    return depth,basin



def volume_integrated_timeseries(state,field,title=None,fig=None,color='k',labels=None,y_origin=2006,scale=rho_ocean*cp_ocean,degK=True):

    if degK:
        K2C=273.15
    else:
        K2C=0.
    zout=[]
    lent=-1
    if fig is None:
        fig=plt.figure(1,figsize=(11,6))
    Y=2006
    n=0
    for s in state:
#        s.adjust_thickness(field)
#        s.volume_integral(field,'XYZ',normalize=False)
        hc = (vars(s)[field]-K2C)*scale
#        dthetao = hc[1:]-hc[0:-1]
#        print zout
#        tax=s.var_dict[field]['tax_data']
        dates=instance_to_datetime(s.var_dict[field]['dates'])
        years=[]
        for d in dates:
            years.append(d.year)
        years=np.asarray(years)
        torigin=np.where(years>=y_origin)[0][0]
        print 'torigin=',torigin,hc[torigin]
#        dates=dates[:-1]
#        dtime=tax[1:]-tax[0:-1]
        dtime=365.
#        zout.append(sq(dthetao)/dtime/8.64e4/1.e15)
        zout.append(sq(hc-hc[torigin])/1.e24)
#        print len(dates),zout[-1].shape
#        tax=2006+(tax[:-1]-tax[0])/365.
        if labels is not None:
            plt.plot_date(dates,zout[-1],alpha=0.5,linestyle='solid',label=labels[n])
        else:
            plt.plot_date(dates,zout[-1],alpha=0.5,linestyle='solid')
        n=n+1
#        print dates
#        if zout[-1].shape[0]>lent:
#            TAX=tax
#        lent=max(zout[-1].shape[0],lent)
#    ZOUT=np.zeros((lent,len(zout)))-999.
#    print ZOUT.shape
#    n=0
#    for z in zout:
#        ZOUT[0:len(z),n]=np.array(z)
#        n=n+1
#    tseries=np.ma.masked_where(ZOUT==-999,ZOUT)
#    ens_av=np.mean(tseries,axis=1)
#    plt.plot(TAX,ens_av,color=color,linewidth=2.0,label=label)


#    ZOUT=np.mean(np.asarray(zout),axis=0)
#    plt.plot_date(dates,ZOUT,color=color,alpha=1.0,linestyle='solid',linewidth=2.0)

    return fig
#    plt.grid()
#    plt.xlabel('Year')
#    plt.ylabel('10**15 Joules')
#    return


def flatten(l, ltypes=(list, tuple)):
        ltype = type(l)
        l = list(l)
        i = 0
        while i < len(l):
            while isinstance(l[i], ltypes):
                if not l[i]:
                    l.pop(i)
                    i -= 1
                    break
                else:
                    l[i:i + 1] = l[i]
            i += 1
        return ltype(l)
# Load CMIP5 database

grid_woa,WOA=load_woa()
depth,basin=load_depth_basin()
grid_woa.D=depth.copy()
grid_woa.wet[grid_woa.D<10.]=0.
grid_woa.mask=basin.copy()
WOA.grid.D=depth
depths=WOA.var_dict['thetao']['zax_data']
ztop=np.where(depths>args.ztop)[0][0]
zbot=np.where(depths>args.zbot)[0][0]


obs=[]
path_obs='obs/ocean_heat_global.nc'
grid_obs=quadmesh(path_obs,var='HEAT_IPRC')
for fld in ['HEAT_RG','HEAT_IPRC','HEAT_ENG','HEAT_ENL','HEAT_ORAS','HEAT_SODA']:
    S=state(path_obs,grid=grid_obs,fields=[fld],verbose=True,z_indices=np.arange(ztop,zbot),default_calendar='julian')
    S.volume_integral(fld,'XYZ',normalize=False)
    S.del_field(fld)
    S.rename_field(fld+'_xyzint','thetao')
    obs.append(S)
y_origin=2006
zout=[]
fig=plt.figure(1,figsize=(11,6))

for o in obs:
    dates=instance_to_datetime(o.var_dict['thetao']['dates'])
    years=[]
    for d in dates:
        years.append(d.year)
    torigin=np.where(years>=y_origin)[0][0]
    zout.append(sq(o.thetao-o.thetao[torigin])/1.e24)
    plt.plot_date(dates,zout[-1],alpha=0.5,linestyle='solid',color='grey',marker=None)

ZOUT=np.mean(np.asarray(zout),axis=0)
plt.plot_date(dates,ZOUT,alpha=1.0,linestyle='solid',linewidth=2.0,color='black',marker=None)

db=dataset.connect('sqlite:///reanalyses.db')
tb=db['Reanalyses']
R=tb.distinct('model')
ModelList=[]
if args.model is None:
    for r in R:
        ModelList.append(r['model'])
print ModelList
tb=db['Reanalysis regridded x/y/z']
Res=[]
thetao=[]
if args.model is not None:
    ModelList=[args.model]
rreg=grid_woa.indexed_region(i=(0,1),j=(0,1))
Labels=[]
for m in ModelList:
    fList=[];dates=[]
    R=tb.find(model=m,variable='thetao',name='annual')
    for r in R:
        fList.append(r['file'])
    fList=sorted(fList)
    if len(fList)>0:
        for f in fList:
            S=state(f,grid=grid_woa,geo_region=rreg,fields=['thetao'],verbose=False)
            dates.append(instance_to_datetime(S.var_dict['thetao']['dates']))
        dates=flatten(dates,ltypes=(list))
        print dates[0],dates[-1]
        S=state(MFpath=fList,grid=grid_woa,fields=['thetao'],z_indices=np.arange(ztop,zbot),verbose=True)
        S.adjust_thickness('thetao')
        S.volume_integral('thetao','XYZ',normalize=False)
        S.del_field('thetao')
        S.rename_field('thetao_xyzint','thetao')
        thetao.append(S)
        thetao[-1].var_dict['thetao']['dates']=dates
        Labels.append(m)

fig=volume_integrated_timeseries(thetao,field='thetao',fig=fig,color='r',degK=False,labels=Labels)

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']
R=tb.distinct('model')
ModelList=[]
if args.model is None:
    for r in R:
        ModelList.append(r['model'])
tb=db['CMIP5 regridded x/y/z']
Res=[]
thetao=[]
if args.model is not None:
    ModelList=[args.model]
rreg=grid_woa.indexed_region(i=(0,1),j=(0,1))
for m in ModelList:
    fList=[];dates=[]
    R=tb.find(model=m,variable='thetao',realization='r1i1p1',name='annual')
    for r in R:
        fList.append(r['file'])
    fList=sorted(fList)
    if len(fList)>0:
        for f in fList:
            S=state(f,grid=grid_woa,geo_region=rreg,fields=['thetao'],verbose=False)
            dates.append(instance_to_datetime(S.var_dict['thetao']['dates']))
        dates=flatten(dates,ltypes=(list))
        print dates[0],dates[-1]
        S=state(MFpath=fList,grid=grid_woa,fields=['thetao'],z_indices=np.arange(ztop,zbot),verbose=True)
        S.adjust_thickness('thetao')
        S.volume_integral('thetao','XYZ',normalize=False)
        S.del_field('thetao')
        S.rename_field('thetao_xyzint','thetao')
        thetao.append(S)
        thetao[-1].var_dict['thetao']['dates']=dates

fig=volume_integrated_timeseries(thetao,field='thetao',fig=fig,color='b')
plt.grid()
plt.xlabel('Year')
plt.ylabel('10**24 Joules')
plt.title('Global 0-2000m Heat Content')
plt.legend()
plt.show()
