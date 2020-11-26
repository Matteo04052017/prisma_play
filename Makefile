

compress:
	ansible client -i inventory -m ansible.builtin.copy -a "src=roles/client-automation/code/compress.py dest=/usr/local/bin/compress.py"
	ansible client -i inventory -a "mkdir /prismadata/rsync/events && mkdir /prismadata/rsync/capture && python3 /home/system/compress.py -r /prismadata/teststation/ -o /prismadata/rsync"
