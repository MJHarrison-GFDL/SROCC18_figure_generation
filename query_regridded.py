import numpy as np
import sys
import dataset
import os

exp=sys.argv[1]
var=sys.argv[2]
#scenario=sys.argv[3]
#realiz = sys.argv[4]
#name = sys.argv[5]

db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 regridded x/y/z']

#R=tb.find(model=exp,variable=var,scenario=scenario,realization=realiz,name=name)
R=tb.find(model=exp,variable=var)

for r in R:
    print r

