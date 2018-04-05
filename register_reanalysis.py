import numpy as np
import pickle
import hashlib
import os
import sys
import dataset

name = sys.argv[1]
root_path = sys.argv[2]
combined=False
try:
    combined=sys.argv[3]
except:
    pass

def file_experiment(model,path,fnam,tb,combined_files=False):
    flds = ['thetao','so']


    f_type=None
    for f in flds:
        if fnam.find(f)>-1:
            f_type=f
            exit
    if f_type is None:
        return None

#    print 'combined_files=',combined_files

    if not combined_files:
        entry=dict(model=model,path=path,file=fnam,variable=f_type)
        h=hash(frozenset(entry.items()))
        entry['hash']=h
        R=tb.find(hash=h)
        try:
            r=R.next()
        except:
#            print entry
            tb.insert(entry)
    else:
        for v in ['thetao','so']:
            cind=fnam.find('.nc')
            fnam_=fnam[:cind]+'_'+v+'.nc'
            entry=dict(model=model,path=path,file=fnam,variable=v)
            h=hash(frozenset(entry.items()))
            entry['hash']=h
            R=tb.find(hash=h)
            try:
                r=R.next()
            except:
#                print entry
                tb.insert(entry)

    return None

db=dataset.connect('sqlite:///reanalyses.db')
tb=db['Reanalyses']

for path,dirs,files in os.walk(root_path):
    for fnam in files:
        print path,fnam
        file_experiment(name,path,fnam,tb,combined_files=combined)


