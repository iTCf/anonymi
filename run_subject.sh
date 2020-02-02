#!/bin/bash

# --- Run anonymization steps

f=$1
run_dir=$2
scripts_path=$3
slicer_exec=$4

# --- Create folder for running and move file
timestamp=`date "+%Y%m%d_%H%M%S"`
run_dir_inc=${run_dir}/inc_${timestamp}
mkdir ${run_dir_inc}
mv "${DIR}/${f}" "${run_dir_inc}"

# ---Run watershed
/bin/bash -e ${scripts_path}/run_fs.sh ${run_dir_inc}/${f} ${run_dir_inc} > ${run_dir_inc}/fs_log.txt

# ---Run Anonymi preparation script
/bin/bash -e ${scripts_path}/anonymi_prepare.sh -f ${f} -p ${run_dir_inc}

# --- Run Anonymi
${slicer_exec} --python-script ${scripts_path}/run_anonymi.py ${f}
