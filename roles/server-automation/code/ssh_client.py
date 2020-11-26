import os
from paramiko.client import SSHClient, AutoAddPolicy
from stat import S_ISDIR

def list_from_directory_ssh_host_keys(address, directory):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(address)
    stdin, stdout, stderr = client.exec_command('ls' + directory)
    result = stdout.read().splitlines()
    client.close()
    return result

def download_file_from_ssh_host_keys(address, remote_filepath, local_filepath):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(address)
    sftp = client.open_sftp()
    sftp.get(remote_filepath, local_filepath)
    sftp.close()
    client.close()

def list_from_directory_ssh_user_pass(address, user, passwd, directory):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(address, username=user, password=passwd)
    stdin, stdout, stderr = client.exec_command('ls ' + directory)
    result = stdout.read().splitlines()
    client.close()
    return result

def download_file_from_ssh_user_pass(address, user, passwd, remote_filepath, local_filepath):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(address, username=user, password=passwd)
    sftp = client.open_sftp()
    sftp.get(remote_filepath, local_filepath)
    sftp.close()
    client.close()

def sftp_walk(sftp, remotepath):
    path=remotepath
    files=[]
    folders=[]
    for f in sftp.listdir_attr(remotepath):
        if S_ISDIR(f.st_mode):
            folders.append(f.filename)
        else:
            files.append(f.filename)
    if files:
        yield path, files
    for folder in folders:
        new_path=os.path.join(remotepath,folder)
        for x in sftp_walk(sftp, new_path):
            yield x
