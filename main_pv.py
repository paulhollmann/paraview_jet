#!/usr/bin/env pvpython
import paraview_functions as pv
import file_functions as ff


################## CONFIG
# no trailing slash
data_folder = "./data_jet"
temp_folder = "./temp_jet" # !! all files will be deleted !!
processed_folder = "./data_jet_processed"
number_frames = 2  # 938
temp_save = False # to save mem
################## CONFIG END

# the data crunching ############################################################################################
for i in range(1, number_frames + 1):
    if ff.exists(f"{processed_folder}/visual{i:05d}.cgns.gz"):
        print(f"visual{i:05d}.cgns.gz already exists skipping")
        continue
    print(f"----------------------------------")
    print(f"STARTING PROCESSING FRAME {i:05d}")
    print(f"----------------------------------")

    # copy the nek5000 data
    if True:
        ff.cleardir(f"{temp_folder}")
        ff.copy(f"{data_folder}/jet_Re35000.f{i:05d}", f"{temp_folder}/jet_Re35000.f{i:05d}")
        ff.copy(f"{data_folder}/jet_Re35001.f{i:05d}", f"{temp_folder}/jet_Re35001.f{i:05d}")
        ff.nek5000(i, temp_folder)


    # cut the hole thing in half
    if True:
        nek5000 = pv.load_VisItNek5000(f"{temp_folder}/jet_data.nek5000", ['velocity', 'velocity_mag'])
        clip = pv.create_Clip(nek5000)
        if temp_save:
            pv.save_Source(clip, f"{temp_folder}/clip.cgns")
            pv.delete_Source(clip)
            pv.delete_Source(nek5000)

    # project on a fast uniform grid
    if True:
        clip = pv.load_CGNS_5_10(f"{temp_folder}/clip.cgns", ['velocity', 'velocity_mag'], ['Base_Volume_Elements'])
        grid = pv.create_FastUniformGrid()
        transform = pv.create_Transformation(grid)
        resample = pv.create_Resample(clip, transform)
        if temp_save:
            pv.save_Source(resample, f"{temp_folder}/resample.cgns")
            pv.delete_Source(resample)
            pv.delete_Source(transform)
            pv.delete_Source(grid)
            pv.delete_Source(clip)

    # compute q-criterion and select iso surfaces
    if True:
        resample = pv.load_CGNS_5_10(f"{temp_folder}/resample.cgns", ['velocity', 'velocity_mag'], ['Base'])
        qcrit = pv.create_QCriterion(resample)
        contour = pv.create_Contour(qcrit)
        if temp_save:
            pv.save_Source(contour, f"{temp_folder}/contour.cgns")
            pv.delete_Source(contour)
            pv.delete_Source(qcrit)
            pv.delete_Source(resample)

    # export the whole
    if True:
        contour = pv.load_CGNS_5_10(f"{temp_folder}/contour.cgns", ['velocity_mag'], ['Base_Surface_Elements'])
        pv.save_SourceCGNS(contour, f"{temp_folder}/visual.cgns")
        if temp_save:
            pv.delete_Source(contour)

    #
    if not temp_save:
        pv.delete_Source(contour)
        pv.delete_Source(qcrit)
        pv.delete_Source(resample)
        pv.delete_Source(transform)
        pv.delete_Source(grid)
        pv.delete_Source(clip)
        pv.delete_Source(nek5000)

    # move the data
    if True:
        ff.compress(f"{temp_folder}/visual.cgns")
        ff.move(f"{temp_folder}/visual.cgns.gz", f"{processed_folder}/visual{i:05d}.cgns.gz")


# the rendering crunching ############################################################################################
for i in range(1, number_frames + 1):
    if ff.exists(f"{processed_folder}/visual{i:05d}.png"):
        print(f"visual{i:05d}.png already exists skipping")
        continue
    if ff.exists(f"{processed_folder}/visual{i:05d}.cgns.gz"):
        print(f"visual{i:05d}.cgns.gz not found, can't render it")
        continue
    print(f"----------------------------------")
    print(f"STARTING RENDERING FRAME {i:05d}")
    print(f"----------------------------------")
    # copy the nek5000 data
    if True:
        ff.cleardir(f"{temp_folder}")
        ff.decompress(f"{processed_folder}/visual{i:05d}.cgns.gz", f"{temp_folder}/visual.cgns")
    if True:
        source = pv.load_CGNS_5_10(f"{temp_folder}/visual.cgns", ['velocity_mag'], ['Base'])
        view = pv.create_View()
        display = pv.init_Display(source, view)
        pv.color_Display(display)
        pv.display_Bar(display, view, True)

        CameraPosition = [60, 0, 37.5]
        CameraFocalPoint = [-7.116276452281695, -0.6798347127267999, 37.5]
        CameraViewUp = [0.0, -1.0, 0.0]
        CameraParallelScale = 41.06120959102141
        layout = pv.init_Layout(view, 3840, 2160, CameraPosition, CameraFocalPoint, CameraViewUp, CameraParallelScale)
        pv.save_screenshot(view, f"{processed_folder}/visual{i:05d}.png", 3840, 2160)


print("Hurrrrrrrrrray we are totally done")