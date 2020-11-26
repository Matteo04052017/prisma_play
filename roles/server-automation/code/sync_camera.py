## get capture and events from camera 

import shutil
import tarfile
import os.path
import sys, getopt
from archive import get_archived_files
from ssh_client import download_file_from_ssh_host_keys, list_from_directory_ssh_host_keys

camera_address = ""
camera_directory_to_sync = ""
local_directory = ""
archived_already = []
## parse arguments
try:
    opts, args = getopt.getopt(sys.argv[1:], "a:d:l:", ["address=", "directory=", "local_directory="])

except getopt.GetoptError:
    print("Please provide proper arguments.")
    print("Usage: $python sync_camera.py --address=<camera_address> --directory=<camera_directory_to_sync> --local_directory=<local_directory>")
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-a", "--address"):
        camera_address = arg
    if opt in ("-d", "--directory"):
        camera_directory_to_sync = arg
    if opt in ("-l", "--local_directory"):
        local_directory = arg

archived_already = get_archived_files()

files_to_sync = list_from_directory_ssh_host_keys(camera_address, camera_directory_to_sync)
for f in files_to_sync:
    if not f in archived_already:
        download_file_from_ssh_host_keys(camera_address, camera_directory_to_sync + f, local_directory)

