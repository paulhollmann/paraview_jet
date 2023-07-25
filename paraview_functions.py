#!/usr/bin/env pvpython
# trace generated using paraview version 5.10.1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *


def load_VisItNek5000(file: str, elements):
    print('pv.load_VisItNek5000')
    source = VisItNek5000Reader(registrationName='nek5000', FileName=file)
    source.Meshes = ['mesh']
    source.PointArrays = elements
    UpdatePipeline(proxy=source)
    return source


def load_CGNS_5_10(file: str, elements, bases):
    print('pv.load_CGNS_5_10')
    source = CGNSSeriesReader(registrationName='cgns', FileNames=[file])
    source.Bases = bases
    source.PointArrayStatus = elements
    source.DoublePrecisionMesh = 0
    UpdatePipeline(proxy=source)
    return source

def create_Clip(source):
    print('pv.create_Clip')
    clip = Clip(registrationName='clip', Input=source)
    clip.ClipType = 'Plane'
    clip.HyperTreeGridClipper = 'Plane'
    clip.Scalars = ['POINTS', 'velocity_mag']
    clip.Value = 0.8015328049659729
    clip.ClipType.Origin = [0.0, 0.0, 37.5]
    clip.HyperTreeGridClipper.Origin = [0.0, 0.0, 37.5]
    UpdatePipeline(proxy=clip)
    return clip

def create_QCriterion(source):
    print('pv.create_QCriterion')
    qcriterion =  Gradient(registrationName='qcrit', Input=source)
    qcriterion.ScalarArray = ['POINTS', 'velocity']
    qcriterion.ComputeGradient = 0
    qcriterion.ComputeQCriterion = 1
    UpdatePipeline(proxy=qcriterion)
    return qcriterion

def create_Contour(source):
    print('pv.create_Contour')
    contour = Contour(registrationName='contour', Input=source)
    contour.ContourBy = ['POINTS', 'Q Criterion']
    contour.Isosurfaces = [0.001]
    contour.PointMergeMethod = 'Uniform Binning'
    UpdatePipeline(proxy=contour)
    return contour

def create_FastUniformGrid(factor):
    print('pv.create_FastUniformGrid')
    fastUniformGrid = FastUniformGrid(registrationName='fastUniformGrid')
    fastUniformGrid.WholeExtent = [int(-250*factor), 0, int(-250*factor), int(250*factor), 0, int(750*factor)]
    return fastUniformGrid

def create_Transformation(source,factor):
    print('pv.create_Transformation')
    transform = Transform(registrationName='transform', Input=source)
    transform.Transform = 'Transform'
    transform.Transform.Scale = [0.1/factor, 0.1/factor, 0.1/factor]
    UpdatePipeline(proxy=transform)
    return transform

def create_Resample(source, destination):
    print('pv.create_Resample')
    resample = ResampleWithDataset(registrationName='resample', SourceDataArrays=source, DestinationMesh=destination)
    resample.CellLocator = 'Static Cell Locator'
    UpdatePipeline(proxy=resample)
    return resample

def save_SourceCGNS(source, file: str):
    print('pv.save_SourceCGNS')
    SetActiveSource(source)
    SaveData(file, proxy=source)

def create_View():
    renderView = GetActiveViewOrCreate('RenderView')
    return renderView

def init_Display(visualcgns, renderView):
    display = Show(visualcgns, renderView, 'UnstructuredGridRepresentation')
    display.Representation = 'Surface'
    display.ColorArrayName = [None, '']
    display.SelectTCoordArray = 'None'
    display.SelectNormalArray = 'None'
    display.SelectTangentArray = 'None'
    display.OSPRayScaleArray = 'velocity_mag'
    display.OSPRayScaleFunction = 'PiecewiseFunction'
    display.SelectOrientationVectors = 'None'
    display.ScaleFactor = 7.5
    display.SelectScaleArray = 'None'
    display.GlyphType = 'Arrow'
    display.GlyphTableIndexArray = 'None'
    display.GaussianRadius = 0.375
    display.SetScaleArray = ['POINTS', 'velocity_mag']
    display.ScaleTransferFunction = 'PiecewiseFunction'
    display.OpacityArray = ['POINTS', 'velocity_mag']
    display.OpacityTransferFunction = 'PiecewiseFunction'
    display.DataAxesGrid = 'GridAxesRepresentation'
    display.PolarAxes = 'PolarAxesRepresentation'
    display.ScalarOpacityUnitDistance = 0.5568154306931443
    display.OpacityArrayName = ['POINTS', 'velocity_mag']
    display.OSPRayScaleFunction.Points = [0.0025922988186968653, 0.0, 0.5, 0.0, 1.5263435463360224, 1.0, 0.5, 0.0]
    display.ScaleTransferFunction.Points = [0.0019556693732738495, 0.0, 0.5, 0.0, 1.4659227132797241, 1.0, 0.5, 0.0]
    display.OpacityTransferFunction.Points = [0.0019556693732738495, 0.0, 0.5, 0.0, 1.4659227132797241, 1.0, 0.5, 0.0]

    display.Position = [0.0, 0.0, 100.0]

    display.Interpolation = 'Gouraud'
    display.Diffuse = 1.0
    display.SpecularPower = 100.0
    display.Specular = 0.3
    display.Luminosity = 100.0
    display.Ambient = 0.2
    return display
def color_Display(display):
    ColorBy(display, ('POINTS', 'velocity_mag'))
    #display.RescaleTransferFunctionToDataRange(True, False)
    velocity_magLUT = GetColorTransferFunction('velocity_mag')
    velocity_magLUT.ApplyPreset('mod', True)
    velocity_magLUT.RescaleTransferFunction(0.0, 1.5)
    velocity_magPWF = GetOpacityTransferFunction('velocity_mag')
    velocity_magPWF.ApplyPreset('mod', True)
    velocity_magPWF.RescaleTransferFunction(0.0, 1.5)


def display_Bar(display, view, visible:bool):
    display.SetScalarBarVisibility(view, visible)

def init_Layout(view, x:int, y:int, camera_position, camera_focalpoint, camera_view_up, camera_parallelscale):
    view.CameraPosition = camera_position
    view.CameraFocalPoint = camera_focalpoint
    view.CameraViewUp = camera_view_up
    view.CameraParallelScale = camera_parallelscale
    #view.EnableRayTracing = 1
    layout = GetLayout()
    layout.SetSize(x, y)

def save_screenshot(layout, file:str, x:int, y:int):
    SaveScreenshot(file, layout, ImageResolution=[x, y], OverrideColorPalette='WhiteBackground', TransparentBackground=0, CompressionLevel='1')
def reset_View(view):
    view.ResetCamera(False)

def update_View(view):
    view.Update()

def clear_ViewsAndLayouts():
    RemoveViewsAndLayouts()

def get_MaterialLibrary():
    return GetMaterialLibrary()

def delete_Source(source):
    Delete(source)
    del source
