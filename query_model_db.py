import numpy as np
import sys
import dataset
import os

exp=sys.argv[1]
var=sys.argv[2]

scenario=None
try:
    scenario=sys.argv[3]
except:
    pass
realiz=None
try:
    realiz = sys.argv[4]
except:
    pass

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 experiments']

if scenario is not None:
    if realiz is not None:
        R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz)
    else:
        R=tb.find(model=exp,variable=var,scenario=scenario)
else:
    R=tb.find(model=exp,variable=var)
for r in R:
    print r
