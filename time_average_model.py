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

# usage
# python time_average_model.py MODEL-NAME VARIABLE-NAME SCENARIO REALIZATION
# e.g. python time_average_model.py ESM2G thetao rcp85 r1i1p1

exp=sys.argv[1]
var=sys.argv[2]
scenario=sys.argv[3]
realiz = sys.argv[4]
start_date = datetime.strptime(sys.argv[5],"%Y-%m-%d") #target dates for averaging
end_date = datetime.strptime(sys.argv[6],"%Y-%m-%d") #target dates for averaging
name = sys.argv[7]


db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']
tb2=db['CMIP5 time-averages']
R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz,order_by='start_date')
try:
    r=R.next()
except:
    print 'not found in database'
    quit()
fout=var+'_tavg_'+str(start_date.year)+'-'+str(end_date.year)+'.nc'
entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,scenario=scenario,realization=realiz,start_date=start_date,end_date=end_date,name=name)
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
#    print r['start_date'],r['end_date']
    try:
        date_start=datetime.strptime(r['start_date'],"%Y-%m-%d")
    except:
        print 'No date information for ',r['file'], var
        quit()

    date_end=datetime.strptime(r['end_date'],"%Y-%m-%d")
#    print 'date_start= ',date_start
#    print 'date_end= ',date_end
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
    print 'date_list=',date_list
    raise()


istart=1
iend=nt
ds=dts[0]
de=dts[1]
while (ds.year < start_date.year) and istart<iend :
    ds=ds+timedelta(days=365.) # assuming monthly data here!
    istart=istart+12
while (de.year > end_date.year) and iend>1:
    de=de-timedelta(days=365.)
    iend=iend-12

tsamp=[]
tsamp.append([istart,iend])

if (iend==nt) and len(flist)>1:
    for f,dts,nt in zip(flist[1:],date_list[1:],nrecs[1:]):
        istart=1
        iend=nt
        ds=dts[0]
        de=dts[1]
        while (de.year > end_date.year) and iend>1:
            de=de-timedelta(days=365.)
            iend=iend-12
        tsamp.append([istart,iend])

tmpflist=[]
cmd_='cdo -s mergetime '
os.system('rm -f ofile.nc tmp.nc')

for f,t in zip(flist,tsamp):
    cmd='cdo -s'
    nrecs=t[1]-t[0]+1
    nskip=t[0]-1
    if nskip>0:
#        cmd=cmd+' -timselavg,'+str(nrecs)+','+str(nskip)+' '+f
        cmd=cmd+' -seltimestep,'+str(nskip+1)+'/'+str(nskip+nrecs)+' '+f
    else:
#        cmd=cmd+' -timselavg,'+str(nrecs)+' '+f
        cmd=cmd+' -seltimestep,1/'+str(nrecs)+' '+f
    fnam=hashlib.md5(f).hexdigest()+'.nc'
    cmd=cmd+' '+fnam
#    print cmd
    os.system(cmd)
    tmpflist.append(fnam)
    cmd_=cmd_+fnam+' '
cmd_=cmd_+' tmp.nc'
os.system(cmd_)
cmd = 'cdo -s -O -timmean tmp.nc ofile.nc'
os.system(cmd)

fnam='tmp.nc'
tb=nc.Dataset(fnam).variables['time_bnds'][:]
dtime=np.squeeze(tb[:,1]-tb[:,0])
#print dtime
if np.max(dtime)>32.:
    print 'Suspect monthly time axis information'
    print dtime
    raise()

wsum=nc.Dataset(fnam).variables[var][:]*dtime[:,np.newaxis,np.newaxis,np.newaxis]
tmean_=np.sum(wsum,axis=0)/np.sum(dtime)
tmean_=tmean_[np.newaxis,:]
f=nc.Dataset('ofile.nc','a')
if f.variables[var].units=='1':
    tmean_=tmean_*1.e3
    f.variables[var].units='psu'
f.variables[var][:]=tmean_
f.sync()
f.close()
cmd='mkdir '+r['path']+'/tavg'

if not os.path.isdir(r['path']+'/tavg'):
    os.system(cmd)
copyfile('ofile.nc',r['path']+'/tavg/'+fout)

if len(tmpflist)>0:
    for f in tmpflist:
#        print 'removing ',f
        os.system('rm -f '+f)

entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,scenario=scenario,realization=realiz,start_date=start_date,end_date=end_date,name=name)

h=hash(frozenset(entry.items()))
entry['hash']=h
R=tb2.find(hash=h)

if not os.path.exists(entry['file']):
    print 'Problem saving time average ',entry['file']
    raise()

try:
   r=R.next()
except:
   tb2.insert(entry)
   db.commit()
   R=tb2.find(hash=h)
   r=R.next()
   print r['id']



