import os, sys, shutil, gzip

def compress(filename_in: str):
    print('file.compressing')
    filename_out = filename_in + ".gz"
    with open(filename_in, "rb") as fin, gzip.open(filename_out, "wb") as fout:
        shutil.copyfileobj(fin, fout)
    print(f"compressed {round(os.stat(filename_in).st_size/1000000)} MB to {round(os.stat(filename_out).st_size/1000000)} MB" )

def move(filename_from: str, filename_to: str):
    print('file.moving')
    shutil.move(filename_from, filename_to)

def copy(filename_from: str, filename_to: str):
    print('file.coping')
    shutil.copy(filename_from, filename_to)

def exists(filename: str):
    return os.path.exists(filename)

def cleardir(dirname: str):
    for f in os.listdir(dirname):
        os.remove(os.path.join(dirname, f))

def nek5000(number: int, temp_folder):
    print('file.nek5000')
    f = open(f"{temp_folder}/jet_data.nek5000", 'w')
    f.write(f"filetemplate: jet_Re3500%01d.f%05d\n")
    f.write(f"firsttimestep: {number:05d}\n")
    f.write("numtimesteps: 1\n")
    f.close()
