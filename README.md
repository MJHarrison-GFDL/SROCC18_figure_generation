# SROCC18_figure_generation
Python and CDO software for the generation of CMIP5 ocean output on a common lat/lon/depth grid and figures


# Requirements

* python2 (https://www.python.org/)
* MIDAS python package (https:github.com/mjharriso/MIDAS)
* Climate Data Operator (CDO) (https://code.mpimet.mpg.de/projects/cdo/)

# Recommended

* anaconda ( https://anaconda.org/ )

## Installation

(asumed Python and Anaconda are installed)

* conda install -c matthewharrison midas
* conda install cartopy
* pip install dataset
* Install cdo package following instructions on website (http://www.studytrails.com/blog/install-climate-data-operator-cdo-with-netcdf-grib2-and-hdf5-support/)

# Usage


Ocean heating rates over the top 700m for PresentDay and Future Scenarios for all ensemble members (using a range of -5 to 5 W m-2)

python OCCC_figs.py --type=heat_maps --ztop=0 --zbot=700 --vmin=-5 --vmax=5


Ocean heating rates from 700m to 2000m for PresentDay and Future Scenarios for CCSM4  (using a range of -5 to 5 W m-2)


python OCCC_figs.py --type=heat_maps --ztop=0 --zbot=700 --vmin=-5 --vmax=5 --model=CCSM4


Zonal Average temperature and salinity changes for PresentDay and Future Scenarios for BCC-CSM1-1 (global,Pacific,Atlantic+Arctic,Indian)

python OCCC_figs.py --type=zonal_avgs --model=BCC-CSM1-1

Zonal Average temperature and salinity changes for PresentDay and Future Scenarios for all ensemble members (global,Pacific,Atlantic+Arctic,Indian)

python OCCC_figs.py --type=zonal_avgs

