#!/usr/bin/env bash

while getopts ":p:f:r:" opt; do
  case $opt in
    p) path="$OPTARG"
    ;;
    f) fname_mri="$OPTARG"
    ;;
    r) resources_path="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

start=`date +%s`

# Make surfaces with Freesurfer's watershed algorithm
#out_name=`basename ${fname_mri}`
#out_name="${out_name%%.*}"
#${resources_path}/bin/mri_watershed -useSRAS -surf ${path}/${out_name} ${path}/${fname_mri} ${path}/bems/ws

mri_watershed -useSRAS -surf ${path}/${out_name} ${path}/${fname_mri} ${path}/bems/ws


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

# invert z values. z values are the negative of surface RAS due to ITK coordinates (slicer will invert it)
z=${cras_array[2]}
if [[ $z == *"-"* ]]; then
  z=${z//-}
else
  z=-${z}
fi

text="""#Insight Transform File V1.0\n#Transform 0\nTransform:
      AffineTransform_double_3_3\nParameters: 1 0 0 0 1 0 0 0 1
      ${cras_array[0]} ${cras_array[1]} $z\nFixedParameters: 0 0 0"""

fname_transform=${path}/${out_name}_surf2mri.tfm
echo -e ${text} > ${fname_transform}
echo "Done"

end=`date +%s`
runtime=$((end-start))
echo Runtime: $((runtime)) seconds
