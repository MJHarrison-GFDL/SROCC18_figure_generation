import dataset
import sys

db=dataset.connect('sqlite:///cmip5.db')
id=sys.argv[1]

tb=db['CMIP5 regridded']

R=tb.find(id=id)
for r in R:
    print r
    tb.delete(id=id)
db.commit()
