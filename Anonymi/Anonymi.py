import os
import unittest
import vtk, qt, ctk, slicer
import numpy as np
from slicer.ScriptedLoadableModule import *
# from slicer.modules import volumeclipwithmodel
import logging


#
# Anonymi
#

class Anonymi(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Anonymi" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Anonymization"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

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

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)

    #
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
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the MRI to be Anonymid." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

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
    self.outerSkinModel.setMRMLScene( slicer.mrmlScene )
    self.outerSkinModel.setToolTip( "Pick outer skin model." )
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
    self.outerSkullModel.setMRMLScene( slicer.mrmlScene )
    self.outerSkullModel.setToolTip( "Pick outer skull model." )
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
    self.faceControl.setMRMLScene( slicer.mrmlScene )
    self.faceControl.setToolTip( "Pick list of control points for the FACE." )
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
    self.earRControl.setToolTip( "Pick list of control points for the RIGHT EAR." )
    parametersFormLayout.addRow("Right ear control points: ", self.earRControl)

    self.earLControl = slicer.qMRMLNodeComboBox()
    self.earLControl.nodeTypes = ["vtkMRMLMarkupsFiducialNode"]
    self.earLControl.selectNodeUponCreation = True
    self.earLControl.addEnabled = False
    self.earLControl.removeEnabled = False
    self.earLControl.noneEnabled = False
    self.earLControl.showHidden = False
    self.earLControl.showChildNodeTypes = False
    self.earLControl.setMRMLScene( slicer.mrmlScene )
    self.earLControl.setToolTip( "Pick list of control points for the LEFT EAR." )
    parametersFormLayout.addRow("Left ear control points: ", self.earLControl)


    #
    # output volume selector
    #
    # self.outputSelector = slicer.qMRMLNodeComboBox()
    # self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    # self.outputSelector.selectNodeUponCreation = True
    # self.outputSelector.addEnabled = True
    # self.outputSelector.removeEnabled = True
    # self.outputSelector.noneEnabled = True
    # self.outputSelector.showHidden = False
    # self.outputSelector.showChildNodeTypes = False
    # self.outputSelector.setMRMLScene( slicer.mrmlScene )
    # self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    # parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # threshold value
    #
    self.rangeRandom = ctk.ctkRangeWidget()
    self.rangeRandom.maximum = 200.
    self.rangeRandom.minimum = 0.
    self.rangeRandom.setValues(50., 100.)
    self.rangeRandom.setToolTip("Range for random values generation")
    parametersFormLayout.addRow("Range for random values", self.rangeRandom)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    # self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Refresh Apply button state
    self.onSelect()

  def cleanup(self):
    pass

  def onSelect(self):
    # self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outerSkinModel.currentNode() and self.outerSkullModel.currentNode()

  def onApplyButton(self):
    logic = AnonymiLogic()
    min_rand = self.rangeRandom.minimum
    max_rand = self.rangeRandom.maximum
    logic.run(self.inputSelector.currentNode(), self.outerSkinModel.currentNode(),
              self.outerSkullModel.currentNode(), self.faceControl.currentNode(),
               self.earRControl.currentNode(), self.earLControl.currentNode(),
               min_rand, max_rand)
#
# AnonymiLogic
#

class AnonymiLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True

  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    slicer.util.delayDisplay('Take screenshot: '+description+'.\nResult is available in the Annotations module.', 3000)

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qimage = ctk.ctkWidgetsUtils.grabWidget(widget)
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, 1, imageData)

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
          earRControl, earLControl, min_rand, max_rand):
    """
    Run the actual algorithm
    """

    logging.info('Processing started')
    ## anonymization

    # Clone T1
    volumesLogic = slicer.modules.volumes.logic()
    T1_anon = volumesLogic.CloneVolume(slicer.mrmlScene, inputVolume, 'T1_anon')
    # mask1 = volumesLogic.CloneVolume(slicer.mrmlScene, T1_anon, 'mask1')

    # Create mask
    vclip = slicer.modules.volumeclipwithmodel.widgetRepresentation().self().logic

    vclip.clipVolumeWithModel(inputVolume, outerSkinModel, True, 0, T1_anon)
    # vclip.clipVolumeWithModel(inputVolume, outerSkinModel, True, 0, mask1)

    logging.info('Creating mask')
    mask = volumesLogic.CloneVolume(slicer.mrmlScene, T1_anon, 'mask')
    # mask = volumesLogic.CloneVolume(slicer.mrmlScene, mask1, 'mask')

    vclip.clipVolumeWithModel(T1_anon, outerSkullModel, False, 0, mask)
    # vclip.clipVolumeWithModel(mask1, outerSkullModel, False, 0, mask)

    logging.info('Applying mask')

    mask_data = slicer.util.arrayFromVolume(mask)
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


    # mask_control = np.zeros((256, 256, 256), dtype=bool)
    mask_control = np.zeros(shape, dtype=bool)

    for con in controls:
        i = vox_coords[con][labels[con].index('I')][directions['S']]
        s = vox_coords[con][labels[con].index('S')][directions['S']]


        min_S = np.min((i,s)) # get span of the mask in the inferio-superior axis
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
                max_A = shape[directions['A']] # determine from which end and to which point to span in the antero-posterior axiss
            else:
                max_A = max(vox_coords[con][labels[con].index('R')][directions['A']], vox_coords[con][labels[con].index('L')][directions['A']])
                min_A = 0

            logging.info('min a %s' % min_A)
            logging.info('max a %s' % max_A)
            # mask_control = self.mask_dims(order, mask_control, min_R, max_R, min_A, max_A, min_S, max_S)

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
    # TODO: range of random values
    # rand_dat = np.random.randint(50, 100, mask_all.sum())
    rand_dat = np.random.randint(500, 1000, mask_all.sum())

    T1_anon_data = slicer.util.arrayFromVolume(T1_anon)
    T1_anon_data[mask_all] = rand_dat

    T1_anon.Modified()

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
