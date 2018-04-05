import argparse
import dataset

parser = argparse.ArgumentParser()
parser.add_argument('--model',type=str,help='model name',default=None)
parser.add_argument('--old_root',type=str,help='new root directory',default=None)
parser.add_argument('--new_root',type=str,help='new root directory',default=None)
parser.add_argument('--check',action='store_true',help='check only',default=False)
args=parser.parse_args()


db=dataset.connect('sqlite:///cmip5.db')

for t in db.tables:
#    print t
    tb=db[t]
    R=tb.find(model=args.model)
    for r in R:
        print r
        try:
            p=r['path']
            q=p[p.find(args.old_root)+len(args.old_root):]
            p=args.new_root+q
            print 'replacing path: ',p
            r['path']=p
        except:
            p=r['file']
            q=p[p.find(args.old_root)+len(args.old_root):]
            p=args.new_root+q
            print 'replacing file: ',p
            r['file']=p
        if r.has_key('name'):
            if r['name']==None:
                r['name']='annual'
        t={}
        for rk,rv in zip(r.keys(),r.values()):
            if rk=='hash':
                print 'replacing hash ',rv
            else:
                t[rk]=rv
        h=hash(frozenset(t.items()))
        t['hash']=h
        print t
        if not args.check:
            tb.update(t,['id'])

if not args.check:
    db.commit()


