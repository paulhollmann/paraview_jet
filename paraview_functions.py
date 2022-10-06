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

def create_FastUniformGrid():
    print('pv.create_FastUniformGrid')
    fastUniformGrid = FastUniformGrid(registrationName='fastUniformGrid')
    fastUniformGrid.WholeExtent = [-250, 0, -250, 250, 0, 750]
    return fastUniformGrid

def create_Transformation(source):
    print('pv.create_Transformation')
    transform = Transform(registrationName='transform', Input=source)
    transform.Transform = 'Transform'
    transform.Transform.Scale = [0.1, 0.1, 0.1]
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
    return display
def color_Display(display):
    ColorBy(display, ('POINTS', 'velocity_mag'))
    display.RescaleTransferFunctionToDataRange(True, False)

def display_Bar(display, view, visible:bool):
    display.SetScalarBarVisibility(view, visible)

def init_Layout(view, x:int, y:int, camera_position, camera_focalpoint, camera_view_up, camera_parallelscale):
    layout = GetLayout()
    layout.SetSize(x, y)
    view.CameraPosition = camera_position
    view.CameraFocalPoint = camera_focalpoint
    view.CameraViewUp = camera_view_up
    view.CameraParallelScale = camera_parallelscale

def save_screenshot(view, file:str, x:int, y:int):
    SaveScreenshot(file, view, ImageResolution=[x, y], OverrideColorPalette='WhiteBackground', TransparentBackground=1, CompressionLevel='1')
def reset_View(view):
    view.ResetCamera(False)

def update_View(view):
    view.Update()

def get_MaterialLibrary():
    return GetMaterialLibrary()

def delete_Source(source):
    Delete(source)
    del source
