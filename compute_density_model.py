import numpy as np
import sys
import dataset
import os
import copy
from datetime import datetime,timedelta
from midas.rectgrid import state,quadmesh,wright_eos
import netCDF4 as nc
from shutil import copyfile
import hashlib

# usage
# python time_average_model.py MODEL-NAME VARIABLE-NAME SCENARIO REALIZATION
# e.g. python time_average_model.py ESM2G thetao rcp85 r1i1p1

id_temp=sys.argv[1]
id_salt=sys.argv[2]
z_ref=1000. # potential densities are referenced to 1000m
degK2C=-273.15

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 regridded x/y/z']

T=tb.find(id=id_temp)
S=tb.find(id=id_salt)
try:
    t=T.next()
except:
    print 'thetao not found in database'
    quit()
try:
    s=S.next()
except:
    print 'thetao not found in database'
    quit()


fout=s['file']
i1=fout.find('so/')
i2=fout.find('so_')

if i1 < 0 or i2 < 0:
    print fout
    raise()
fout=fout[:i1]+'sigma'+fout[i1+2:i2]+'sigma_'+fout[i2+3:]
#print fout
i1=fout.find('/tavg')
path=fout[:i1+5]
cmd="mkdir -p "+path
if not os.path.exists(path):
    os.system(cmd)
#    print cmd
entry=dict(model=t['model'],file=fout,variable='sigma',scenario=t['scenario'],realization=t['realization'],name=t['name'])
#print entry
h=hash(frozenset(entry.items()))
entry['hash']=h
T=tb.find(hash=h)
done_it=False
try:
    r=T.next()
    done_it=True
    id=r['id']
except:
    pass

if done_it:
    print id
    quit()

thetao=state(t['file'],fields=['thetao'])
so=state(s['file'],fields=['so'])
S=state(grid=thetao.grid)
vd=thetao.var_dict['thetao'].copy()
z=vd['z']

#if z.min() < -1:
#    density=wright_eos(thetao.thetao+degK2C,so.so,-z*1.e4)-1000.
#else:
#    density=wright_eos(thetao.thetao+degK2C,so.so,z*1.e4)-1000.
sigma=wright_eos(thetao.thetao+degK2C,so.so,z_ref)-1000.
vd['units']='kg m-3'
S.add_field_from_array(sigma,'sigma',vd)
print entry['file']
S.write_nc(entry['file'],['sigma'])

tb.insert(entry)
db.commit()
R=tb.find(hash=h)
r=R.next()
print r['id']



