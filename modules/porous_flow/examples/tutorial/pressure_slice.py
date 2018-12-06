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
renderView1.CenterOfRotation = [5.0000001192092896, 5.0, -2.9999998211860657]
renderView1.StereoType = 0
renderView1.CameraPosition = [5.0000001192092896, -49.11103945388406, -2.9999998211860657]
renderView1.CameraFocalPoint = [5.0000001192092896, 5.0, -2.9999998211860657]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 14.286950412518905
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

# create a new 'Slice'
slice1 = Slice(Input=a01_box_oute)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [5.0, 5.0, -3.0]
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from slice1
slice1Display = Show(slice1, renderView1)

# get color transfer function/color map for 'porepressure'
porepressureLUT = GetColorTransferFunction('porepressure')
porepressureLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 5.878906683738906e-39, 0.865003, 0.865003, 0.865003, 1.1757813367477812e-38, 0.705882, 0.0156863, 0.14902]
porepressureLUT.ScalarRangeInitialized = 1.0

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'porepressure']
slice1Display.LookupTable = porepressureLUT
slice1Display.OSPRayScaleArray = 'porepressure'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'None'
slice1Display.SelectScaleArray = 'None'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'None'
slice1Display.GaussianRadius = 0.05
slice1Display.SetScaleArray = ['POINTS', 'porepressure']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'porepressure']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.SelectionCellLabelFontFile = ''
slice1Display.SelectionPointLabelFontFile = ''
slice1Display.PolarAxes = 'PolarAxesRepresentation'

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
slice1Display.DataAxesGrid.XTitleFontFile = ''
slice1Display.DataAxesGrid.YTitleFontFile = ''
slice1Display.DataAxesGrid.ZTitleFontFile = ''
slice1Display.DataAxesGrid.XLabelFontFile = ''
slice1Display.DataAxesGrid.YLabelFontFile = ''
slice1Display.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
slice1Display.PolarAxes.PolarAxisTitleFontFile = ''
slice1Display.PolarAxes.PolarAxisLabelFontFile = ''
slice1Display.PolarAxes.LastRadialAxisTextFontFile = ''
slice1Display.PolarAxes.SecondaryRadialAxesTextFontFile = ''

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
slice1Display.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'porepressure'
porepressurePWF = GetOpacityTransferFunction('porepressure')
porepressurePWF.Points = [0.0, 0.0, 0.5, 0.0, 1.1757813367477812e-38, 1.0, 0.5, 0.0]
porepressurePWF.ScalarRangeInitialized = 1

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(slice1)
# ----------------------------------------------------------------
WriteImage('pressure_slice.png')

