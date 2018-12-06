# state file generated using paraview version 5.6.0
final_fig = True
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
renderView1.CenterOfRotation = [5.0, 5.0, 0.0]
renderView1.StereoType = 0
renderView1.CameraPosition = [-18.95271387213014, -40.04468361336347, 18.945241689214654]
renderView1.CameraFocalPoint = [5.0, 5.0, 0.0]
renderView1.CameraViewUp = [0.140556509581304, 0.3194062688247228, 0.9371357975500616]
renderView1.CameraParallelScale = 14.36886933553501
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
a01_box_3d_mesh_oute = ExodusIIReader(FileName=['/Users/danielb/projects/moose/modules/porous_flow/examples/tutorial/01_box_3d_mesh_out.e'])
a01_box_3d_mesh_oute.ElementVariables = ['darcy_vel_']
a01_box_3d_mesh_oute.PointVariables = ['porepressure']
a01_box_3d_mesh_oute.NodeSetArrayStatus = []
a01_box_3d_mesh_oute.SideSetArrayStatus = []
a01_box_3d_mesh_oute.ElementBlocks = ['Unnamed block ID: 0 Type: HEX8']

# ----------------------------------------------------------------
# setup the visualization in view 'renderView1'
# ----------------------------------------------------------------

# show data from a01_box_3d_mesh_oute
a01_box_3d_mesh_outeDisplay = Show(a01_box_3d_mesh_oute, renderView1)

# get color transfer function/color map for 'porepressure'
porepressureLUT = GetColorTransferFunction('porepressure')
porepressureLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 500000.0, 0.865003, 0.865003, 0.865003, 1000000.0, 0.705882, 0.0156863, 0.14902]
porepressureLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'porepressure'
porepressurePWF = GetOpacityTransferFunction('porepressure')
porepressurePWF.Points = [0.0, 0.0, 0.5, 0.0, 1000000.0, 1.0, 0.5, 0.0]
porepressurePWF.ScalarRangeInitialized = 1

# trace defaults for the display properties.
a01_box_3d_mesh_outeDisplay.Representation = 'Surface'
a01_box_3d_mesh_outeDisplay.ColorArrayName = ['POINTS', 'porepressure']
a01_box_3d_mesh_outeDisplay.LookupTable = porepressureLUT
a01_box_3d_mesh_outeDisplay.OSPRayScaleArray = 'GlobalNodeId'
a01_box_3d_mesh_outeDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
a01_box_3d_mesh_outeDisplay.SelectOrientationVectors = 'GlobalNodeId'
a01_box_3d_mesh_outeDisplay.ScaleFactor = 1.2000000000000002
a01_box_3d_mesh_outeDisplay.SelectScaleArray = 'GlobalNodeId'
a01_box_3d_mesh_outeDisplay.GlyphType = 'Arrow'
a01_box_3d_mesh_outeDisplay.GlyphTableIndexArray = 'GlobalNodeId'
a01_box_3d_mesh_outeDisplay.GaussianRadius = 0.06
a01_box_3d_mesh_outeDisplay.SetScaleArray = ['POINTS', 'GlobalNodeId']
a01_box_3d_mesh_outeDisplay.ScaleTransferFunction = 'PiecewiseFunction'
a01_box_3d_mesh_outeDisplay.OpacityArray = ['POINTS', 'GlobalNodeId']
a01_box_3d_mesh_outeDisplay.OpacityTransferFunction = 'PiecewiseFunction'
a01_box_3d_mesh_outeDisplay.DataAxesGrid = 'GridAxesRepresentation'
a01_box_3d_mesh_outeDisplay.SelectionCellLabelFontFile = ''
a01_box_3d_mesh_outeDisplay.SelectionPointLabelFontFile = ''
a01_box_3d_mesh_outeDisplay.PolarAxes = 'PolarAxesRepresentation'
a01_box_3d_mesh_outeDisplay.ScalarOpacityFunction = porepressurePWF
a01_box_3d_mesh_outeDisplay.ScalarOpacityUnitDistance = 1.7453618244717872

# init the 'GridAxesRepresentation' selected for 'DataAxesGrid'
a01_box_3d_mesh_outeDisplay.DataAxesGrid.XTitleFontFile = ''
a01_box_3d_mesh_outeDisplay.DataAxesGrid.YTitleFontFile = ''
a01_box_3d_mesh_outeDisplay.DataAxesGrid.ZTitleFontFile = ''
a01_box_3d_mesh_outeDisplay.DataAxesGrid.XLabelFontFile = ''
a01_box_3d_mesh_outeDisplay.DataAxesGrid.YLabelFontFile = ''
a01_box_3d_mesh_outeDisplay.DataAxesGrid.ZLabelFontFile = ''

