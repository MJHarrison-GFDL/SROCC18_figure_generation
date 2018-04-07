#model='MRI-CGCM3'
#python OCCC_figs.py --type=heat_maps --ztop=0 --zbot=700  --vmin=-5 --vmax=5 --model=$model
#python OCCC_figs.py --type=heat_maps --ztop=700 --zbot=2000  --vmin=-5 --vmax=5 --model=$model
#python OCCC_figs.py --type=zonal_sections --model=$model
#python OCCC_figs.py --type=zonal_density_sections --model=$model

python OCCC_figs.py --type=heat_maps --ztop=0 --zbot=700  --vmin=-5 --vmax=5
python OCCC_figs.py --type=heat_maps --ztop=700 --zbot=2000  --vmin=-5 --vmax=5
python OCCC_figs.py --type=zonal_sections
#python OCCC_figs.py --type=zonal_density_sections


