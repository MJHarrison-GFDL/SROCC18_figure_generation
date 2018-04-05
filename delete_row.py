import argparse
import dataset

parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str,help='model name',default=None)
parser.add_argument('--variable',type=str,help='variable name',default=None)
parser.add_argument('--table',type=str,help='table name',default=None)
parser.add_argument('--id',type=int,help='id',default=None)
parser.add_argument('--confirm',type=int,help='id',default=0)
args=parser.parse_args()


db=dataset.connect('sqlite:///cmip5.db')

print db.tables

tb=db[args.table]

if args.id is not None:
    R=tb.find(id=args.id)
else:
    if args.variable is None:
        R=tb.find(model=args.model)
    else:
        R=tb.find(model=args.model,variable=args.variable)

for r in R:
    if args.confirm==0:
        print r
    else:
        tb.delete(id=r['id'])

db.commit()

