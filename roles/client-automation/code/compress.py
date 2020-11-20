import shutil
import tarfile
import os.path

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

list_subfolders_with_paths = [f.path for f in os.scandir(rootdir) if f.is_dir()]

for directory in list_subfolders_with_paths:
    make_tarfile(os.path.basename(directory), directory)
    shutil.rmtree(directory)