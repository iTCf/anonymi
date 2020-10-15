import os
import vtk, qt, ctk, slicer
import numpy as np
from slicer.ScriptedLoadableModule import *
# from slicer.modules import volumeclipwithmodel
import logging
import subprocess as sp
import shlex

#
# Anonymi
#

class Anonymi(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "AnonyMI"
    self.parent.categories = ["Anonymization"]
    self.parent.dependencies = []
    self.parent.contributors = ["Ezequiel Mikulan (University of Milan)", "Simone Russo (University of Milan)", "Andrea Pigorini (University of Milan)"]
    self.parent.helpText = """
    AnonyMI is an MRI anonymization tool that preserves the subject's anatomical geometry
    """

    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
    This research has received funding from the European Union's Horizon 2020 Framework Programme for Research and Innovation under the
    Specific Grant Agreements No. 720270 and No. 785907 (Human Brain Project SGA1 and SGA2)
    """

#
# AnonymiWidget
#

class AnonymiWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...

    # Status Area
    #
    statusCollapsibleButton = ctk.ctkCollapsibleButton()
    statusCollapsibleButton.text = "Status"
    self.layout.addWidget(statusCollapsibleButton)

    # Layout - Status
    statusFormLayout = qt.QFormLayout(statusCollapsibleButton)
    self.statusLabel = qt.QLabel('Not Running')
    self.statusLabel.setFixedHeight(30)
    self.statusLabel.setAlignment(qt.Qt.AlignCenter)
    self.statusLabel.setStyleSheet("background-color: lightgray")
    statusFormLayout.addRow(self.statusLabel)

    # Prepare Area
    #
    prepareCollapsibleButton = ctk.ctkCollapsibleButton()
    prepareCollapsibleButton.text = "Prepare files"
    self.layout.addWidget(prepareCollapsibleButton)

    # Layout - Prepare
    prepareFormLayout = qt.QFormLayout(prepareCollapsibleButton)

    self.prepareFilesSelector = qt.QPushButton("Select Files to Prepare")
    self.prepareFilesSelector.toolTip = "Select the files for preparation"
    self.prepareFilesSelector.enabled = True

    prepareFormLayout.addRow(self.prepareFilesSelector)

    self.prepareFilesSelector.connect('clicked(bool)', self.onPrepareFiles)

    # Single Subject
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Single Subject"
    self.layout.addWidget(parametersCollapsibleButton)
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene(slicer.mrmlScene)
    self.inputSelector.setToolTip("Pick the MRI to be Anonymized.")
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    # surf2mri transform selector
    #
    self.surf2mri = slicer.qMRMLNodeComboBox()
    self.surf2mri.nodeTypes = ["vtkMRMLLinearTransformNode"]
    self.surf2mri.selectNodeUponCreation = True
    self.surf2mri.addEnabled = False
    self.surf2mri.removeEnabled = False
    self.surf2mri.noneEnabled = False
    self.surf2mri.showHidden = False
    self.surf2mri.showChildNodeTypes = False
    self.surf2mri.setMRMLScene(slicer.mrmlScene)
    self.surf2mri.setToolTip("Pick surf2mri transform.")
    parametersFormLayout.addRow("Surface to MRI transform: ", self.surf2mri)
    # TODO: autoselect nodes by name

    # outer_skin_surface selector
    #
    self.outerSkinModel = slicer.qMRMLNodeComboBox()
    self.outerSkinModel.nodeTypes = ["vtkMRMLModelNode"]
    self.outerSkinModel.selectNodeUponCreation = True
    self.outerSkinModel.addEnabled = False
    self.outerSkinModel.removeEnabled = False
    self.outerSkinModel.noneEnabled = False
    self.outerSkinModel.showHidden = False
    self.outerSkinModel.showChildNodeTypes = False
    self.outerSkinModel.setMRMLScene(slicer.mrmlScene)
    self.outerSkinModel.setToolTip("Pick outer skin model.")
    parametersFormLayout.addRow("Outer skin model: ", self.outerSkinModel)

    # outer_skull_surface selector
    #
    self.outerSkullModel = slicer.qMRMLNodeComboBox()
    self.outerSkullModel.nodeTypes = ["vtkMRMLModelNode"]
    self.outerSkullModel.selectNodeUponCreation = True
    self.outerSkullModel.addEnabled = False
    self.outerSkullModel.removeEnabled = False
    self.outerSkullModel.noneEnabled = False
    self.outerSkullModel.showHidden = False
    self.outerSkullModel.showChildNodeTypes = False
    self.outerSkullModel.setMRMLScene(slicer.mrmlScene)
    self.outerSkullModel.setToolTip("Pick outer skull model.")
    parametersFormLayout.addRow("Outer skull model: ", self.outerSkullModel)

    # Control points
    #
    self.faceControl = slicer.qMRMLNodeComboBox()
    self.faceControl.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.faceControl.selectNodeUponCreation = True
    self.faceControl.addEnabled = False
    self.faceControl.removeEnabled = False
    self.faceControl.noneEnabled = False
    self.faceControl.showHidden = False
    self.faceControl.showChildNodeTypes = False
    self.faceControl.setMRMLScene(slicer.mrmlScene)
    self.faceControl.setToolTip("Pick list of control points for the FACE.")
    parametersFormLayout.addRow("Face control points: ", self.faceControl)

    self.earRControl = slicer.qMRMLNodeComboBox()
    self.earRControl.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.earRControl.selectNodeUponCreation = True
    self.earRControl.addEnabled = False
    self.earRControl.removeEnabled = False
    self.earRControl.noneEnabled = False
    self.earRControl.showHidden = False
    self.earRControl.showChildNodeTypes = False
    self.earRControl.setMRMLScene( slicer.mrmlScene )
    self.earRControl.setToolTip("Pick list of control points for the RIGHT EAR.")
    parametersFormLayout.addRow("Right ear control points: ", self.earRControl)

    self.earLControl = slicer.qMRMLNodeComboBox()
    self.earLControl.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.earLControl.selectNodeUponCreation = True
    self.earLControl.addEnabled = False
    self.earLControl.removeEnabled = False
    self.earLControl.noneEnabled = False
    self.earLControl.showHidden = False
    self.earLControl.showChildNodeTypes = False
    self.earLControl.setMRMLScene(slicer.mrmlScene)
    self.earLControl.setToolTip("Pick list of control points for the LEFT EAR.")
    parametersFormLayout.addRow("Left ear control points: ", self.earLControl)

    #
    # Auto control points
    #
    self.getControl = qt.QPushButton("Get control points")
    self.getControl.toolTip = "Get control points automatically."
    self.getControl.enabled = True
    parametersFormLayout.addRow(self.getControl)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.getControl.connect('clicked(bool)', self.onGetControl)
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Refresh Apply button state (enabled when all inputs are ok)
    self.onSelect()

    # Batch Area
    #
    batchCollapsibleButton = ctk.ctkCollapsibleButton()
    batchCollapsibleButton.text = "Automatic Processing"
    self.layout.addWidget(batchCollapsibleButton)

    # Layout - Batch
    batchFormLayout = qt.QFormLayout(batchCollapsibleButton)

    self.batchFilesSelector = qt.QPushButton("Select Files to Run")
    self.batchFilesSelector.toolTip = "Select the files for batch running"
    self.batchFilesSelector.enabled = True

    self.batchFiles = ''
    self.batchFolderText = qt.QLineEdit()
    self.batchFolderText.setAlignment(qt.Qt.AlignCenter)
    self.batchFolderText.setDisabled(True)
    self.batchFolderText.setText('No selected files')

    self.batchRun = qt.QPushButton("Run")
    self.batchRun.toolTip = "Run Batch Process"
    self.batchRun.enabled = True  # TODO: enable run batch when files are selected

    batchFormLayout.addRow(self.batchFilesSelector)
    batchFormLayout.addRow(self.batchFolderText)
    batchFormLayout.addRow(self.batchRun)

    self.batchFilesSelector.connect('clicked(bool)', self.onSelectBatchFiles)
    self.batchRun.connect('clicked(bool)', self.onRunBatch)


    # Template Area
    #
    templCollapsibleButton = ctk.ctkCollapsibleButton()
    templCollapsibleButton.text = "Template"
    self.layout.addWidget(templCollapsibleButton)

    # Layout - Template
    templFormLayout = qt.QFormLayout(templCollapsibleButton)

    self.custTempCheckb = qt.QCheckBox()
    self.templFilesSelector = qt.QPushButton("Select Custom Template")
    self.templFilesSelector.toolTip = "Select Custom Template"
    self.templFilesSelector.enabled = True

    self.templateFiles = ''
    self.templFolderText = qt.QLineEdit()
    self.templFolderText.setAlignment(qt.Qt.AlignCenter)
    self.templFolderText.setDisabled(True)
    self.templFolderText.setText('No Custom Template Selected')

    templFormLayout.addRow("Use Custom Template ", self.custTempCheckb)
    templFormLayout.addRow(self.templFilesSelector)
    templFormLayout.addRow(self.templFolderText)

    self.templFilesSelector.connect('clicked(bool)', self.onSelectTemplate)

    # Add vertical spacer
    self.layout.addStretch(1)

  def onPrepareFiles(self):
    logic = AnonymiLogic()
    self.statusLabel.setText("Running: Prepare Files")
    self.statusLabel.setStyleSheet("background-color: green")
    logic.prepareFiles()
    self.statusLabel.setText("Not Running")
    self.statusLabel.setStyleSheet("background-color: lightgray")


  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outerSkinModel.currentNode() and \
                               self.outerSkullModel.currentNode() and self.faceControl.currentNode() and \
                               self.earRControl.currentNode(), self.earLControl.currentNode()

  def onApplyButton(self):
    logic = AnonymiLogic()
    logic.subj = self.inputSelector.currentNode().GetName()

    self.statusLabel.setText("Running: Anonymization")
    self.statusLabel.setStyleSheet("background-color: green")

    logic.run(self.inputSelector.currentNode(), self.outerSkinModel.currentNode(),
              self.outerSkullModel.currentNode(), self.faceControl.currentNode(),
              self.earRControl.currentNode(), self.earLControl.currentNode(),
              isBatch=False)

    self.statusLabel.setText("Not Running")
    self.statusLabel.setStyleSheet("background-color: lightgray")

  def onGetControl(self):
    logic = AnonymiLogic()
    logic.align_surf_to_mri(self.surf2mri.currentNode(), self.outerSkinModel.currentNode(), self.outerSkullModel.currentNode())

    if self.custTempCheckb.isChecked():
        template = self.templFiles[0]
        print('-----> Using custom template: %s' % template)
    else:
        template = 'IXI'
        print('-----> Using IXI template')

    self.statusLabel.setText("Running: Get Control Points")
    self.statusLabel.setStyleSheet("background-color: green")

    logic.getControl(self.outerSkinModel.currentNode(),
                     self.inputSelector.currentNode(), template)

    self.statusLabel.setText("Not Running")
    self.statusLabel.setStyleSheet("background-color: lightgray")

  def onSelectBatchFiles(self):
    batchFiles = qt.QFileDialog.getOpenFileNames(None, "Choose files", "~", "Skin surfaces (*skin*.vtk)") # use vtk to avoid specyfing mri file type

    self.batchFiles = batchFiles
    self.batchFolderText.setText('Selected files: %s' % len(batchFiles))

  def onRunBatch(self):
      print('---> Running Batch')
      logic = AnonymiLogic()
      self.statusLabel.setText("Running: Batch Anonymization")
      self.statusLabel.setStyleSheet("background-color: green")

      for f in self.batchFiles:
          print('------> Input file: %s' % os.path.split(f)[1])

          logic.getFileNames(f)
          print(logic.fnames)
          # pretty logging

          logic.loadFiles()

          logic.align_surf_to_mri(logic.subj_trans_node, logic.subj_skin_node, logic.subj_skull_node)

          if self.custTempCheckb.isChecked():
              template = self.templFiles[0]
              print('-----> Using custom template: %s' % template)
          else:
              template = 'IXI'
              print('-----> Using IXI template')

          logic.getControl(logic.subj_skin_node, logic.subj_mri_node, template)
          logic.run(logic.subj_mri_node, logic.subj_skin_node,
                    logic.subj_skull_node, logic.subj_control_nodes['face'],
                    logic.subj_control_nodes['earR'], logic.subj_control_nodes['earL'],
                    isBatch=True)
          logic.cleanSubjFiles()
      self.statusLabel.setText("Not Running")
      self.statusLabel.setStyleSheet("background-color: lightgray")

  def onSelectTemplate(self):
      templFiles = qt.QFileDialog.getOpenFileNames(None, "Choose files", "~",
                                                   "Template (*.dcm *.nrrd *.img *.nii *.nii.gz *.mgz)")

      if templFiles:
          self.templFiles = templFiles
          self.templFolderText.setText('Selected file: %s' % templFiles)


#
# AnonymiLogic
#

class AnonymiLogic(ScriptedLoadableModuleLogic):
  # TODO: Snapshots
  # TODO: Better interface for batch files to run
  # TODO: Manual (pdf) & Logo
  # TODO: Pretty logging
  # TODO: fix CLI

  def getFsEnv(self):
      """Create an environment for elastix where executables are added to the path"""
      fsBinDir = '/Users/lpen/scripts/anonymi/Anonymi/Resources/bin:/usr/lib:'
      fsEnv = os.environ.copy()
      fsEnv["PATH"] = fsBinDir + os.pathsep + fsEnv["PATH"] if fsEnv.get("PATH") else fsBinDir
      fsEnv['DYLD_LIBRARY_PATH'] = '/Users/lpen/scripts/anonymi/Anonymi/Resources/lib/gcc/lib'
      fsEnv['FREESURFER_HOME'] = '/Users/lpen/scripts/anonymi/Anonymi/Resources'
      return fsEnv

  def prepareFiles(self, do_ws=True, do_conv=True, do_tfm=True):
      # todo: add parameters for choosing what to run
      prepareFiles = qt.QFileDialog.getOpenFileNames(None, "Choose files", "~", "")  # TODO: specify only mri types
      self.prepareFiles = prepareFiles
      fsEnv = self.getFsEnv()

      for f in prepareFiles:
          print('Preparing file: %s' % f)
          file_spl = os.path.split(f)
          file_dir = file_spl[0]
          file_name = file_spl[1]
          base_name = file_name.split('.')[0]
          logfile = open('%s/%s_log.txt' % (file_dir, base_name), 'w')

          # run watershed
          if do_ws:
              command = 'mri_watershed -useSRAS -surf %s/%s %s %s/bems/ws' % (file_dir, base_name, f, file_dir)
              p = sp.Popen(shlex.split(command), env=fsEnv, stdout=logfile, stderr=logfile)
              p.wait()
              print('Watershed Done: %s' % f)

          # convert surfaces to vtk
          if do_conv:
              surfs = ('outer_skull', 'outer_skin')
              for s in surfs:
                  file_s = '%s/%s_%s_surface' % (file_dir, base_name, s)
                  command = 'mris_convert %s %s' % (file_s, file_s+'.vtk')
                  p = sp.Popen(shlex.split(command), env=fsEnv, stdout=logfile, stderr=logfile)
                  p.wait()

          # create alignment file
          if do_tfm:
              command = 'mri_info %s --cras' % f
              cras = sp.check_output(shlex.split(command), env=fsEnv, stderr=logfile)
              cras = cras.strip('\n').split(' ')
              cras = [round(float(n), 2) for n in cras]
              cras[2] *= -1  # invert for ITK

              text = ('#Insight Transform File V1.0\n'
                      '#Transform 0\n'
                      'Transform: AffineTransform_double_3_3\n'
                      'Parameters: 1 0 0 0 1 0 0 0 1 %s %s %s\n'
                      'FixedParameters: 0 0 0\n\n' % (cras[0], cras[1], cras[2]))

              file_trans = '%s/%s_surf2mri.tfm' % (file_dir, base_name)
              with open(file_trans, 'w') as f_tr:
                  f_tr.write(text)
              print('Alignment Transform Done: %s' % f)
          logfile.close()

          # clean
          s_to_clean = ('brain', 'inner_skull', 'outer_skull', 'outer_skin')
          for s in s_to_clean:
              s_file = '%s/%s_%s_surface' % (file_dir, base_name, s)
              if os.path.isfile(s_file):
                os.remove(s_file)
          print('Prepare Files Done: %s' % f)

  def find_closest_point_coords(self, cloud, point):
    dist_all = np.sqrt(np.sum((cloud - point) ** 2, axis=1))
    min_dist_ix = np.argmin(dist_all)
    min_dist_coords = cloud[min_dist_ix]
    return min_dist_coords

  def align_surf_to_mri(self, surf2mri, outerSkinModel, outerSkullModel):
    outerSkinModel.SetAndObserveTransformNodeID(surf2mri.GetID())
    outerSkullModel.SetAndObserveTransformNodeID(surf2mri.GetID())

    trans_logic = slicer.vtkSlicerTransformLogic()
    trans_logic.hardenTransform(outerSkinModel)
    trans_logic.hardenTransform(outerSkullModel)


  def getControl(self, outerSkinModel, inputVolume, template='IXI'):
    import Elastix
    print('--> Getting control points')
    controls = ['face', 'earR', 'earL']

    # check if templates are loaded
    try:
        template_mri_node = slicer.util.getNode('%s_mri*' % template)
        template_control_nodes = {k: slicer.util.getNode('%s_%s_control*' % (template, k)) for k in controls}
        print('--> Using already loaded template')

    except:
        print('--> Loading template')
        base_dir = os.path.split(slicer.modules.anonymi.path)[0]
        if template == 'IXI':
            template_path = os.path.join(base_dir, 'Resources', 'templates')
            template_fname = 'IXI.nii'
            template_basename = template
        else:
            template_path, template_fname = os.path.split(template)
            template_basename = os.path.splitext(template_fname)[0]

        template_mri_fname = os.path.join(template_path, template_fname)
        template_control_fname = os.path.join(base_dir, 'Resources', 'templates', '%s_%s_control.fcsv')
        _ = [slicer.util.loadMarkupsFiducialList(template_control_fname % (template_basename, k)) for k in controls]
        template_mri_node = slicer.util.loadVolume(template_mri_fname, returnNode=True)[1]
        template_control = slicer.util.loadMarkupsFiducialList(template_control_fname)  # check load control nodes
        template_control_nodes = {k: slicer.util.getNode('%s_%s_control*' % (template_basename, k)) for k in controls}

    shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)

    subj_control_nodes = {}
    for c in controls:
        itemIDToClone = shNode.GetItemByDataNode(template_control_nodes[c])
        clonedItemID = slicer.modules.subjecthierarchy.logic().CloneSubjectHierarchyItem(shNode, itemIDToClone)
        clonedNode = shNode.GetItemDataNode(clonedItemID)
        clonedNode.SetName(c)
        subj_control_nodes[c] = clonedNode

    print('--> Running Elastix Registration')

    elastix_logic = Elastix.ElastixLogic()
    outputVolume = slicer.vtkMRMLScalarVolumeNode()
    slicer.mrmlScene.AddNode(outputVolume)
    outputVolume.CreateDefaultDisplayNodes()

    outputTransform = slicer.vtkMRMLTransformNode()
    print(type(inputVolume))
    parameterFilenames = elastix_logic.getRegistrationPresets()[0][5] # 5 = RegistrationPresets_ParameterFilenames
    elastix_logic.registerVolumes(inputVolume, template_mri_node,
                                  parameterFilenames=parameterFilenames,
                                  outputVolumeNode=outputVolume,
                                  outputTransformNode=outputTransform)
    outputVolume.Modified()
    slicer.mrmlScene.AddNode(outputTransform)

    # harden the registration on the fiducials
    _ = [subj_control_nodes[k].SetAndObserveTransformNodeID(outputTransform.GetID()) for k in controls]

    trans_logic = slicer.vtkSlicerTransformLogic()
    _ = [trans_logic.hardenTransform(subj_control_nodes[k]) for k in controls]

    # project to the skin surface
    surf_arr = slicer.util.arrayFromModelPoints(outerSkinModel)

    for k in template_control_nodes.keys():
        numFids = subj_control_nodes[k].GetNumberOfFiducials()
        for i in range(numFids):
            world = [0,0,0,1]
            subj_control_nodes[k].GetNthFiducialWorldCoordinates(i,world)
            print(world)
            proj_coords = self.find_closest_point_coords(surf_arr, world[:3])
            subj_control_nodes[k].SetNthFiducialPositionFromArray(i, proj_coords)
    print('--> Control Points Registraion Finished')

    self.subj_control_nodes = subj_control_nodes
    slicer.mrmlScene.RemoveNode(outputVolume)
    slicer.mrmlScene.RemoveNode(outputTransform)
    slicer.mrmlScene.RemoveNode(template_mri_node)
    for c in controls:
        slicer.mrmlScene.RemoveNode(template_control_nodes[c])
    # TODO: remove nodes only if not in batch mode
    # TODO: add option for custom template

  def getFileNames(self, skinFname):
    fnames = {}
    basename = skinFname.replace('_outer_skin_surface.vtk', '')
    fdir = os.path.split(skinFname)[0]
    all_files = os.listdir(fdir)
    scode = os.path.split(basename)[1]
    sfiles = [f for f in all_files if f.startswith(scode)]  # fix names that start with the same name
    sfiles = [os.path.join(fdir, f) for f in sfiles]
    fnames['skin'] = skinFname
    fnames['skull'] = basename + '_outer_skull_surface.vtk'
    fnames['trans'] = basename + '_surf2mri.tfm'
    fnames['mri'] = [f for f in sfiles if f not in fnames.values()]

    if len(fnames['mri']) != 1:
     print(fnames)
     print('Inconsistent number of files')
     return 1  # check correct return ?
    else:
        fnames['mri'] = fnames['mri'][0]
    self.subj = scode
    self.fnames = fnames

  def loadFiles(self):
      try:
          print('Loading files')
          print(self.fnames)
          self.subj_mri_node = slicer.util.loadVolume(self.fnames['mri'], returnNode=True)[1]
          self.subj_skin_node = slicer.util.loadModel(self.fnames['skin'], returnNode=True)[1]
          self.subj_skull_node = slicer.util.loadModel(self.fnames['skull'], returnNode=True)[1]
          self.subj_trans_node = slicer.util.loadTransform(self.fnames['trans'], returnNode=True)[1]

      except Exception as e:
          print('Unable to load files')  # error check ?
          print(e)

  def cleanSubjFiles(self):
      nodes_to_del = [self.subj_mri_node, self.subj_skin_node,
                      self.subj_skull_node, self.subj_trans_node,
                      self.subj_mri_anon_node, self.subj_control_nodes['face'],
                      self.subj_control_nodes['earR'],
                      self.subj_control_nodes['earL']]

      for n in nodes_to_del:
          slicer.mrmlScene.RemoveNode(n)

  def mask_dims(self, order, mask_control, min_R, max_R, min_A, max_A, min_S, max_S):
      # TODO: add all combinations
    if order == ['R', 'S', 'A']: # SLICER CHANGES THE AXIS ORDER!!!
        mask_control[min_A:max_A, min_S:max_S, min_R:max_R] = True
        # mask_control[min_R:max_R, min_S:max_S, min_A:max_A] = True
    elif order == ['R', 'A', 'S']:
        mask_control[min_S:max_S, min_A:max_A, min_R:max_R] = True
        # mask_control[min_R:max_R, min_A:max_A, min_S:max_S] = True
    return mask_control

  def run(self, inputVolume, outerSkinModel, outerSkullModel, faceControl,
          earRControl, earLControl, isBatch):

    """
    Run the actual algorithm
    """

    logging.info('Processing started')
    ## anonymization

    # Clone T1
    volumesLogic = slicer.modules.volumes.logic()
    T1_anon = volumesLogic.CloneVolume(slicer.mrmlScene, inputVolume, self.subj + '_anonymi')

    # Create mask
    vclip = slicer.modules.volumeclipwithmodel.widgetRepresentation().self().logic

    vclip.clipVolumeWithModel(inputVolume, outerSkinModel, True, 0, False, 255, T1_anon)

    logging.info('Creating mask')
    mask = volumesLogic.CloneVolume(slicer.mrmlScene, T1_anon, 'mask')

    vclip.clipVolumeWithModel(T1_anon, outerSkullModel, False, 255, True, 0, mask)

    logging.info('Applying mask')

    mask_data = slicer.util.arrayFromVolume(mask)

    min_rand, max_rand = np.percentile(mask_data[mask_data !=0 ], [40 ,80])
    logging.info(min_rand)
    logging.info(max_rand)

    mask_data = mask_data != 0

    # transform from RAS to Volume
    transformRasToVolumeRas = vtk.vtkGeneralTransform()
    slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(None, T1_anon.GetParentTransformNode(), transformRasToVolumeRas)

    # get control points
    controls = ['face', 'earR', 'earL']
    coords = {k: [] for k in controls}
    labels = {k: [] for k in controls}
    vox_coords = {k: [] for k in controls}

    for con, nod in zip(controls, [faceControl, earRControl, earLControl]):
        n_markups = nod.GetNumberOfMarkups()
        for m in np.arange(n_markups):
            point_Ras = [0, 0, 0, 1]
            nod.GetNthFiducialWorldCoordinates(m, point_Ras)
            coords[con].append(point_Ras)
            label = nod.GetNthFiducialLabel(m)
            labels[con].append(label)

            # If volume node is transformed, apply that transform to get volume's RAS coordinates
            point_VolumeRas = transformRasToVolumeRas.TransformPoint(point_Ras[0:3])
            volumeRasToIjk = vtk.vtkMatrix4x4()
            T1_anon.GetRASToIJKMatrix(volumeRasToIjk)

            point_Ijk = [0, 0, 0, 1]
            volumeRasToIjk.MultiplyPoint(np.append(point_VolumeRas,1.0), point_Ijk)
            point_Ijk = [ int(round(c)) for c in point_Ijk[0:3] ]
            vox_coords[con].append(point_Ijk)

    # create mask
    shape = mask_data.shape
    logging.info('Data shape: %s %s %s' % shape)

    # find volume orientation
    volumeIjkToRas = vtk.vtkMatrix4x4()
    T1_anon.GetIJKToRASMatrix(volumeIjkToRas)
    logging.info(volumeIjkToRas)
    ijk_to_ras = [volumeIjkToRas.GetElement(x,y) for x in range(3) for y in range(3)]
    ijk_to_ras = np.array(ijk_to_ras).reshape(3,3)
    ijk_to_ras_round = np.rint(ijk_to_ras)

    logging.info(ijk_to_ras)
    logging.info(ijk_to_ras_round)

    directions = {k: np.argmax(np.abs(ijk_to_ras_round[i,:])) for i, k in enumerate(['R', 'A', 'S'])}
    signs = {k: ijk_to_ras_round[i, directions[k]] for i, k in enumerate(['R', 'A', 'S'])}
    order = [k for i in range(3) for k in directions.keys() if directions[k] == i]
    logging.info(directions)
    logging.info(signs)
    logging.info(order)

    mask_control = np.zeros(shape, dtype=bool)

    for con in controls:
        i = vox_coords[con][labels[con].index('I')][directions['S']]
        s = vox_coords[con][labels[con].index('S')][directions['S']]

        min_S = np.min((i,s)) # get span of the mask in the inferior-superior axis
        max_S = np.max((i,s))

        logging.info('min s %s' % min_S)
        logging.info('max s %s' % max_S)

        if con == 'face':
            r = vox_coords[con][labels[con].index('R')][directions['R']]
            l = vox_coords[con][labels[con].index('L')][directions['R']]

            min_R = np.min((r,l)) # get span of the mask in the left-right axis
            max_R = np.max((r,l))

            logging.info('min r %s' % min_R)
            logging.info('max r %s' % max_R)

            if signs['A'] > 0:
                min_A = min(vox_coords[con][labels[con].index('R')][directions['A']], vox_coords[con][labels[con].index('L')][directions['A']])
                max_A = shape[directions['A']] # determine from which end and to which point to span in the antero-posterior axis
            else:
                max_A = max(vox_coords[con][labels[con].index('R')][directions['A']], vox_coords[con][labels[con].index('L')][directions['A']])
                min_A = 0

            logging.info('min a %s' % min_A)
            logging.info('max a %s' % max_A)

        else:
            a = vox_coords[con][labels[con].index('A')][directions['A']]
            p = vox_coords[con][labels[con].index('P')][directions['A']]

            min_A = np.min((a, p))
            max_A = np.max((a, p))

            logging.info('min a %s' % min_A)
            logging.info('max a %s' % max_A)

            if ((con == 'earR') & (signs['R'] > 0)) or ((con == 'earL') & (signs['R'] < 0)):
                min_R = min(vox_coords[con][labels[con].index('A')][directions['R']], vox_coords[con][labels[con].index('P')][directions['R']])
                max_R = shape[directions['R']]
            else:
                max_R = max(vox_coords[con][labels[con].index('A')][directions['R']], vox_coords[con][labels[con].index('P')][directions['R']])
                min_R = 0
            logging.info('min r %s' % min_R)
            logging.info('max r %s' % max_R)

        mask_control = self.mask_dims(order, mask_control, min_R, max_R, min_A, max_A, min_S, max_S)

    mask_all = np.logical_and(mask_data, mask_control)
    rand_dat = np.random.randint(min_rand, max_rand, mask_all.sum())

    T1_anon_data = slicer.util.arrayFromVolume(T1_anon)
    T1_anon_data[mask_all] = rand_dat

    T1_anon.Modified()

    if isBatch:
        slicer.util.saveNode(T1_anon, self.fnames['mri'].replace(self.subj, self.subj + '_anonymi'))
    slicer.mrmlScene.RemoveNode(mask)
    self.subj_mri_anon_node = T1_anon
    slicer.util.setSliceViewerLayers(background=T1_anon)
    logging.info('Processing completed')
    return True


class AnonymiTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_Anonymi1()

  def test_Anonymi1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        logging.info('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        logging.info('Loading %s...' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = AnonymiLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
