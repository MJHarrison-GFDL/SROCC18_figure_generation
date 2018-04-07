# ESM2M experiments (offset by 1600 years, i.e. calendar year 2000 corresponds to model year 400 in the piControl)

exps='piControl historical rcp26 rcp85'
realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'

# for exp in $exps; do
#   python register_experiment.py 'CCSM4' 'output/CMIP5/CCSM4' $exp
# done

# vars='thetao so'
# for exp in $exps; do
#     for v in $vars; do
# 	for r in $realiz; do
# 	    python update_db_times.py 'CCSM4' $v $exp $r
# 	done
#     done
# done

echo "Finished updating time info"

# Y=2006
# while [ $Y -lt 2100 ]; do
#     for v in $vars; do
# 	for r in $realiz; do
# 	    id=`python ann_average_model.py CCSM4 $v rcp85 $r $Y`
# 	    id=`python remap_to_latlon.py $id`
# 	    id=`python remap_vertical.py $id`
# 	done
#     done
#     let Y=Y+1
# done


# for v in $vars; do
#     id=`python time_average_model.py 'CCSM4' $v 'piControl' 'r1i1p1' '1201-01-14' '1205-12-15' PresentDay_ref_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'piControl' 'r1i1p1' '1214-01-14' '1218-12-15' PresentDay_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'historical' 'r1i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'historical' 'r2i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'historical' 'r3i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'historical' 'r4i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'rcp85' 'r1i1p1' '2014-01-14' '2018-12-15' PresentDay`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'rcp85' 'r2i1p1' '2014-01-14' '2018-12-15' PresentDay`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     id=`python time_average_model.py 'CCSM4' $v 'rcp85' 'r3i1p1' '2014-01-14' '2018-12-15' PresentDay`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
# done


# echo "Finished processing PresentDay output"
# for v in $vars; do
#     id=`python time_average_model.py 'CCSM4' $v 'piControl' 'r1i1p1' '1181-01-14' '1199-12-15' Future_ref_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     echo "Finished processing Future_ref_ctrl $v output "
#     id=`python time_average_model.py 'CCSM4' $v 'piControl' 'r1i1p1' '1281-01-14' '1299-12-15' Future_ctrl`
#     id=`python remap_to_latlon.py $id`
#     id=`python remap_vertical.py $id`
#     echo "Finished processing Future_ctrl $v output"
#     realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'
#     for r in $realiz; do
#       id=`python time_average_model.py 'CCSM4' $v 'historical' $r '1986-01-14' '2004-12-15' Future_ref`
#       id=`python remap_to_latlon.py $id`
#       id=`python remap_vertical.py $id`
#       echo "Finished processing Future_ref $v output for $r"
#     done
#     realiz='r1i1p1 r2i1p1 r3i1p1'
#     for r in $realiz; do
#       id=`python time_average_model.py 'CCSM4' $v 'rcp85' 'r1i1p1' '2086-01-14' '2099-12-15' Future`
#       id=`python remap_to_latlon.py $id`
#       id=`python remap_vertical.py $id`
#       echo "Finished processing Future $v output for $r"
#     done
# done

# echo "Finished processing Future output"

id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=PresentDay_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CCSM4 --var=so --name=PresentDay_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Present Day Ref Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi

realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=PresentDay_ref --realization=$r --scenario=historical --show=0`
    id_s=`python query_regridded.py --model=CCSM4 --var=so --name=PresentDay_ref --realization=$r --scenario=historical --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Present Day Ref ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi
done

id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=PresentDay_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CCSM4 --var=so --name=PresentDay_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Present Day Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi

realiz='r1i1p1 r2i1p1 r3i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=PresentDay --realization=$r --scenario=rcp85 --show=0`
    id_s=`python query_regridded.py --model=CCSM4 --var=so --name=PresentDay --realization=$r --scenario=rcp85 --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Present Day ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi
done

realiz='r1i1p1 r2i1p1 r3i1p1 r4i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=Future_ref --realization=$r --scenario=historical --show=0`
    id_s=`python query_regridded.py --model=CCSM4 --var=so --name=Future_ref --realization=$r --scenario=historical --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Future Ref ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi

done


id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=Future_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CCSM4 --var=so --name=Future_ref_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Future Ref Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi


id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=Future_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
id_s=`python query_regridded.py --model=CCSM4 --var=so --name=Future_ctrl --realization=r1i1p1 --scenario=piControl --show=0`
if [ $id_t -gt 0 ]; then
    if [ $id_s -gt 0 ]; then
	echo 'Future Ctrl r1i1p1 ' $id_t $id_s
	python compute_density_model.py $id_t $id_s
    fi
fi

realiz='r1i1p1 r2i1p1 r3i1p1'
for r in $realiz; do
    id_t=`python query_regridded.py --model=CCSM4 --var=thetao --name=Future --realization=$r --scenario=rcp85 --show=0`
    id_s=`python query_regridded.py --model=CCSM4 --var=so --name=Future --realization=$r --scenario=rcp85 --show=0`
    if [ $id_t -gt 0 ]; then
	if [ $id_s -gt 0 ]; then
	    echo 'Future ' $r $id_t $id_s
	    python compute_density_model.py $id_t $id_s
	fi
    fi
done
