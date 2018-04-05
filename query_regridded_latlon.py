import numpy as np
import sys
import dataset
import os

exp=sys.argv[1]
var=sys.argv[2]


db=dataset.connect('sqlite:///cmip5.db')
tb=db['CMIP5 regridded']

R=tb.find(model=exp,variable=var)

for r in R:
    print r
