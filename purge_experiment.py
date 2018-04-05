import dataset
import sys

db=dataset.connect('sqlite:///cmip5.db')
model=sys.argv[1]
hard_purge='False'

try:
    hard_purge= sys.argv[2]
except:
    pass

for t in db.tables:
    print t
    tb=db[t]
    if t == 'CMIP5 experiments':
        if hard_purge=='full':
            R=tb.find(model=model)
            for r in R:
                print r
            tb.delete(model=model)
    else:
        R=tb.find(model=model)
        for r in R:
            print r
        tb.delete(model=model)
    db.commit()
