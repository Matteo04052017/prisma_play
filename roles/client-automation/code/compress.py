import shutil
import tarfile
import os.path
import sys, getopt

def check_tarfile(tar_filename):
    print("Checking tarball " + tar_filename)
    BLOCK_SIZE = 1024
    with tarfile.open(tar_filename) as tardude:
        for member in tardude.getmembers():
            with tardude.extractfile(member.name) as target:
                for chunk in iter(lambda: target.read(BLOCK_SIZE), b''):
                    pass

def make_tarfile(output_filename, source_dir):
    print("Creating tarball " + output_filename)
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
            ## tarball for events
            tar_name = outdir + "/events/" + os.path.basename(directory) + ".tar.gz"
            if not os.path.isfile(tar_name):
                make_tarfile(tar_name, f)
            else:
                try:
                    check_tarfile(tar_name)
                except:
                    make_tarfile(tar_name, f)
        if (f.is_dir() and "capture" in f.path):
            ## tarball for capture
            tar_name = outdir + "/capture/" + os.path.basename(directory) + ".tar.gz"
            if not os.path.isfile(tar_name):
                make_tarfile(tar_name, f)
            else:
                try:
                    check_tarfile(tar_name)
                except:
                    make_tarfile(tar_name, f)
