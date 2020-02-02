# import Anonymi
#
# # ERROR
# # Could not find matching overload for given arguments:
# # ('VolumeFile', {'fileName': '/home/eze/data/anonyval/cc359/test/CC0070_philips_3_80_F.nii.gz'}, (vtkCommonCorePython.vtkCollection)0x7fd892783a78)
# #  The following slots are available:
# # loadNodes(qSlicerIO::IOFileType fileType, qSlicerIO::IOProperties parameters, vtkCollection loadedNodes) -> bool
# # loadNodes(qSlicerIO::IOFileType fileType, qSlicerIO::IOProperties parameters) -> bool
# # loadNodes(qSlicerIO::IOFileType fileType, QVariantMap parameters, vtkCollection loadedNodes) -> bool
# # loadNodes(qSlicerIO::IOFileType fileType, QVariantMap parameters) -> bool
#
#
#
# fname = '/home/eze/data/anonyval/cc359/test/CC0070_philips_3_80_F_outer_skin_surface.vtk'
# logic = Anonymi.AnonymiLogic()
#
# logic.getFileNames(fname)
# logic.loadFiles()
#
# print('aa')
# print(logic.fnames)
#
# logic.subj_skin_node.SetAndObserveTransformNodeID(logic.subj_trans_node.GetID())
# logic.subj_skull_node.SetAndObserveTransformNodeID(logic.subj_trans_node.GetID())
#
# trans_logic = slicer.vtkSlicerTransformLogic()
# trans_logic.hardenTransform(logic.subj_skin_node)
# trans_logic.hardenTransform(logic.subj_skull_node)
#
# logic.getControl(logic.subj_skin_node, logic.subj_mri_node)
# logic.run(logic.subj_mri_node, logic.subj_skin_node,
#           logic.subj_skull_node, logic.subj_control_nodes['face'],
#            logic.subj_control_nodes['earR'], logic.subj_control_nodes['earL'])
#
# logic.cleanSubjFiles()
# exit()
