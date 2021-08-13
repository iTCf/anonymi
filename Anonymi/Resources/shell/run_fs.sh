#!/bin/bash

# Run the watershed algorithm

file=$1
run_dir_inc=`dirname ${file}`
bname=`basename $file`
out_name="${bname%%.*}" # get filename without extension

mri_watershed -useSRAS -surf ${run_dir_inc}/${out_name} ${file} ${run_dir_inc}/ws
