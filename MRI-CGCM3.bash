exps='piControl historical rcp85'
for exp in $exps; do
  python register_experiment.py 'MRI-CGCM3' '/net2/mjh/data/CMIP5/MRI-CGCM3' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'MRI-CGCM3' $v $exp 'r1i1p1'
	python update_db_times.py 'MRI-CGCM3' $v $exp 'r2i1p1'
    done
done

for v in $vars; do
    id=`python time_average_model.py 'MRI-CGCM3' $v 'piControl' 'r1i1p1' '2001-01-14' '2005-12-15' PresentDay_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'MRI-CGCM3' $v 'piControl' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'MRI-CGCM3' $v 'historical' 'r1i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'MRI-CGCM3' $v 'rcp85' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
done

for v in $vars; do
    id=`python time_average_model.py 'MRI-CGCM3' $v 'piControl' 'r1i1p1' '1986-01-14' '2005-12-15' Future_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'MRI-CGCM3' $v 'piControl' 'r1i1p1' '2086-01-14' '2100-12-15' Future_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'MRI-CGCM3' $v 'historical' 'r1i1p1' '1986-01-14' '2005-12-15' Future_ref`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'MRI-CGCM3' $v 'rcp85' 'r1i1p1' '2086-01-14' '2100-12-15' Future`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
done
