#!/bin/bash
# CM3 experiments (offset by 1600 years, i.e. calendar year 2000 corresponds to model year 400 in the piControl)

exps='piControl historical rcp85'
for exp in $exps; do
  python register_experiment.py 'CM3' 'output/CMIP5/CM3' $exp
done

# realiz='r1i1p1'
# Y=2006
# while [ $Y -lt 2100 ]; do
#     for v in $vars; do
# 	for r in $realiz; do
# 	    id=`python ann_average_model.py CM3 $v rcp85 $r $Y`
# 	    id=`python remap_to_latlon.py $id`
# 	    id=`python remap_vertical.py $id`
# 	done
#     done
#     let Y=Y+1
# done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'CM3' $v $exp 'r1i1p1'
	python update_db_times.py 'CM3' $v $exp 'r2i1p1'
	python update_db_times.py 'CM3' $v $exp 'r3i1p1'
	python update_db_times.py 'CM3' $v $exp 'r4i1p1'
    done
done

ensembles="r1i1p1 r2i1p1 r3i1p1 r4i1p1"

for v in $vars; do
    for p in $ensembles; do
	id=`python time_average_model.py 'CM3' $v 'historical' $p '2001-01-14' '2005-12-15' PresentDay_ref`
	id=`python remap_to_latlon.py $id`
	id=`python remap_vertical.py $id`
    done
    id=`python time_average_model.py 'CM3' $v 'piControl' r1i1p1 '0401-01-14' '0405-12-15' PresentDay_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CM3' $v 'piControl' 'r1i1p1' '0416-01-14' '0420-12-15' PresentDay_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CM3' $v 'rcp85' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
done

for v in $vars; do
    for p in $ensembles; do
	id=`python time_average_model.py 'CM3' $v 'historical' $p '1986-01-14' '2005-12-15' Future_ref`
	id=`python remap_to_latlon.py $id`
	id=`python remap_vertical.py $id`
    done
    id=`python time_average_model.py 'CM3' $v 'piControl' 'r1i1p1' '0386-01-14' '0405-12-15' Future_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CM3' $v 'piControl' 'r1i1p1' '0486-01-14' '0500-12-15' Future_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CM3' $v 'rcp85' 'r1i1p1' '2086-01-14' '2100-12-15' Future`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
done
