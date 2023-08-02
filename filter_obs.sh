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

obs_files=(${obs_dir}/*.h5)
for ob in "${obs_files[@]}"
do
  echo Processing: ${ob}
  obs_filename=$(basename -- "${ob}")
  obs_filename_base=${obs_filename%.*}
  mask_filename=mask_"${obs_filename}"
  mask_dirname=$(dirname -- $(dirname -- "${ob}"))/maskOut
  mask_fqn="${mask_dirname}"/"${mask_filename}"
  ./filter_obs.py "${static_file}" "${ob}" "${mask_fqn}"
  
  examples/plot_obs.py "${ob}" --output "${obs_filename_base}".png
  examples/plot_obs.py "${ob}" --mask-file "${mask_fqn}" --output "${obs_filename_base}"_mask.png
 
done

