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
    print r
