import numpy as np
import sys
import dataset
import os
import datetime
import glob

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 regridded x/y/z']

R=tb.distinct('model')
Mlist=[]
for r in R:
    Mlist.append(r['model'])

FLIST=[]

for m in Mlist:
    flist=[]
    R=tb.find(model=m,name='annual',variable='thetao',order_by='start_date')
    for r in R:
#        print r
        flist.append((r['file'],r['id']))
    flist=sorted(flist)
    FLIST.append(flist)

#    for f,i in flist:
#        print i,f
#    quit()
for files,m in zip(FLIST,Mlist):
    if len(files)>0:
        print m,files[0],files[-1],len(files)
    for f in files:
        print f
