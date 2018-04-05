python register_reanalysis.py 'GFDL_ECDA' 'obs/GFDL_ECDA/3.1'
vars='thetao so'
for v in $vars; do
    python update_reanalysis_db_times.py 'GFDL_ECDA' $v
done

Y=1995
while [ $Y -lt 2016 ]; do
    for v in $vars; do
  	id=`python ann_average_reanalysis.py GFDL_ECDA $v $Y`
  	id=`python remap_reanalysis_to_latlon.py $id`
  	id=`python remap_reanalysis_vertical.py $id`
    done
    let Y=Y+1
done

#for v in $vars; do
#    python time_average_reanalysis.py 'GFDL_ECDA' $v '2001-01-14' '2004-12-15' PresentDay_ref
#    id=`python remap_reanalysis_to_latlon.py $id`
#    id=`python remap_reanalysis_vertical.py $id`
#    id=`python time_average_reanalysis.py 'GFDL_ECDA' $v '2013-01-14' '2017-12-15' PresentDay`
#    id=`python remap_reanalysis_to_latlon.py $id`
#    id=`python remap_reanalysis_vertical.py $id`
#done

