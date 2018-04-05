# Compule annual averages
import numpy as np
import sys
import dataset
import os
import copy
from datetime import datetime,timedelta
from midas.rectgrid import state,quadmesh
import netCDF4 as nc
from shutil import copyfile
import hashlib

exp=sys.argv[1]
var=sys.argv[2]
scenario=sys.argv[3]
realiz = sys.argv[4]
year = sys.argv[5]
start_date_str=str(year)+'-01-01'
end_date_str=str(year)+'-12-31'
start_date = datetime.strptime(start_date_str,"%Y-%m-%d") #target dates for averaging
end_date = datetime.strptime(end_date_str,"%Y-%m-%d") #target dates for averaging

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']
tb2=db['CMIP5 time-averages']
R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz,order_by='start_date')

try:
    r=R.next()
except:
    print 'not found in database'
    quit()

fout=var+'_tavg_'+str(year)+'.nc'
entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,scenario=scenario,realization=realiz,start_date=start_date,end_date=end_date,name='annual')
R.close()
h=hash(frozenset(entry.items()))
entry['hash']=h
T=tb2.find(hash=h)

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

R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz,order_by='start_date')

flist=[];date_list=[];nrecs=[]
for r in R:
    try:
        date_start=datetime.strptime(r['start_date'],"%Y-%m-%d")
    except:
        print 'No date information for ',r['file'], var
        quit()

    date_end=datetime.strptime(r['end_date'],"%Y-%m-%d")
    if len(flist)==0:
        if (date_start.year<=start_date.year and date_end.year>=start_date.year):
            flist.append(r['path']+'/'+r['file'])
            nrecs.append(r['ntimes'])
            date_list.append([date_start,date_end])
    else:
        if (date_end.year<=end_date.year):
            flist.append(r['path']+'/'+r['file'])
            nrecs.append(r['ntimes'])
            date_list.append([date_start,date_end])
        elif (date_start.year<=end_date.year):
            flist.append(r['path']+'/'+r['file'])
            nrecs.append(r['ntimes'])
            date_list.append([date_start,date_end])


if (len(flist)>0):
    f=flist[0];dts=date_list[0];nt=nrecs[0]
else:
    print 'flist,start,end= ',flist,start_date,end_date
    raise()

cmd='cdo -seldate,'+start_date_str+','+end_date_str+' '+f
if os.path.exists('tmp.nc'):
    os.system('rm -f tmp.nc')
fnam=hashlib.md5(f).hexdigest()+'.nc'
cmd=cmd+' tmp.nc'
os.system(cmd)
cmd='cdo -timselavg,12 tmp.nc '+fnam
os.system(cmd)

f=nc.Dataset(fnam,'a')
tmean_=f.variables[var][:]
if f.variables[var].units=='1':
    tmean_=tmean_*1.e3
    f.variables[var].units='psu'

f.variables[var][:]=tmean_
f.sync()
f.close()
cmd='mkdir '+r['path']+'/tavg'

if not os.path.isdir(r['path']+'/tavg'):
    os.system(cmd)
copyfile(fnam,r['path']+'/tavg/'+fout)

entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,scenario=scenario,realization=realiz,start_date=start_date,end_date=end_date,name='annual')
h=hash(frozenset(entry.items()))
entry['hash']=h
R=tb2.find(hash=h)

if not os.path.exists(entry['file']):
    print 'Problem saving time average ',entry['file']
    raise()

try:
    r=R.next()
except:
    pass
    tb2.insert(entry)
    db.commit()
    R=tb2.find(hash=h)
    r=R.next()
    print r['id']
