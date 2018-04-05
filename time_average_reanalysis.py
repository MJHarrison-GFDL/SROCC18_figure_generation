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
start_date = datetime.strptime(sys.argv[3],"%Y-%m-%d") #target dates for averaging
end_date = datetime.strptime(sys.argv[4],"%Y-%m-%d") #target dates for averaging
name = sys.argv[5]


db=dataset.connect('sqlite:///reanalyses.db')
tb=db['Reanalyses']
tb2=db['Reanalysis time-averages']

R=tb.find(model=exp,variable=var,order_by='start_date')
try:
    r=R.next()
except:
    print 'not found in database'
    quit()

fout=var+'_tavg_'+str(start_date.year)+'-'+str(end_date.year)+'.nc'
entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,start_date=start_date,end_date=end_date,name=name)
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

R=tb.find(model=exp,variable=var,order_by='start_date')

flist=[];date_list=[];nrecs=[]
for r in R:
    print r['start_date'],r['end_date']
    try:
        date_start=datetime.strptime(r['start_date'],"%Y-%m-%d")
    except:
        print 'No date information for ',r['file'], var
        quit()

    date_end=datetime.strptime(r['end_date'],"%Y-%m-%d")
#    print 'date_start= ',date_start
#    print 'date_end= ',date_end
#    print 'start_date= ',start_date
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
    print flist
    f=flist[0];dts=date_list[0];nt=nrecs[0]
else:
    print 'flist,start,end= ',flist,start_date,end_date
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
#        print nt,f,dts
        istart=1
        iend=nt
        ds=dts[0]
        de=dts[1]
        while (de.year > end_date.year) and iend>1:
            de=de-timedelta(days=365.)
            iend=iend-12
        tsamp.append([istart,iend])

tmpflist=[]
cmd_='cdo mergetime '
os.system('rm -f ofile.nc tmp.nc')

for f,t in zip(flist,tsamp):
    cmd='cdo '
    nrecs=t[1]-t[0]+1
    nskip=t[0]-1
    if nskip>0:
        cmd=cmd+' -timselavg,'+str(nrecs)+','+str(nskip)+' '+f
    else:
        cmd=cmd+' -timselavg,'+str(nrecs)+' '+f
    fnam=hashlib.md5(f).hexdigest()+'.nc'
    cmd=cmd+' '+fnam
    print cmd
    os.system(cmd)
    tmpflist.append(f)
    cmd_=cmd_+fnam+' '
cmd_=cmd_+' tmp.nc'
os.system(cmd_)
cmd = 'cdo -timmean tmp.nc ofile.nc'
os.system(cmd)

for fnam in tmpflist:
    tb=nc.Dataset(fnam).variables['time_bnds'][:]
    dtime=np.squeeze(tb[:,1]-tb[:,0])

    # if np.max(dtime)>31.:
    #     print 'Suspect monthly time axis information'
    #     print dtime
    #     quit()

    wsum=nc.Dataset(fnam).variables[var][:]*dtime[:,np.newaxis,np.newaxis,np.newaxis]
    wsum=np.sum(wsum,axis=0)/np.sum(dtime)
    try:
        res=res+wsum
    except:
        res=wsum

tmean_=res/len(tmpflist)
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

# if len(tmpflist)>0:
#     for f in tmpflist:
#         os.system('rm -f '+f)

entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,start_date=start_date,end_date=end_date,name=name)

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



# #        print 'ntimes= ',r['ntimes']
#         de=date_end
#         while de.year > end_date.year:
#             de=de-timedelta(days=365.)
#             iend=iend-12
#             if iend<1:
#                 print 'Houston we have a problem'
#                 raise()
# #        print 'is,ie= ',istart,iend,ds,de,start_date,end_date
#         nsteps=iend-istart+1
#         noffset=istart-1
#         cmd='ncks -O -F -d time,'+str(istart)+','+str(iend)+' '+r['path']+'/'+r['file']+' '+'tmp.nc'
# #        print cmd
#         os.system(cmd)
#         cmd='cdo timselavg,'+str(nsteps)+' '+'tmp.nc'+' '+'avg.nc'
#         os.system(cmd)



 #        fout=var+'_tavg_'+str(start_date.year)+'-'+str(end_date.year)+'.nc'
#         if os.path.isfile(r['path']+'/tavg/'+fout):
#             exit
#         istart=1
#         ds=date_start
#         while ds.year < start_date.year:
#             ds=ds+timedelta(days=365.)
#             istart=istart+12
#         iend=r['ntimes']
# #        print 'ntimes= ',r['ntimes']
#         de=date_end
#         while de.year > end_date.year:
#             de=de-timedelta(days=365.)
#             iend=iend-12
#             if iend<1:
#                 print 'Houston we have a problem'
#                 raise()
# #        print 'is,ie= ',istart,iend,ds,de,start_date,end_date
#         nsteps=iend-istart+1
#         noffset=istart-1
#         cmd='ncks -O -F -d time,'+str(istart)+','+str(iend)+' '+r['path']+'/'+r['file']+' '+'tmp.nc'
# #        print cmd
#         os.system(cmd)
#         cmd='cdo timselavg,'+str(nsteps)+' '+'tmp.nc'+' '+'avg.nc'
#         os.system(cmd)
#         S=state('tmp.nc',fields=[var],verbose=False)
#         S.time_avg(var) # use MIDAS for time-averaging since time weight are not readily available in file
#         S.rename_field(var+'_tav',var)
#         f=nc.Dataset('avg.nc','a')
#         f.variables[var][:]=vars(S)[var]
#         f.sync()
#         f.close()
#         cmd='mkdir '+r['path']+'/tavg'
#         fout=var+'_tavg_'+str(start_date.year)+'-'+str(end_date.year)+'.nc'
#         if not os.path.isdir(r['path']+'/tavg'):
#             os.system(cmd)
#         copyfile('avg.nc',r['path']+'/tavg/'+fout)
#         entry=dict(model=exp,file=r['path']+'/tavg/'+fout,variable=var,scenario=scenario,realization=realiz,start_date=start_date,end_date=end_date,name=name)
#         h=hash(frozenset(entry.items()))
#         entry['hash']=h
#         R=tb2.find(hash=h)
#         try:
#             r=R.next()
#         except:
#             tb2.insert(entry)
#             db.commit()
#             R=tb2.find(hash=h)
#             r=R.next()
#             print r['id']

#    else:
#        print 'data outside of time window ',date_start,date_end,start_date,end_date

