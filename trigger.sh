#!/usr/bin/env bash
filename=$1
today=Today:${filename:0:8}
file_ext=${filename:0-3}
work_dir=~/cbm_log
base_dir=~/cbm_zip
python_bin=~/miniforge3/envs/procmail/bin/python
if [ "$file_ext" == "zip" ]; then
	unzip -o -d $work_dir $base_dir/$filename
	/usr/bin/rclone copy --max-age 12h $work_dir gd:/05.其他案/高鐵CBM_PCDL-23-0315/cbm-log
	source ~/github/cbm-email-ziplog-to-file/token.ini
	message=$today$(echo -e '\n')$(~/github/cbm-email-ziplog-to-file/m10-1-check.sh)
	$python_bin /home/ceds_log/github/notify/notify_line.py "$message"
	$python_bin /home/ceds_log/github/cbm-email-ziplog-to-file/read_log2json.py today  > /tmp/trigger_status_csv.log
	/usr/bin/rclone copy ~/cbm_log_csv gd:/05.其他案/高鐵CBM_PCDL-23-0315/cbm-log
fi
