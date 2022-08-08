#!/usr/bin/env pvpython
import paraview_functions as pv
import file_functions as ff

################## CONFIG
# no trailing slash
data_folder = "./data_jet"
temp_folder = "./temp_jet" # !! all files will be deleted !!
processed_folder = "./data_jet_processed"
number_frames = 2  # 938
pv_version = "5.10" #"5.10", "5.8" TODO
temp_save = False
################## CONFIG END

for i in range(1, number_frames + 1):
    if ff.exists(f"{processed_folder}/visual{i:05d}.cgns.gz"):
        print(f"visual{i:05d}.cgns.gz already exists skipping")
        continue
    print(f"----------------------------------")
    print(f"STARTING FRAME {i:05d}")
    print(f"----------------------------------")
    #ff.cleardir(f"{temp_folder}")

    # copy the nek5000 data
    if False:
        ff.copy(f"{data_folder}/jet_Re35000.f{i:05d}", f"{temp_folder}/jet_Re35000.f{i:05d}")
        ff.copy(f"{data_folder}/jet_Re35001.f{i:05d}", f"{temp_folder}/jet_Re35001.f{i:05d}")
        ff.nek5000(i, temp_folder)


    # cut the hole thing in half and save
    if True:
        nek5000 = pv.load_VisItNek5000(f"{temp_folder}/jet_data.nek5000", ['velocity', 'velocity_mag'])
        clip = pv.create_Clip(nek5000)
        if temp_save:
            pv.save_Source(clip, f"{temp_folder}/clip.cgns")
            pv.delete_Source(clip)
            pv.delete_Source(nek5000)

    # project on a fast uniform grid
    if True:
        if (pv_version == "5.10") & temp_save:
            clip = pv.load_CGNS_5_10(f"{temp_folder}/clip.cgns", ['velocity', 'velocity_mag'], ['Base_Volume_Elements'])
        if (pv_version == "5.8") & temp_save:
            clip = pv.load_CGNS_5_8(f"{temp_folder}/clip.cgns", ['velocity', 'velocity_mag'], ['/Hierarchy/Base_Volume_Elements/Zone 1/Grid'])
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
    if False:
        if pv_version == "5.10" & temp_save:
            resample = pv.load_CGNS_5_10(f"{temp_folder}/resample.cgns", ['velocity', 'velocity_mag'], ['Base'])
        if pv_version == "5.8" & temp_save:
            resample = pv.load_CGNS_5_8(f"{temp_folder}/resample.cgns", ['velocity', 'velocity_mag'], ['Base'])
        qcrit = pv.create_QCriterion(resample)
        contour = pv.create_Contour(qcrit)
        if temp_save:
            pv.save_Source(contour, f"{temp_folder}/contour.cgns")
            pv.delete_Source(contour)
            pv.delete_Source(qcrit)
            pv.delete_Source(resample)

    # export the whole
    if False:
        if pv_version == "5.10" & temp_save:
            contour = pv.load_CGNS(f"{temp_folder}/contour.cgns", ['velocity_mag'], ['Base_Surface_Elements'])
        if pv_version == "5.8" & temp_save:
            contour #= pv.load_CGNS(f"{temp_folder}/contour.cgns", ['velocity_mag'], ['Base_Surface_Elements'])#todo

        # todo export
        pv.save_SourceVTM(contour, f"{temp_folder}/export/visual.vtm")
        pv.save_SourceC(contour, f"{temp_folder}/visual.cgns")
        pv.delete_Source(contour)

    # move the data
    if False:
        ff.compress(f"{temp_folder}/visual.cgns")
        ff.move(f"{temp_folder}/visual.cgns.gz", f"{processed_folder}/visual{i:05d}.cgns.gz")


print("Hurrrrrrrrrray we are totally done")