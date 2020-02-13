# Anony-MI

Anony-Mi is a tool for anonymizing MRIs which preserves the subject's anatomical geometry. It works as a 3D Slicer plug-in and can also be used as a standalone command line script.



ADD IMAGE



## Installation

### Requirements

It requires 3D Slicer (with two extra plug-ins) and Freesurfer. 

In order to install [3D Slicer](https://www.slicer.org/) please refer to their to their website. After it is installed, open 3D Slicer and go to the Extensions Manager (View > Extensions Manager). In the "Install Extensions" tab search for the VolumeClip and the SlicerElastix extensions and install them.

To install [Freesurfer](https://surfer.nmr.mgh.harvard.edu/) please refer to their website.

### Downloading

In order to download Anony-MI clone or download this repository:

 To do so, open a terminal, go to the folder you want to install download the software and run:

```
git clone (add final link)
```

or use the download button from GitHub.

### Adding the plug-in

Once you have downloaded it, open 3D Slicer, go to Settings (Edit > Application Settings) and in the Modules tab click on the Add button next to the Additional module paths section:

(Add image)



## Usage

The whole procedure takes ~15 minutes of computation time and ~2 minutes of manual intervention.

The complete pipeline involves:

1. Creating the anatomical surfaces (or copying them if they have already been computed) and preparing the necessary files.
3. Running the masking procedure.

Steps 1 can be performed using a single script provided in this repository (ADD LINK). Step 2 is performed using 3D Slicer's interface.

The anonymization procedure can also be run in batch, in order to process multiple images in an automatic way.



### 1. Creating the anatomical surfaces and preparing the files

The first step involves running a Freesurfer command to get the surfaces corresponding to the skin and skull of the subject and obtaining the transformation to align them propertly with the MRI.

To do so, open a terminal and run:

```
anonymi_prepare.sh -p path/to/subj_folder
```

This will create the surfaces, their _.vtk_ files and the _bem2mri.tfm_ transform.



### 2. Running the masking procedure

1. Open 3D Slicer and load the following files:

    - MRI to be anonymized.
    - _outer_skin.vtk_ & _outer_skull.vtk_
    - _bem2mri.tfm_

(Add image)

2. Then, go the the Modules selector and choose Anony-MI (Anonymization > Anony-MI).

(Add image)

3. Select your MRI as the Input Volume

4. Click on Get control points

5. Select the corresponding surfaces (models) and control points.

6. Click Apply

At this point you should see the anonymized MRI. You can make a 3D render in order to verify that it has been correctly anonymized. To do so, go to the Volume Rendering module, select the anonymized mri and make it visible.

(Add image)



### Batch processing

If you need to anonymize multiple MRIs, you can run them serially, by creating all the required files and then running the masking procedure in batch.

To do so, go to the Batch Processing section, click on Choose Batch Files, and select the _outer_skin_  files of all subjects that you want to run. Finally, click on Run Batch.





















