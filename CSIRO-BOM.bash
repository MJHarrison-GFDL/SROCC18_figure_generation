#!/bin/bash
# CSIRO-BOM experiments (offset by 1351 years, i.e. calendar year 2100 corresponds to model year 749 in the piControl)

exps='piControl historical rcp85'
for exp in $exps; do
  python register_experiment.py 'CSIRO-BOM' '/net2/mjh/data/CMIP5/CSIRO-BOM' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'CSIRO-BOM' $v $exp 'r1i1p1'
    done
done

for v in $vars; do
   id=`python time_average_model.py 'CSIRO-BOM' $v 'piControl' 'r1i1p1' '0650-01-14' '0654-12-15' PresentDay_ref_ctrl`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id=`python time_average_model.py 'CSIRO-BOM' $v 'piControl' 'r1i1p1' '0663-01-14' '0667-12-15' PresentDay_ctrl`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id=`python time_average_model.py 'CSIRO-BOM' $v 'historical' 'r1i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id=`python time_average_model.py 'CSIRO-BOM' $v 'rcp85' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
done

for v in $vars; do
    id=`python time_average_model.py 'CSIRO-BOM' $v 'piControl' 'r1i1p1' '0635-01-14' '0655-12-15' Future_ref_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CSIRO-BOM' $v 'piControl' 'r1i1p1' '0729-01-14' '0749-12-15' Future_ctrl`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CSIRO-BOM' $v 'historical' 'r1i1p1' '1986-01-14' '2006-12-15' Future_ref`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
    id=`python time_average_model.py 'CSIRO-BOM' $v 'rcp85' 'r1i1p1' '2086-01-14' '2100-12-15' Future`
    id=`python remap_to_latlon.py $id`
    id=`python remap_vertical.py $id`
done
