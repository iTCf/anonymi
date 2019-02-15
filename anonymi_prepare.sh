#!/usr/bin/env bash

while getopts ":p:f:" opt; do
  case $opt in
    p) path="$OPTARG"
    ;;
    f) file="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done


# Convert bem


#mris_convert $(path)/$(file)

fpath=${path}/${file}
echo ${fpath}
cras=$(mri_info ${fpath} --cras)
echo ${cras}

cras_array=($cras)

text="#Insight Transform File V1.0\n#Transform 0\nTransform:
      AffineTransform_double_3_3\nParameters: 1 0 0 0 1 0 0 0 1
      ${cras_array[0]} ${cras_array[1]} -${cras_array[2]}\nFixedParameters: 0 0 0"

fname_transform=${path}/bem2mri.tfm
echo -e ${text} > bem2mri.tfm
