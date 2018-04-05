
python register_reanalysis.py 'ECCO' 'obs/ECCO/v4/r3'
vars='thetao so'
for v in $vars; do
   python update_reanalysis_db_times.py 'ECCO' $v
done


Y=1992
while [ $Y -lt 1993 ]; do
    for v in $vars; do
	    python ann_average_reanalysis.py ECCO $v $Y
#	    id=`python remap_reanalysis_to_latlon.py $id`
#	    id=`python remap_reanalysis_vertical.py $id`
    done
    let Y=Y+1
done

# for v in $vars; do
#    python time_average_reanalysis.py 'GFDL_ECDA' $v '2001-01-14' '2004-12-15' PresentDay_ref
#    id=`python remap_reanalysis_to_latlon.py $id`
#    id=`python remap_reanalysis_vertical.py $id`
#    id=`python time_average_reanalysis.py 'GFDL_ECDA' $v '2013-01-14' '2017-12-15' PresentDay`
#    id=`python remap_reanalysis_to_latlon.py $id`
#    id=`python remap_reanalysis_vertical.py $id`
# done


