#!/usr/bin/env bash
filename=$1
today=Today:${filename:4:8}
work_dir=/home/ceds_log/cbm_log
base_dir=/home/ceds_log/cbm_zip
python_bin=/home/ceds_log/miniforge3/envs/procmail/bin/python
unzip -o -d $work_dir $base_dir/$filename
/usr/bin/rclone copy --max-age 12h $work_dir gd:/05.其他案/高鐵CBM_PCDL-23-0315/cbm-log
