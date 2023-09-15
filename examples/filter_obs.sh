#/usr/bin/bash

# get list of observations

# location of static MPAS domain file
static_file=$1

# Observation file direcotry
if [ "$#" == 0 ]; then
  echo "usage:"
  exit
elif [ "$#" == 1 ]; then
  obs_dir=`pwd` 
else
  obs_dir=$2
fi

#obs_files="${obs_dir}"/*.h5
obs_dir=${HOME}/workspace/obs_io_testing/dbIn
echo "${obs_dir}"
obs_files="${obs_dir}"/*.h5
for ob in ${obs_files[@]}
do
  echo "${ob}"
  echo Processing: ${ob}
  ob_filename=$(basename -- "${ob}")
  ob_filename_base=${ob_filename%.*}
  filtered_ob_filename=filtered_"${ob_filename}"
  filtered_ob_dirname=$(dirname -- $(dirname -- "${ob}"))/maskOut
  filtered_ob_fqn="${filtered_ob_dirname}"/"${filtered_ob_filename}"
  ./filter_obs.py "${static_file}" "${ob}" "${filtered_ob_fqn}"
  
  ./plot_obs.py "${ob}" --output "${ob_filename_base}".png
  ./plot_obs.py "${filtered_ob_fqn}" --output "${ob_filename_base}"_filtered.png
done

