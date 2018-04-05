import numpy as np
import pickle
import hashlib
import os
import sys
import dataset

name = sys.argv[1]
root_path = sys.argv[2]
exp = sys.argv[3]

def file_experiment(model,path,fnam,tb):
    exps = ['historical','piControl','rcp45','rcp85']
    rz = ['r1i1p1','r2i1p1','r3i1p1','r4i1p1','r5i1p1','r6i1p1']
    flds = ['thetao','so']

    e_type=None
    for e in exps:
        if fnam.find(e)>-1:
            e_type=e
            exit
    if e_type is None:
        return None

    r_type=None
    for r in rz:
        if fnam.find(r)>-1:
            r_type=r
            exit
    if r_type is None:
        return None

    f_type=None
    for f in flds:
        if fnam.find(f)>-1:
            f_type=f
            exit
    if f_type is None:
        return None



    entry=dict(model=model,path=path,file=fnam,variable=f_type,scenario=e_type,realization=r_type)
    h=hash(frozenset(entry.items()))
    entry['hash']=h
    R=tb.find(hash=h)
    try:
        r=R.next()
    except:
#        print entry
        tb.insert(entry)

    return None

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']

for path,dirs,files in os.walk(root_path):
    for fnam in files:
#        print path
        file_experiment(name,path,fnam,tb)


