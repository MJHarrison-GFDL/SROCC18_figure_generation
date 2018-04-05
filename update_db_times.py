import numpy as np
import sys
import dataset
import os

exp=sys.argv[1]
var=sys.argv[2]
scenario=sys.argv[3]
realiz = sys.argv[4]

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']

R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz)

for r in R:
#    print r
    if r.has_key('start_date'):
        if r['start_date'] is not None:
            continue
    fnam=r['path']+'/'+r['file']
    cmd="cdo showdate "+fnam+' > junk'
    os.system(cmd)
    f=open('junk');line=f.readline();f.close()
    line=line.split()
    nt=len(line)
    data=dict(id=r['id'],start_date=line[0],end_date=line[-1],ntimes=nt)
    print data
#    cmd="ncdiminq "+fnam+' 0 > junk'
#    os.system(cmd)
#    f=open('junk');lines=f.readlines();f.close()
#    line=lines[4].split("=")
#    line=line[1]
#    nt=int(line[0:line.index(';')])
#    data['ntimes']=nt
    tb.update(data,['id'])

db.commit()

#R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz)

#for r in R:
#    print r
