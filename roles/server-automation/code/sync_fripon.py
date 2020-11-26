## get capture and events from ftp fripon

import shutil
import tarfile
import os
import sys, getopt
from datetime import date, timedelta
from archive import get_archived_files
from ssh_client import download_file_from_ssh_user_pass, list_from_directory_ssh_user_pass

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

fripon_address = "ssh.fripon.org"
fripon_username = ""
fripon_password = ""
fripon_capture_diretory = "/data/fripon_stations"
fripon_events_directory = "/data/fripon_detections/multiple"
cameras_to_sync = ["ITER01"]
tmp_directory = "/tmp"
last_n_days = 5

archived_already = get_archived_files()

## get capture of the last n days
month_capture_directories = [date.today().strftime("%Y%m")]
to_date = date.today() - timedelta(days=1) #yesterday
from_date = to_date - timedelta(days=last_n_days)
time_elapsed = to_date - from_date
for x in range(int(time_elapsed.days / 30)):
    date_to_consider = to_date - timedelta(days=x)
    month_capture_directories.append(date_to_consider.strftime("%Y%m"))

day_capture_directories = []
for x in range(time_elapsed.days):
    date_to_consider = to_date - timedelta(days=x)
    day_capture_directories.append(date_to_consider.strftime("%Y%m%d"))

for camera in cameras_to_sync:
    for capture_dir in month_capture_directories: 
        list_dir = fripon_capture_diretory + "/" + str(camera) + "/" + str(capture_dir)
        all_capture_files = list_from_directory_ssh_user_pass(fripon_address, fripon_username, fripon_password, list_dir)
        download_dir = tmp_directory + "/" + str(camera) + "/" + str(capture_dir)
        if not os.path.isdir(download_dir):
            os.makedirs(download_dir)
        for f in all_capture_files:
            check_name = str(str(f.decode()).split('_')[1])[:8]
            if check_name in day_capture_directories:
                remote_file = list_dir + "/" + str(f.decode())
                local_file = download_dir + "/" + str(f.decode())
                download_file_from_ssh_user_pass(fripon_address, fripon_username, fripon_password, remote_file, local_file)

        ## calibrate?
        ## zip and archive


        

