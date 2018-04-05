# ESM2M experiments (offset by 1600 years, i.e. calendar year 2000 corresponds to model year 400 in the piControl)

exps='piControl historical rcp26 rcp85'

for exp in $exps; do
 python register_experiment.py 'ESM2M' 'output/CMIP5/ESM2M' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'ESM2M' $v $exp 'r1i1p1'
    done
done

for v in $vars; do
   id=`python time_average_model.py 'ESM2M' $v 'piControl' 'r1i1p1' '0401-01-14' '0405-12-15' PresentDay_ref_ctrl`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id=`python time_average_model.py 'ESM2M' $v 'piControl' 'r1i1p1' '0416-01-14' '0420-12-15' PresentDay_ctrl`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id=`python time_average_model.py 'ESM2M' $v 'historical' 'r1i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id=`python time_average_model.py 'ESM2M' $v 'rcp85' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
done

for v in $vars; do
  id=`python time_average_model.py 'ESM2M' $v 'piControl' 'r1i1p1' '0386-01-14' '0405-12-15' Future_ref_ctrl`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id=`python time_average_model.py 'ESM2M' $v 'piControl' 'r1i1p1' '0486-01-14' '0500-12-15' Future_ctrl`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id=`python time_average_model.py 'ESM2M' $v 'historical' 'r1i1p1' '1986-01-14' '2005-12-15' Future_ref`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id=`python time_average_model.py 'ESM2M' $v 'rcp85' 'r1i1p1' '2086-01-14' '2100-12-15' Future`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
done

# Y=2006
# vars='thetao'
# exps='rcp26 rcp85'
# while [ $Y -lt 2100 ]; do
#     for exp in $exps; do
# 	for v in $vars; do
# 	    id=`python ann_average_model.py ESM2M $v $exp r1i1p1 $Y`
# 	    id=`python remap_to_latlon.py $id`
# 	    id=`python remap_vertical.py $id`
# 	done
#     done
#     let Y=Y+1
# done
