import numpy as np
import sys
import dataset
import os
from midas.rectgrid import quadmesh,state
import netCDF4 as nc

# usage
# python remap_to_latlon.py ID

id=sys.argv[1]
db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 time-averages']
tb2=db['CMIP5 regridded']
tb0=db['CMIP5 experiments']

fill_bad=0
try:
    fill_bad=sys.argv[2]
except:
    fill_bad=0
R=tb.find(id=id)
done_it=False
try:
    r=R.next()
except:
    print 'Time-average data index not found, id=',id
    quit()


fout=r['file']
fout=fout[:fout.index('.nc')]+'.r360x180.nc'
entry=dict(model=r['model'],file=fout,variable=r['variable'],scenario=r['scenario'],realization=r['realization'],name=r['name'])
h=hash(frozenset(entry.items()))
entry['hash']=h
#print entry
T=tb2.find(hash=h)
R.close()
try:
    t=T.next()
    done_it=True
except:
    pass



if done_it:
    print t['id']
    quit()

R.close()
R=tb.find(id=id)
for r in R:
    fout=r['file']
    fout=fout[:fout.index('.nc')]+'.r360x180.nc'
    cmd='cdo remapbil,r360x180 -selname,'+r['variable']+' '+r['file']+' '+fout
    os.system(cmd)
    if fill_bad==1:
        var=entry['variable']
        grid=quadmesh('woa_depths.r360x180.nc',var='depth',cyclic=True)
        grid.D=nc.Dataset('woa_depths.r360x180.nc').variables['depth'][:]
        S=state(entry['file'],grid=grid,fields=[var],verbose=False)
        S.adjust_thickness(var)
        S.fill_interior(var)
        f_=nc.Dataset(entry['file'],'a')
        f_.variables[var][:]=vars(S)[var]
        f_.sync()
        f_.close()

#    print entry
tb2.insert(entry)
db.commit()
U=tb2.find(hash=h)
r=U.next()
print r['id']
