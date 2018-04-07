# ESM2M experiments (offset by 1600 years, i.e. calendar year 2000 corresponds to model year 400 in the piControl)

exps='piControl historical rcp85'

for exp in $exps; do
 python register_experiment.py 'ESM2G' 'output/CMIP5/ESM2G' $exp
done

vars='thetao so'
for exp in $exps; do
    for v in $vars; do
	python update_db_times.py 'ESM2G' $v $exp 'r1i1p1'
	python update_db_times.py 'ESM2G' $v $exp 'r2i1p1'
    done
done

id_pd_ref_ctrl=''
id_pd_ctrl=''
id_pd_ref=''
id_pd=''
for v in $vars; do
   id=`python time_average_model.py 'ESM2G' $v 'piControl' 'r1i1p1' '0401-01-14' '0405-12-15' PresentDay_ref_ctrl`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id_pd_ref_ctrl="$id_pd_ref_ctrl $id"
   id=`python time_average_model.py 'ESM2G' $v 'piControl' 'r1i1p1' '0416-01-14' '0420-12-15' PresentDay_ctrl`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id_pd_ctrl="$id_pd_ctrl $id"
   id=`python time_average_model.py 'ESM2G' $v 'historical' 'r2i1p1' '2001-01-14' '2005-12-15' PresentDay_ref`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id_pd_ref="$id_pd_ref $id"
   id=`python time_average_model.py 'ESM2G' $v 'rcp85' 'r1i1p1' '2013-01-14' '2017-12-15' PresentDay`
   id=`python remap_to_latlon.py $id`
   id=`python remap_vertical.py $id`
   id_pd="$id_pd $id"
done

set -- $id_pd_ref_ctrl
python compute_density_model.py $1 $2
set -- $id_pd_ctrl
python compute_density_model.py $1 $2
set -- $id_pd_ref
python compute_density_model.py $1 $2
set -- $id_pd
python compute_density_model.py $1 $2

id_future_ref_ctrl=''
id_future_ctrl=''
id_future_ref=''
id_future=''
for v in $vars; do
  id=`python time_average_model.py 'ESM2G' $v 'piControl' 'r1i1p1' '0386-01-14' '0405-12-15' Future_ref_ctrl`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id_future_ref_ctrl="$id_future_ref_ctrl $id"
  id=`python time_average_model.py 'ESM2G' $v 'piControl' 'r1i1p1' '0486-01-14' '0500-12-15' Future_ctrl`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id_future_ctrl="$id_future_ctrl $id"
  id=`python time_average_model.py 'ESM2G' $v 'historical' 'r2i1p1' '1986-01-14' '2005-12-15' Future_ref`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id_future_ref="$id_future_ref $id"
  id=`python time_average_model.py 'ESM2G' $v 'rcp85' 'r1i1p1' '2086-01-14' '2100-12-15' Future`
  id=`python remap_to_latlon.py $id`
  id=`python remap_vertical.py $id`
  id_future="$id_future $id"
done

set -- $id_future_ref_ctrl
python compute_density_model.py $1 $2
set -- $id_future_ctrl
python compute_density_model.py $1 $2
set -- $id_future_ref
python compute_density_model.py $1 $2
set -- $id_future
python compute_density_model.py $1 $2

# Y=2006
# vars='thetao'
# while [ $Y -lt 2100 ]; do
#     for v in $vars; do
# 	id=`python ann_average_model.py ESM2G $v rcp85 r1i1p1 $Y`
# 	id=`python remap_to_latlon.py $id`
# 	id=`python remap_vertical.py $id`
#     done
#     let Y=Y+1
# done
