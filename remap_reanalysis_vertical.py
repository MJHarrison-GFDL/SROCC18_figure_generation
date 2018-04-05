import numpy as np
import sys
import dataset
import os
from midas.rectgrid import state,quadmesh
import netCDF4 as nc

id=sys.argv[1]
db=dataset.connect('sqlite:///reanalyses.db')
tb=db['Reanalysis time-averages']
tb2=db['Reanalysis regridded']
tb3=db['Reanalysis regridded x/y/z']
tb0=db['Reanalyses']

R=tb2.find(id=id)


done_it=False

try:
    r=R.next()
    fout=r['file']
    fout=fout[:fout.index('.nc')]+'.z_remap.nc'
    entry=dict(model=r['model'],file=fout,variable=r['variable'],name=r['name'])
    h=hash(frozenset(entry.items()))
    entry['hash']=h
    T=tb3.find(hash=h)
    R.close()
    try:
        t=T.next()
#        print 'Already ALE remapped ',r
        done_it=True
    except:
        pass
except:
    pass

R.close()
if done_it:
#    print 'done it'
    print t['id']
    quit()

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

def load_depth_basin(depth_path='woa_depths.r360x180.nc',basin_path='basin_codes.r360x180.nc'):
#These files were used to generate the depth and basin files
#GEBCO_path='/archive/gold/datasets/topography/GEBCO_08_v2.nc'
#depth,basin=depths_and_basin_codes(GEBCO_path,grid_woa)
    depth=nc.Dataset(depth_path).variables['depth'][:]
    basin=nc.Dataset(basin_path).variables['basin'][:]
    return depth,basin
def make_vaxis(path,zname,grid,max_depth):
    #  vertical remapping to a common grid
    zax=nc.Dataset(path).variables[zname][:]
    if zax[0]<1.e-2: zax[0]=5.0 #hard-coded for woa!!
    zax[-1]=np.maximum(zax[-1],max_depth)
    zbax = np.zeros(zax.shape[0]+1)
    zbax[1:-1] = 0.5*(zax[0:-1]+zax[1:])
    zbax[-1]= max_depth
    im=grid.im
    jm=grid.jm
    ZB=np.tile(-zbax[:,np.newaxis,np.newaxis],(1,jm,im))
    return zax,zbax,ZB

def remap_vert(S,var,Vgrid,min_tracer=-5,max_tracer=50):
    S.adjust_thickness(var)
    S.remap_ALE([var],z_bounds=Vgrid['interfaces'],zbax_data=Vgrid['depth_axis_bounds'],method='pcm')
    S.rename_field(var+'_remap',var)
    vars(S)[var]=np.ma.masked_where(vars(S)[var]<min_tracer,vars(S)[var])
#    vars(S)[var]=np.ma.masked_where(vars(S)[var]>max_tracer,vars(S)[var])

grid_woa,WOA=load_woa()
depth,basin=load_depth_basin()
grid_woa.D=depth.copy()
grid_woa.wet[grid_woa.D<10.]=0.
grid_woa.mask=basin.copy()

tb=db['Reanalysis regridded']
R=tb.find(id=id)
r=R.next()
max_depth=6000.
zax,zbax,ZB=make_vaxis('woa.r360x180.nc','DEPTH',grid_woa,max_depth)
Vgrid=dict(depth_axis=zax,depth_axis_bounds=zbax,interfaces=ZB)
S=state(r['file'],grid=grid_woa,fields=[r['variable']],verbose=False)
remap_vert(S,r['variable'],Vgrid)
fout=r['file']
fout=fout[:fout.index('.nc')]+'.z_remap.nc'
entry=dict(model=r['model'],file=fout,variable=r['variable'],name=r['name'])
h=hash(frozenset(entry.items()))
entry['hash']=h
#print entry['file']
S.write_nc(entry['file'],fields=[r['variable']])
tb3.insert(entry)
db.commit()
U=tb3.find(hash=h)
r=U.next()
print r['id']
