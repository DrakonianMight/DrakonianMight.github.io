#!/bin/bash
# My first script

echo starting scripts

#set broken conda binary location (yuk!)
export PROJ_LIB=/home/leo/anaconda3/envs/mlenv/share/proj

start=`date +%s`

# create ECMWF Pressure data
/home/leo/anaconda3/envs/mlenv/bin/python /home/leo/Python/web_projects/DrakonianMight.github.io/python/create_animations_ECMWF.py
echo "Duration: $((($(date +%s)-$start)/60))"

# create NOAA WW3 latest grid animations
/home/leo/anaconda3/envs/mlenv/bin/python /home/leo/Python/web_projects/DrakonianMight.github.io/python/grid_animations.py
echo "Duration: $((($(date +%s)-$start)/60))"

# create NOAA WW3 actual and forecast
/home/leo/anaconda3/envs/mlenv/bin/python /home/leo/Python/web_projects/DrakonianMight.github.io/python/create_plot_page_NOAA_WW3.py
echo "Duration: $((($(date +%s)-$start)/60))"
