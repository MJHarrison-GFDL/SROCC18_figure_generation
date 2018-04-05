# ESM2M experiments (offset by 1600 years, i.e. calendar year 2000 corresponds to model year 400 in the piControl)

exps='piControl historical rcp85'
realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1 r5i1p1 r6i1p1'

for exp in $exps; do
  python register_experiment.py 'IPSL-CM5A-LR' 'output/CMIP5/IPSL-CM5A-LR' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	for r in $realiz; do
	    python update_db_times.py 'IPSL-CM5A-LR' $v $exp $r
	done
    done
done

# realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'
# Y=2006
# while [ $Y -lt 2100 ]; do
#     for v in $vars; do
# 	for r in $realiz; do
# 	    id=`python ann_average_model.py IPSL-CM5A-LR $v rcp85 $r $Y`
# 	    id=`python remap_to_latlon.py $id`
# 	    id=`python remap_vertical.py $id`
# 	done
#     done
#     let Y=Y+1
# done

vars='thetao so'
for v in $vars; do
  id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'piControl' 'r1i1p1' '2000-01-14' '2004-12-15' PresentDay_ref_ctrl`
  id=`python remap_to_latlon.py $id`
  sleep 2s
  python remap_vertical.py $id
done

for v in $vars; do
  realiz='r2i1p1 r3i1p1 r4i1p1 r5i1p1'
  for r in $realiz; do
      id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'historical' $r '2000-01-14' '2004-12-15' PresentDay_ref`
      id=`python remap_to_latlon.py $id`
      sleep 2s
      python remap_vertical.py $id
  done
done

for v in $vars; do
    id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'piControl' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay_ctrl`
    id=`python remap_to_latlon.py $id`
    sleep 2s
    python remap_vertical.py $id
done

for v in $vars; do
 realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'
 for r in $realiz; do
     id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'rcp85' $r '2013-01-14' '2017-12-15' PresentDay`
     id=`python remap_to_latlon.py $id`
     id=`python remap_vertical.py $id`
 done
done

for v in $vars; do
   realiz='r2i1p1 r3i1p1 r4i1p1 r5i1p1'
    realiz='r1i1p1'
    for r in $realiz; do
	python time_average_model.py 'IPSL-CM5A-LR' $v 'historical' $r '1986-01-14' '2005-12-15' Future_ref
	id=`python remap_to_latlon.py $id`
	sleep 2s
	python remap_vertical.py $id
    done

    id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'piControl' 'r1i1p1' '1986-01-14' '2005-12-15' Future_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    sleep 2s
    python remap_vertical.py $id
    id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'piControl' 'r1i1p1' '2086-01-14' '2100-12-15' Future_ctrl`
    id=`python remap_to_latlon.py $id`
    sleep 2s
    python remap_vertical.py $id
    realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'
    for r in $realiz; do
    	id=`python time_average_model.py 'IPSL-CM5A-LR' $v 'rcp85' $r '2086-01-14' '2100-12-15' Future`
    	id=`python remap_to_latlon.py $id`
    	sleep 2s
    	python remap_vertical.py $id
    done
done