# init the 'PolarAxesRepresentation' selected for 'PolarAxes'
a01_box_3d_mesh_outeDisplay.PolarAxes.PolarAxisTitleFontFile = ''
a01_box_3d_mesh_outeDisplay.PolarAxes.PolarAxisLabelFontFile = ''
a01_box_3d_mesh_outeDisplay.PolarAxes.LastRadialAxisTextFontFile = ''
a01_box_3d_mesh_outeDisplay.PolarAxes.SecondaryRadialAxesTextFontFile = ''

# setup the color legend parameters for each legend in this view

# get color transfer function/color map for 'vtkBlockColors'
vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')
vtkBlockColorsLUT.InterpretValuesAsCategories = 1
vtkBlockColorsLUT.AnnotationsInitialized = 1
vtkBlockColorsLUT.Annotations = ['0', '0', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6', '7', '7', '8', '8', '9', '9', '10', '10', '11', '11']
vtkBlockColorsLUT.ActiveAnnotatedValues = ['0']
vtkBlockColorsLUT.IndexedColors = [1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.6299992370489051, 0.6299992370489051, 1.0, 0.6699931334401464, 0.5000076295109483, 0.3300068665598535, 1.0, 0.5000076295109483, 0.7499961852445258, 0.5300068665598535, 0.3499961852445258, 0.7000076295109483, 1.0, 0.7499961852445258, 0.5000076295109483]
vtkBlockColorsLUT.IndexedOpacities = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

# get color legend/bar for vtkBlockColorsLUT in view renderView1
vtkBlockColorsLUTColorBar = GetScalarBar(vtkBlockColorsLUT, renderView1)
vtkBlockColorsLUTColorBar.Title = 'vtkBlockColors'
vtkBlockColorsLUTColorBar.ComponentTitle = ''
vtkBlockColorsLUTColorBar.TitleFontFile = ''
vtkBlockColorsLUTColorBar.LabelFontFile = ''

# set color bar visibility
vtkBlockColorsLUTColorBar.Visibility = 0

# get color legend/bar for porepressureLUT in view renderView1
porepressureLUTColorBar = GetScalarBar(porepressureLUT, renderView1)
porepressureLUTColorBar.Title = 'porepressure'
porepressureLUTColorBar.ComponentTitle = ''
porepressureLUTColorBar.TitleFontFile = ''
porepressureLUTColorBar.LabelFontFile = ''

# set color bar visibility
porepressureLUTColorBar.Visibility = 1

# get color transfer function/color map for 'darcy_vel_'
darcy_vel_LUT = GetColorTransferFunction('darcy_vel_')
darcy_vel_LUT.RGBPoints = [2.4439190576113716e-09, 0.231373, 0.298039, 0.752941, 1.4744975162436396e-07, 0.865003, 0.865003, 0.865003, 2.9245558419111655e-07, 0.705882, 0.0156863, 0.14902]
darcy_vel_LUT.ScalarRangeInitialized = 1.0

# get color legend/bar for darcy_vel_LUT in view renderView1
darcy_vel_LUTColorBar = GetScalarBar(darcy_vel_LUT, renderView1)
darcy_vel_LUTColorBar.Title = 'darcy_vel_'
darcy_vel_LUTColorBar.ComponentTitle = 'Magnitude'
darcy_vel_LUTColorBar.TitleFontFile = ''
darcy_vel_LUTColorBar.LabelFontFile = ''

# set color bar visibility
darcy_vel_LUTColorBar.Visibility = 0

# show color legend
a01_box_3d_mesh_outeDisplay.SetScalarBarVisibility(renderView1, True)

# ----------------------------------------------------------------
# setup color maps and opacity mapes used in the visualization
# note: the Get..() functions create a new object, if needed
# ----------------------------------------------------------------

# get opacity transfer function/opacity map for 'darcy_vel_'
darcy_vel_PWF = GetOpacityTransferFunction('darcy_vel_')
darcy_vel_PWF.Points = [2.4439190576113716e-09, 0.0, 0.5, 0.0, 2.9245558419111655e-07, 1.0, 0.5, 0.0]
darcy_vel_PWF.ScalarRangeInitialized = 1

# get opacity transfer function/opacity map for 'vtkBlockColors'
vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

# Check the current view time
view = GetActiveView()
view.ViewTime
reader = GetActiveSource()
reader.TimestepValues
tsteps = reader.TimestepValues
# Lets be fancy and use a time annotation filter. This will show the
# current time value of the reader as text in the corner of the view.
annTime = AnnotateTimeFilter(reader)
# Show the filter
Show(annTime)

#### Look at a few time steps. Note that the time value is requested not
if final_fig:
    view.ViewTime = tsteps[-1]
    Render()
    WriteImage('smooth_3d_final.png')
else:
    ### OR create an image of every time value
    ntimesteps = len(tsteps)
    for i in xrange(0,ntimesteps):
        view.ViewTime = tsteps[i]
        Render()
        pngname = 'smooth_3d_'+str(i).zfill(4)+'.png'
        WriteImage(pngname)

# ----------------------------------------------------------------
# finally, restore active source
SetActiveSource(a01_box_3d_mesh_oute)
# ----------------------------------------------------------------
