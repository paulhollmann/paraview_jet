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
    source.Bases = bases #pv5.10.1
    source.PointArrayStatus = elements
    source.DoublePrecisionMesh = 0
    UpdatePipeline(proxy=source)
    return source

def load_CGNS_5_8(file: str, elements, blocks):
    print('pv.load_CGNS_5_8')
    source = CGNSSeriesReader(registrationName='cgns', FileNames=[file])
    source.Blocks = blocks #pv5.8.0
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

def save_SourceVTM(source, file: str, point_data_arrays, field_data_arrays):
    print('pv.save_SourceVTM')
    SetActiveSource(source)
    SaveData(file, proxy=source, PointDataArrays=point_data_arrays, FieldDataArrays=field_data_arrays)
             # ['velocity_mag'], ['ispatch']


def delete_Source(source):
    Delete(source)
    del source
