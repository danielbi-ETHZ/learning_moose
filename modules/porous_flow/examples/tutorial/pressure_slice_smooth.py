# state file generated using paraview version 5.6.0

# ----------------------------------------------------------------
# setup views used in the visualization
# ----------------------------------------------------------------

# trace generated using paraview version 5.6.0
#
# To ensure correct image size when batch processing, please search 
# for and uncomment the line `# renderView*.ViewSize = [*,*]`

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get the material library
materialLibrary1 = GetMaterialLibrary()

# Create a new 'Render View'
renderView1 = CreateView('RenderView')
renderView1.ViewSize = [708, 1097]
renderView1.AxesGrid = 'GridAxes3DActor'
renderView1.CenterOfRotation = [5.0, 5.0, -3.0]
renderView1.StereoType = 0
renderView1.CameraPosition = [5.0, -40.076035784191674, -3.0]
renderView1.CameraFocalPoint = [5.0, 5.0, -3.0]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 11.901436278830314
renderView1.Background = [0.32, 0.34, 0.43]
renderView1.OSPRayMaterialLibrary = materialLibrary1

# init the 'GridAxes3DActor' selected for 'AxesGrid'
renderView1.AxesGrid.XTitleFontFile = ''
renderView1.AxesGrid.YTitleFontFile = ''
renderView1.AxesGrid.ZTitleFontFile = ''
renderView1.AxesGrid.XLabelFontFile = ''
renderView1.AxesGrid.YLabelFontFile = ''
renderView1.AxesGrid.ZLabelFontFile = ''

# ----------------------------------------------------------------
# restore active view
SetActiveView(renderView1)
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'ExodusIIReader'
a01_box_oute = ExodusIIReader(FileName=['/Users/danielb/projects/moose/modules/porous_flow/examples/tutorial/01_box_out.e'])
a01_box_oute.ElementVariables = ['darcy_vel_']
a01_box_oute.PointVariables = ['porepressure']
a01_box_oute.NodeSetArrayStatus = []
a01_box_oute.SideSetArrayStatus = []
a01_box_oute.ElementBlocks = ['caps', 'aquifer']

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from a01_box_oute
a01_box_outeDisplay = Show(a01_box_oute, renderView1)

# get color transfer function/color map for 'porepressure'
porepressureLUT = GetColorTransferFunction('porepressure')
porepressureLUT.RGBPoints = [-28425.919019840854, 0.231373, 0.298039, 0.752941, 485787.0404900796, 0.865003, 0.865003, 0.865003, 1000000.0, 0.705882, 0.0156863, 0.14902]
porepressureLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'porepressure'
porepressurePWF = GetOpacityTransferFunction('porepressure')
porepressurePWF.Points = [-28425.919019840854, 0.0, 0.5, 0.0, 1000000.0, 1.0, 0.5, 0.0]
porepressurePWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
a01_box_outeDisplay.Representation = 'Surface With Edges'
a01_box_outeDisplay.ColorArrayName = ['POINTS', 'porepressure']
a01_box_outeDisplay.LookupTable = porepressureLUT
a01_box_outeDisplay.OSPRayScaleArray = 'GlobalNodeId'
a01_box_outeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
a01_box_outeDisplay.SelectOrientationVectors = 'GlobalNodeId'
a01_box_outeDisplay.SelectScaleArray = 'GlobalNodeId'
a01_box_outeDisplay.GlyphType = 'Arrow'
a01_box_outeDisplay.GlyphTableIndexArray = 'GlobalNodeId'
a01_box_outeDisplay.GaussianRadius = 0.05
a01_box_outeDisplay.SetScaleArray = ['POINTS', 'GlobalNodeId']
a01_box_outeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
a01_box_outeDisplay.OpacityArray = ['POINTS', 'GlobalNodeId']
a01_box_outeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
a01_box_outeDisplay.DataAxesGrid = 'GridAxesRepresentation'
a01_box_outeDisplay.SelectionCellLabelFontFile = ''
a01_box_outeDisplay.SelectionPointLabelFontFile = ''
a01_box_outeDisplay.PolarAxes = 'PolarAxesRepresentation'
a01_box_outeDisplay.ScalarOpacityFunction = porepressurePWF
a01_box_outeDisplay.ScalarOpacityUnitDistance = 1.4456469783661345

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
a01_box_outeDisplay.DataAxesGrid.XTitleFontFile = ''
a01_box_outeDisplay.DataAxesGrid.YTitleFontFile = ''
a01_box_outeDisplay.DataAxesGrid.ZTitleFontFile = ''
a01_box_outeDisplay.DataAxesGrid.XLabelFontFile = ''
a01_box_outeDisplay.DataAxesGrid.YLabelFontFile = ''
a01_box_outeDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
a01_box_outeDisplay.PolarAxes.PolarAxisTitleFontFile = ''
a01_box_outeDisplay.PolarAxes.PolarAxisLabelFontFile = ''
a01_box_outeDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
a01_box_outeDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# setup the color legend parameters for each legend in this view

# get color legend/bar for porepressureLUT in view renderView1
porepressureLUTColorBar = GetScalarBar(porepressureLUT, renderView1)
porepressureLUTColorBar.Title = 'porepressure'
porepressureLUTColorBar.ComponentTitle = ''
porepressureLUTColorBar.TitleFontFile = ''
porepressureLUTColorBar.LabelFontFile = ''

# set color bar visibility
porepressureLUTColorBar.Visibility = 1

# show color legend
a01_box_outeDisplay.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(a01_box_oute)
# ----------------------------------------------------------------
WriteImage('pressure_slice_smooth.png')
