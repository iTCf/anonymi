# USE SLICER TO RUN
# ~/soft/Slicer-4.10.2-linux-amd64/Slicer --python-script run_anonymi.py

import sys
import Anonymi

skin_fname = sys.argv[1]

print(fname)

logic = Anonymi.AnonymiLogic()
logic.getFileNames(skin_fname) # get filesnames of required files
logic.loadFiles()

logic.subj_skin_node.SetAndObserveTransformNodeID(logic.subj_trans_node.GetID())
logic.subj_skull_node.SetAndObserveTransformNodeID(logic.subj_trans_node.GetID())

trans_logic = slicer.vtkSlicerTransformLogic()
trans_logic.hardenTransform(logic.subj_skin_node)
trans_logic.hardenTransform(logic.subj_skull_node)

logic.getControl(logic.subj_skin_node, logic.subj_mri_node)
logic.run(logic.subj_mri_node, logic.subj_skin_node,
          logic.subj_skull_node, logic.subj_control_nodes['face'],
           logic.subj_control_nodes['earR'], logic.subj_control_nodes['earL'])
logic.cleanSubjFiles()
