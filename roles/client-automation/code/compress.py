import shutil
import tarfile
import os.path
import sys, getopt

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

rootdir = ""
## parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "r:", ["rootdir="])

except getopt.GetoptError:
    print("Please provide proper arguments.")
    print("Usage: $python compress.py --rootdir=<rootdir>")
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-r", "--rootdir"):
        rootdir = arg

list_subfolders_with_paths = []
for f in os.scandir(rootdir):
    if (f.is_dir()):
        list_subfolders_with_paths.append(f.path)

for directory in list_subfolders_with_paths:
    tar_name = directory + "/" + os.path.basename(directory) + ".tar.gz"
    for f in os.scandir(directory):
        if (f.is_dir() and "events" in f.path):
            tar_name = directory + "/" + os.path.basename(directory) + "_events.tar.gz"
    print("make tar of diretory " + str(directory) + "with name: " + tar_name)
    #make_tarfile(tar_name, directory)
    #shutil.rmtree(directory)
