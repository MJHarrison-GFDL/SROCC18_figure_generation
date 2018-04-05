exps='piControl historical rcp85'
for exp in $exps; do
  python register_experiment.py 'CNRM-CM5' '/net2/mjh/data/CMIP5/CNRM-CM5' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'CNRM-CM5' $v $exp 'r1i1p1'
	python update_db_times.py 'CNRM-CM5' $v $exp 'r2i1p1'
	python update_db_times.py 'CNRM-CM5' $v $exp 'r3i1p1'
    done
done

for v in $vars; do
    id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '2000-01-14' '2004-12-15' PresentDay_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    realizs='r1i1p1 r2i1p1 r3i1p1'
    for p in $realizs; do
    	id=`python time_average_model.py 'CNRM-CM5' $v 'historical' $p '2000-01-14' '2004-12-15' PresentDay_ref`
    	id=`python remap_to_latlon.py $id`
    	id=`python remap_vertical.py $id`
    done
    realizs='r1i1p1 r2i1p1'
    for p in $realizs; do
    	id=`python time_average_model.py 'CNRM-CM5' $v 'rcp85' $p '2013-01-14' '2017-12-15' PresentDay`
    	id=`python remap_to_latlon.py $id`
    	id=`python remap_vertical.py $id`
    done
done

for v in $vars; do
    id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '1985-01-14' '2005-12-15' Future_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '2085-01-14' '2099-12-15' Future_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    realizs='r1i1p1 r2i1p1 r3i1p1'
    for p in $realizs; do
	id=`python time_average_model.py 'CNRM-CM5' $v 'historical' $p '1985-01-14' '2005-12-15' Future_ref`
	id=`python remap_to_latlon.py $id`
	id=`python remap_vertical.py $id`
    done
    realizs='r1i1p1 r2i1p1'
    for p in $realizs; do
	id=`python time_average_model.py 'CNRM-CM5' $v 'rcp85' $p '2085-01-14' '2099-12-15' Future`
	id=`python remap_to_latlon.py $id`
	id=`python remap_vertical.py $id`
    done
done
