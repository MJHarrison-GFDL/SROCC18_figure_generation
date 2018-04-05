exps='piControl historical rcp85'
for exp in $exps; do
  python register_experiment.py 'CMCC-CESM' 'output/CMIP5/CMCC-CESM' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'CMCC-CESM' $v $exp 'r1i1p1'
    done
done

# realiz='r1i1p1'
# Y=2006
# while [ $Y -lt 2100 ]; do
#     for v in $vars; do
# 	for r in $realiz; do
# 	    id=`python ann_average_model.py CMCC-CESM $v rcp85 $r $Y`
# 	    id=`python remap_to_latlon.py $id`
# 	    id=`python remap_vertical.py $id`
# 	done
#     done
#     let Y=Y+1
# done

for v in $vars; do
    id=`python time_average_model.py 'CMCC-CESM' $v 'piControl' 'r1i1p1' '4514-01-14' '4518-12-15' PresentDay_ref_ctrl`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CMCC-CESM' $v 'piControl' 'r1i1p1' '4527-01-14' '4531-12-15' PresentDay_ctrl`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CMCC-CESM' $v 'historical' 'r1i1p1' '2001-01-14' '2004-12-15' PresentDay_ref`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CMCC-CESM' $v 'rcp85' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
done

for v in $vars; do
    id=`python time_average_model.py 'CMCC-CESM' $v 'piControl' 'r1i1p1' '4486-01-14' '4505-12-15' Future_ref_ctrl`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CMCC-CESM' $v 'piControl' 'r1i1p1' '4586-01-14' '4600-12-15' Future_ctrl`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CMCC-CESM' $v 'historical' 'r1i1p1' '1986-01-14' '2005-12-15' Future_ref`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CMCC-CESM' $v 'rcp85' 'r1i1p1' '2086-01-14' '2100-12-15' Future`
    id=`python remap_to_latlon.py $id fill`
    id=`python remap_vertical.py $id`
done
