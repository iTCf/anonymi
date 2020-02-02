#!/bin/bash

# set path to watch
DIR="/home/eze/imaging/anonym/incoming"
# set path for main running folder
run_dir="/home/eze/imaging/anonym/run_dir"
# set path of scripts
scripts_path="/home/eze/scripts/anonymi"
#set path of slicer
slicer_ecec="/home/eze/soft/Slicer-4.10.2-linux-amd64/Slicer"

# setup watch
inotifywait -m -e moved_to -e create "$DIR" --format "%f" | while read f

# run as files arrive
do
  # TODO: check if is folder and run in batch
    echo $f
    /bin/bash -e ${scripts_path}/run_subject.sh ${f} ${run_dir} ${scripts_path} ${slicer_ecec}
    echo Done
done
