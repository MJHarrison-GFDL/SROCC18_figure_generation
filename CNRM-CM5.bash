# exps='piControl historical rcp85'
# for exp in $exps; do
#   python register_experiment.py 'CNRM-CM5' '/net2/mjh/data/CMIP5/CNRM-CM5' $exp
# done

# vars='thetao so'
# for exp in $exps; do
#     for v in $vars; do
# 	python update_db_times.py 'CNRM-CM5' $v $exp 'r1i1p1'
# 	python update_db_times.py 'CNRM-CM5' $v $exp 'r2i1p1'
# 	python update_db_times.py 'CNRM-CM5' $v $exp 'r3i1p1'
#     done
# done

# for v in $vars; do
#     id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '2000-01-14' '2004-12-15' PresentDay_ref_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     realizs='r1i1p1 r2i1p1 r3i1p1'
#     for p in $realizs; do
#     	id=`python time_average_model.py 'CNRM-CM5' $v 'historical' $p '2000-01-14' '2004-12-15' PresentDay_ref`
#     	id=`python remap_to_latlon.py $id`
#     	id=`python remap_vertical.py $id`
#     done
#     realizs='r1i1p1 r2i1p1'
#     for p in $realizs; do
#     	id=`python time_average_model.py 'CNRM-CM5' $v 'rcp85' $p '2013-01-14' '2017-12-15' PresentDay`
#     	id=`python remap_to_latlon.py $id`
#     	id=`python remap_vertical.py $id`
#     done
# done

# for v in $vars; do
#     id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '1985-01-14' '2005-12-15' Future_ref_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CNRM-CM5' $v 'piControl' 'r1i1p1' '2085-01-14' '2099-12-15' Future_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     realizs='r1i1p1 r2i1p1 r3i1p1'
#     for p in $realizs; do
# 	id=`python time_average_model.py 'CNRM-CM5' $v 'historical' $p '1985-01-14' '2005-12-15' Future_ref`
# 	id=`python remap_to_latlon.py $id`
# 	id=`python remap_vertical.py $id`
#     done
#     realizs='r1i1p1 r2i1p1'
#     for p in $realizs; do
# 	id=`python time_average_model.py 'CNRM-CM5' $v 'rcp85' $p '2085-01-14' '2099-12-15' Future`
# 	id=`python remap_to_latlon.py $id`
# 	id=`python remap_vertical.py $id`
#     done
# done

id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=PresentDay_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=PresentDay_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Present Day Ref Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi

realiz='r1i1p1 r2i1p1 r3i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=PresentDay_ref --realization=$r --scenario=historical --show=0`
    id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=PresentDay_ref --realization=$r --scenario=historical --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Present Day Ref ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi
done

id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=PresentDay_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=PresentDay_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Present Day Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi

realiz='r1i1p1 r2i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=PresentDay --realization=$r --scenario=rcp85 --show=0`
    id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=PresentDay --realization=$r --scenario=rcp85 --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Present Day ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi
done

realiz='r1i1p1 r2i1p1 r3i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=Future_ref --realization=$r --scenario=historical --show=0`
    id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=Future_ref --realization=$r --scenario=historical --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Future Ref ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi

done


id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=Future_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=Future_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Future Ref Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi


id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=Future_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=Future_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Future Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi

realiz='r1i1p1 r2i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CNRM-CM5 --var=thetao --name=Future --realization=$r --scenario=rcp85 --show=0`
    id_s=`python query_regridded.py --model=CNRM-CM5 --var=so --name=Future --realization=$r --scenario=rcp85 --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Future ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi
done
