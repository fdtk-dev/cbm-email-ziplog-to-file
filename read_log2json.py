import os
import csv
import re
import json
import re
import read_log2json_and_status
import sys
import datetime

def append_status_to_csv_list(log_date, hostname, status_dict, csv_list):
    csv_list.append([log_date, hostname] + list(status_dict.values()))
    # print(csv_list[-1])
    return csv_list

def save_status_to_csv(log_date, hostname, status_dict, csv_filename, csv_list=[]):
    header = ["date", "hostname"] + list(status_dict.keys())
    # print(header)
    if not os.path.exists(csv_filename):
        with open(csv_filename, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(header)
    with open(csv_filename, "a") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_list)

def bonding_two_files_to_one(file_list, cbm_log_dir):
    line_raw = ""
    for i, file in enumerate(file_list):
        file_path = os.path.join(cbm_log_dir, file)
        with open(file_path, "r") as f:
            line_raw += f.read()
    return line_raw
def bonding_one_file_to_one(file, cbm_log_dir):
    file_path = os.path.join(cbm_log_dir, file)
    with open(file_path, "r") as f:
        line_raw = f.read()
    return line_raw

def one_day_log_dictory_key_by_hostname(log_string):
    pattern = r"<div hostname=(.*?)>(.*?)</div hostname=\1>"
    extracted_strings = {}
    matches = re.findall(pattern, log_string, re.DOTALL)
    for match in matches:
        hostname = match[0]
        string = match[1]
        extracted_strings[hostname] = string
    return extracted_strings

def log_dict_key_by_div(log_string):
    pattern = r"<div id=(.*?)>(.*?)</div id=\1>"
    extracted_strings = {}
    matches = re.findall(pattern, log_string, re.DOTALL)
    host_dict_extracted = dict(matches)
    return host_dict_extracted

def main(cmd_args):
    print(cmd_args)
    if cmd_args == "today":
        target_files = files[:2]
        today_date = datetime.datetime.now().strftime("%Y%m%d%H")
        print(target_files,today_date)
        if target_files[0].split("-")[0][:8] != today_date[:8] and target_files[0].split("-")[2] != "pmc.txt":
            print("今天的PMC檔案不存在，請確認。" + target_files[0].split("-")[2] )
            sys.exit()
        if target_files[1].split("-")[1][:8] != today_date[:8] and target_files[1].split("-")[2] != "ceds.txt":
            print("今天的PMC檔案不存在，請確認。")
            sys.exit()
    elif cmd_args == "all":
        target_files = sorted(files)
        csv_filename = f"./cbm_log_csv/Status.csv"
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
    else:
        target_files = files[:2]

    for filename in target_files:
        print(filename)
        # lines_raw = bonding_two_files_to_one(newest_files, directory)
        lines_raw = bonding_one_file_to_one(filename, directory)
        log_dict_key_by_hostname = one_day_log_dictory_key_by_hostname(lines_raw)
        log_date = filename.split("_")[0][:12]
        host_list = list(log_dict_key_by_hostname.keys())
        host_dict = {}
        csv_list = []
        for hostname in host_list:
            csv_filename = f"./cbm_log_csv/Status.csv"
            if not os.path.exists("./cbm_log_csv"):
                os.makedirs("./cbm_log_csv")

            host_dict = log_dict_key_by_div(log_dict_key_by_hostname[hostname])
            host_dict = read_log2json_and_status.showhardconf_status(host_dict)
            host_dict = read_log2json_and_status.uptime_status(host_dict)
            host_dict = read_log2json_and_status.sas2ircu_status(host_dict)
            host_dict = read_log2json_and_status.zpool_status(host_dict)
            host_dict = read_log2json_and_status.netstat_aun_status(host_dict)
            host_dict = read_log2json_and_status.ipadm_status(host_dict)
            host_dict = read_log2json_and_status.temp_status(host_dict)
            host_dict = read_log2json_and_status.volt_status(host_dict)
            host_dict = read_log2json_and_status.Fan_status(host_dict)
            host_dict = read_log2json_and_status.power_status(host_dict)
            host_dict = read_log2json_and_status.air_status(host_dict)
            host_dict = read_log2json_and_status.showboard_status(host_dict)
            host_dict = read_log2json_and_status.cmmc_status(host_dict)
            host_dict = read_log2json_and_status.oracle_status(host_dict)
            host_dict = read_log2json_and_status.bmode_status(host_dict)
            status_dict = host_dict.get("Status")
            csv_list = append_status_to_csv_list(log_date, hostname, status_dict, csv_list)
        save_status_to_csv(log_date, hostname, status_dict, csv_filename, csv_list)
if __name__ == "__main__":
    # Specify the directory path
    directory = "/home/ceds_log/cbm_log"
    # Get the list of files in the directory
    files = os.listdir(directory)
    # Sort the files by modification time (newest first)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    if len(sys.argv) == 2:
        if sys.argv[1] == "all":
            cmd_args = "all"
            main(cmd_args)
        elif sys.argv[1] == "today":
            cmd_args = "today"
            main(cmd_args)
    elif len(sys.argv) > 2:
        print("參數太多，只有一個參數才能接受，請重新輸入。 容許的參數: all，today 或沒有參數")
    else:
        cmd_args = "today"
        print("沒有參數，預設為today。")
        main(cmd_args)