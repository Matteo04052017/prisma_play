import shutil
import tarfile
import os.path
import sys, getopt

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

rootdir = ""
outdir = ""
## parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "r:o:", ["rootdir=", "outdir="])

except getopt.GetoptError:
    print("Please provide proper arguments.")
    print("Usage: $python compress.py --rootdir=<rootdir> --outdir=<outdir>")
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-r", "--rootdir"):
        rootdir = arg
    if opt in ("-o", "--outdir"):
        outdir = arg

list_subfolders_with_paths = []
for f in os.scandir(rootdir):
    if (f.is_dir()):
        list_subfolders_with_paths.append(f.path)

for directory in list_subfolders_with_paths:
    tar_name = outdir + "/" + os.path.basename(directory) + ".tar.gz"
    for f in os.scandir(directory):
        if (f.is_dir() and "events" in f.path):
            tar_name = outdir + "/" + os.path.basename(directory) + "_with_events.tar.gz"
    print("make tar of diretory " + str(directory) + " with name: " + tar_name)
    if not os.path.isfile(tar_name):
        make_tarfile(tar_name, directory)
    #shutil.rmtree(directory)
