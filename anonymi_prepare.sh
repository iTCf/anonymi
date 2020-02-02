#!/usr/bin/env bash

while getopts ":p:f:" opt; do
  case $opt in
    p) path="$OPTARG"
    ;;
    f) fname_mri="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

# Convert bem surfaces to .vtk
echo "Converting surfaces"
for file in ${path}/*outer*
do
  if [ ! -f $file.vtk ]; then
      mris_convert $file $file.vtk
  fi
done

# Create transform file, from surface to mri space
echo "Creating transform file"
# mri=${path}/T1.mgz
mri=${fname_mri}
cras=$(mri_info ${mri} --cras)

cras_array=($cras)

# invert z values. z values are the negative of surfacer RAS due to ITK coordinates (slicer will invert it)
z=${cras_array[2]}
if [[ $z == *"-"* ]]; then
  z=${z//-}
else
  z=-${z}
fi

text="#Insight Transform File V1.0\n#Transform 0\nTransform:
      AffineTransform_double_3_3\nParameters: 1 0 0 0 1 0 0 0 1
      ${cras_array[0]} ${cras_array[1]} $z\nFixedParameters: 0 0 0"

fname_transform=${path}/bem2mri.tfm
echo -e ${text} > bem2mri.tfm
echo "Done"
