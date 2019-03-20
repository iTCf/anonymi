# Anonymi

## 1. Prepare files

### 1.1. Copy required files

Copy the T1 MRI (T1.mgz) and the outer skin and skull surface files to a folder


### 1.2. Run preparation script

run:

```
anonymi_prepare.sh -p path/to/subj_folder
```
This will create the vtk files for the surfaces and the bem2mri.tfm transform



## 2. Set control points

In Slicer, open the Markups module and mark the control points for the Face and the Left and Right Ears:

imgs

## 3. Run Anonymi





