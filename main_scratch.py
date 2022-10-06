#!/usr/bin/env pvpython
import paraview_functions as pv
import file_functions as ff


ff.decompress('F:\\visual.cgns.gz', 'F:\\visual.cgns')

source = pv.load_CGNS_5_10('F:\\visual.cgns', ['velocity_mag'], ['Base'])
view = pv.create_View()
display = pv.init_Display(source, view)
pv.color_Display(display)
pv.display_Bar(display, view, True)

CameraPosition = [60, 0, 37.5]
CameraFocalPoint = [-7.116276452281695, -0.6798347127267999, 37.5]
CameraViewUp = [0.0, -1.0, 0.0]
CameraParallelScale = 41.06120959102141
layout = pv.init_Layout(view,3840,2160,CameraPosition,CameraFocalPoint,CameraViewUp,CameraParallelScale)

pv.save_screenshot(view, 'F:\\visual.png',3840,2160)



