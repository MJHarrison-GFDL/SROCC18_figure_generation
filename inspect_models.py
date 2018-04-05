import dataset
import os,sys

typ=sys.argv[1]
var=sys.argv[2]
model=None
try:
    model=sys.argv[3]
except:
    pass

def load_file_list(R):
    flist=[]
    for r in R:
        flist.append(r['file'])
    return flist

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 regridded x/y/z']
if model is not None:
    P=tb.find(variable=var,name=typ,model=model)
else:
    P=tb.find(variable=var,name=typ)
flist=load_file_list(P)


for f in flist:
    print f
    cmd='ncview '+f
    os.system(cmd)

