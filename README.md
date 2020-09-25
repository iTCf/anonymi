# Anony-MI

Anony-Mi is a tool for anonymizing MRIs which preserves the subject's anatomical geometry. It works as a 3D Slicer Extension and can also be used as a standalone command line script.



ADD IMAGE



For a detailed explanation of the procedure please refer to [add publication].

<br/>

## Installation

### Downloading

In order to download Anony-MI clone or download this repository:

 To do so, open a terminal, go to the folder you want to install download the software and run:

```
git clone (add final link)
```

or use the download button from GitHub.

Once you have it, place it in your computer on a folder of your choosing.

<br/>

### Requirements

It requires 3D Slicer (with two extra plug-ins). In order to install [3D Slicer](https://www.slicer.org/) please refer to their to their website. After it is installed, open 3D Slicer and go to the Extensions Manager (View > Extensions Manager). In the "Install Extensions" tab search for the VolumeClip and the SlicerElastix extensions and install them.

AnonyMI uses some [Freesurfer](https://surfer.nmr.mgh.harvard.edu/) functions that are already included in it, but require a Freesurfer license to be used. Obtaining a Freesurfer license es free and fast. Fill this [form](https://surfer.nmr.mgh.harvard.edu/registration.html)  and you will receive it via e-mail. Copy the indicated text and put it inside the Resources folder of AnonyMI once you have downloaded it. If you already have a freesurfer's license, just copy the file.

```shell
.
├── Anonymi
│   ├── Anonymi.py
│   ├── Anonymi.pyc
│   ├── CMakeLists.txt
│   ├── Resources  <------------------- INTO THIS FOLDER
│   │   ├── Icons
│   │   ├── anonymi_cli.py
│   │   ├── average
│   │   ├── bin
│   │   ├── imgs
│   │   ├── lib
│   │   ├── license.txt  <------------- HERE
│   │   ├── run_anonymi.py
│   │   ├── shell
│   │   └── templates
│   └── Testing
│       ├── CMakeLists.txt
│       └── Python
├── Anonymi.png
├── CMakeLists.txt
└── README.md
```

<br/>

### Adding the plug-in

Once you have downloaded it, open 3D Slicer, go to Settings (Edit > Application Settings) and in the Modules tab click on the Add button next to the Additional module paths section. This step has to be done only once.

![addplug](Anonymi/Resources/imgs/man_addplugin.png)



<br/>

## Usage

AnonyMI can be used either automatically or manually. Automatic operation will perform the whole process by simply pressing two buttons. It is the fastest way of performing the anonymization procedure. Manual operation allows for precise fine-tuning of the areas to be anonymized, which can be useful for particularly difficult cases.

In both cases the procedure is divided in two steps. 1) Preparing the files (~10 minutes) and 2) Running the algorithm (~1 minute).

To open AnonyMI's interface go to the Modules menu in Slicer and under Anonymization you will find AnonyMI.

<img src="Anonymi/Resources/imgs/man_findanonymi.png" alt="find" style="zoom:65%;" />

<br/>

### Preparing the files

This involves several steps that are executed in sequence by choosing one or more MRI files.

Press the _Prepare Files_ button, navigate to the folder where you have your MRIs and choose one or more MRI files. If you choose multiple files their preparation will be performed in sequence. It is advisable to copy all the MRIs you want to anonymize on one folder, this way, selecting the files will be faster and you will always have a back-up.

<img src="Anonymi/Resources/imgs/man_prepare.png" alt="img" style="zoom:50%;" />

<br/>

### Automatic Mode

To automatically anonymize one or more MRIs follow these steps

1. Press the button _Select files to Run_ in the Automatic Processing section, navigate to the folder where the MRIs are located and choose the files corresponding to the subject or subjects you want to process. The possible files to be selected will be highlighted (you only need to select the files ending in _outer_skin_surface.vtk_).

2. Press the _Run_ button on the Automatic Processing section.

<img src="/Users/lpen/scripts/anonymi/Anonymi/Resources/imgs/man_runauto.png" alt="auto" style="zoom:50%;" />

<br/>

### Manual Mode

To run the anonymization in manual mode follow these steps.

1. Load the files that have been prepared for the subject you want to anonymize (see Preparing Files above) using Slicer's interface:

   (Add image)

2. Select the appropriate files on the _Input Volume_, _Surface to MRI transform_, _Outer skin model_, _Outer skull model_.

   (Add image)

3. At this point AnonyMI can identify the face and ears areas by itself or you can indicate them yourself (see below for the latter procedure). To find the face and ears areas press the _Get control points_ button.

4. Press _Apply_.



After it finishes you will be able to see the anonymized MRI and also to create a 3D render of it to observe the results (see below).

<br/>

#### Manual control points

In the example above the control points used for finding the portions to be masked were automatically determined. However, in some cases it is preferable to set them manually, for example if there are certain non-standard areas that would need to be masked, or if the template doesn't match the subject, as would be the case for young subjects. 

In order to manually assign the control points:



(Add instructions)

<br/>

#### Group Specific Templates

To create a custom template:

1. Run the _Prepare Files_ process on the MRI that you want to use as a template as explained above.

2. Manually mark the control points as explained above.

3. Save the control points using Slicer's interface naming the according to the following convention

   (Add image)



To run the process, either manually or automatically:

1. Mark the _Use Custom Template_ box in the Template section

2. Press the _Select Custom Template_ button in the Template section and select the MRI you want to use.
3. Run the anonymization process either manually or automatically as explained above.

<br/>

#### 3D Rendering of Results

To create a 3D render of the anoymized MRI:

1. Open the Volume Rendering module on the modules section.
2. Select the anonymized Volume (or the original MRI if you want to compare them)
3. Click the eye symbol.

The render will appear on the 3D View panel.























