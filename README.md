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

# Description

Model output from piControl,historical and rcp runs are located in output/CMIP5/model_name

Information on the current state of the data processing are contained in a simple Python database - cmip5.db and reanalyses.cb

The database was populated by executing the bash scripts, one for each model, contained in this directory. Processing occurs in stages:

* time-averages for assigned date ranges defined as PresentDay and Future and associated reference time periods for calculating a change in the ocean state
* regridding to a common lat-lon grid
* remapping in the vertical to a common depth grid

The time periods defined here are (subject to change):

* PresentDay reference :2001-2005
* PresentDay:2013-2017
* Future reference:1986-2005
* Future:2086-2100

Changes in the ocean state are defined with respecting to changes in the piControl run.

# Usage


Ocean heating rates over the top 700m for PresentDay and Future Scenarios for all ensemble members (using a range of -5 to 5 W m-2)

python OCCC_figs.py --type=heat_maps --ztop=0 --zbot=700 --vmin=-5 --vmax=5

Output: heating_map_0to700_present.png,heating_map_0to700_future.png

Ocean heating rates from 700m to 2000m for PresentDay and Future Scenarios for CCSM4  (using a range of -5 to 5 W m-2)


python OCCC_figs.py --type=heat_maps --ztop=700 --zbot=2000 --vmin=-5 --vmax=5 --model=CCSM4

Output: heating_map_700to2000_present.png,heating_map_700to2000_future.png

Zonal Average temperature and salinity changes for PresentDay and Future Scenarios for BCC-CSM1-1 (global,Pacific,Atlantic+Arctic,Indian)

python OCCC_figs.py --type=zonal_avgs --model=BCC-CSM1-1

Output: {Atlantic,Global,Indian,Pacific}_zonal_{thetao,so}_{present,future}.png

Zonal Average temperature and salinity changes for PresentDay and Future Scenarios for all ensemble members (global,Pacific,Atlantic+Arctic,Indian)

python OCCC_figs.py --type=zonal_avgs

