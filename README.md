# Anonymi

## 1. Convert outer_skin_surface (output of make_bem) to vtk

[import directly into slicer?]

Using freesurfer:

```bash
mris_convert sname_outer_skin_surface sname_outer_skin_surface.vtk
```



## 2. Get MRI origin:

Using freesurfer:

```bash
mri_info --cras MRI_name.mgz
```



## 3. Load MRI and surface on Slicer:

Data -> Choose File(s) to Add -> *Select files* -> OK

## 

## 4. Create and apply transform to align the mri and the bem surface:

Modules -> Transforms -> Active Transform: Create new Linear Transform as ... -> name it _bem2mri_

Apply transform -> select the _bem_ node

Display the MRI on the 3D View and confirm that they are aligned.

Transformed: select _bem_ and harden the transform (icon)



## 5. Segmentation

Modules: Segmentations -> Active segmentation: Create new Segmentation as ... -> name it _bem_seg_

Export/import models and labelmaps -> Select options Import and Models -> Input node: _bem_ -> Import

Modules: Segment Editor -> + Add -> Paint -> Editable area: _Inside bem_seg_

Paint every couple of slices the area to be anonymized (i.e. eyes, nose and mouth).

Set _anony_seg_ to be the only visible segmentation -> Fill between slices -> Initialize -> Apply

Modules: Segmentations -> Set _anony_seg_ to be the only visible segmentation -> Export/import models and labelmaps -> Select options Export, Labelmap and Advanced: Exported segments and Reference volume: T1: _Visible_ -> Input node: _bem_ -> Export

Save all files on a new folder changing the format of _bem_seg-label_ to _.nii



## Appendix

Get data array:

```python
a = slicer.util.array('node_name')
```

Get node:

```python
n = slicer.util.getNode('node_name')
```







