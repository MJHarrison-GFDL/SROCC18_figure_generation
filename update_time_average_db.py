import numpy as np
import sys
import dataset
import os
from datetime import datetime

model=sys.argv[1]
var=sys.argv[2]
scenario=sys.argv[3]
realiz = sys.argv[4]
start_date = datetime.strptime(sys.argv[5],"%Y-%m-%d")
end_date = datetime.strptime(sys.argv[6],"%Y-%m-%d")
name = sys.argv[7]

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']
tb2=db['CMIP5 time-averages']

R=tb.find(model=model,variable=var,scenario=scenario,realization=realiz)
try:
    r=R.next()
except:
    print 'experiment not logged'
    raise()

fnam=var+'_tavg_'+str(start_date.year)+'-'+str(end_date.year)+'.nc'
entry=dict(model=model,file=r['path']+'/tavg/'+fnam,variable=var,scenario=scenario,realization=realiz,start_date=start_date,end_date=end_date,name=name)
h=hash(frozenset(entry.items()))
entry['hash']=h
R=tb2.find(hash=h)
try:
    r=R.next()
except:
    tb2.insert(entry)
    db.commit()
    R=tb2.find(hash=h)
    r=R.next()
    print r['id']
