import re


def showhardconf_status(host_dict):
    # print("showhardconf_status")
    # Create a dictionary to store the extracted content
    host_dict["Status"] = {}
    # Extract the CPU informatioGn
    cpu_pattern = r"CPU#0 Status:.*?;"
    cpu_match = re.search(cpu_pattern, host_dict.get("showhardconf", ""))
    if cpu_match:
        host_dict["Status"]["CPU#0 Status"] = re.split( r"\W+", cpu_match.group())[-2]
    else:
        host_dict["Status"]["CPU#0 Status"] = "N/A"

    # Extract the memory information
    mem_pattern = r"MEM#.*? Status:.*?;"
    mem_match = re.findall(mem_pattern, host_dict.get("showhardconf", ""))
    if mem_match:
        host_dict["Status"]["MEM#00A Status"] = re.split(r"\W+", mem_match[0])[ -2 ]
        host_dict["Status"]["MEM#01A Status"] = re.split(r"\W+", mem_match[1])[ -2 ]
        host_dict["Status"]["MEM#02A Status"] = re.split(r"\W+", mem_match[2])[ -2 ]
        host_dict["Status"]["MEM#03A Status"] = re.split(r"\W+", mem_match[3])[ -2 ]
    else:
        host_dict["Status"]["MEM#00A Status"] = "N/A"
        host_dict["Status"]["MEM#01A Status"] = "N/A"
        host_dict["Status"]["MEM#02A Status"] = "N/A"
        host_dict["Status"]["MEM#03A Status"] = "N/A"
        if (
            len(mem_match) > 4
        ):  # Check if there are more than 4 memory modules 這裏南港站的例外處理
            host_dict["Status"]["MEM#10A Status"] = re.split( r"\W+", mem_match[4])[-2]
            host_dict["Status"]["MEM#11A Status"] = re.split( r"\W+", mem_match[5])[-2]
            host_dict["Status"]["MEM#12A Status"] = re.split( r"\W+", mem_match[6])[-2]
            host_dict["Status"]["MEM#13A Status"] = re.split( r"\W+", mem_match[7])[-2]
        # print(host_dict[hostname]["Status"]["MEM#03A Status"])

    # Extract the power supply information
    psu_pattern = r"PSU#.*? Status:.*?;"
    psu_match = re.findall(psu_pattern, host_dict.get("showhardconf", ""))
    if psu_match:
        host_dict["Status"]["PSU#0 Status"] = re.split(r"\W+", psu_match[0])[ -2 ]
        host_dict["Status"]["PSU#1 Status"] = re.split(r"\W+", psu_match[1])[ -2 ]
    else:
        host_dict["Status"]["PSU#0 Status"] = "N/A"
        host_dict["Status"]["PSU#1 Status"] = "N/A"

    # Extract the fan information
    fan_pattern = r"FANU#.*? Status:.*?;"
    fan_match = re.findall(fan_pattern, host_dict.get("showhardconf", ""))
    if fan_match:
        host_dict["Status"]["FANU#0 Status"] = re.split(r"\W+", fan_match[0])[ -2 ]
        host_dict["Status"]["FANU#1 Status"] = re.split(r"\W+", fan_match[1])[ -2 ]
        host_dict["Status"]["FANU#2 Status"] = re.split(r"\W+", fan_match[2])[ -2 ]
        host_dict["Status"]["FANU#3 Status"] = re.split(r"\W+", fan_match[3])[ -2 ]
        host_dict["Status"]["FANU#4 Status"] = re.split(r"\W+", fan_match[4])[ -2 ]
        host_dict["Status"]["FANU#5 Status"] = re.split(r"\W+", fan_match[5])[ -2 ]
        host_dict["Status"]["FANU#6 Status"] = re.split(r"\W+", fan_match[6])[ -2 ]
    else:
        host_dict["Status"]["FANU#0 Status"] = "N/A"
        host_dict["Status"]["FANU#1 Status"] = "N/A"
        host_dict["Status"]["FANU#2 Status"] = "N/A"
        host_dict["Status"]["FANU#3 Status"] = "N/A"
        host_dict["Status"]["FANU#4 Status"] = "N/A"
        host_dict["Status"]["FANU#5 Status"] = "N/A"
        host_dict["Status"]["FANU#6 Status"] = "N/A"
    return host_dict

def uptime_status(host_dict):
    uptime_pattern = r"up (.*?) day"
    uptime_match = re.findall(uptime_pattern, host_dict.get("uptime", ""))
    if uptime_match:
        host_dict["Status"]["uptime"] = uptime_match[0]
    else:
        host_dict["Status"]["uptime"] = "N/A"
    load_average_match = re.findall(r"load average: (.*)", host_dict.get("uptime", ""))
    if load_average_match:
        host_dict["Status"]["load_average_last_1_min"] = re.split(r", ?", load_average_match[0])[0]
        host_dict["Status"]["load_average_last_5_min"] = re.split(r", ?", load_average_match[0])[1]
        host_dict["Status"]["load_average_last_15_min"] = re.split(r", ?", load_average_match[0])[2]
    else:
        host_dict["Status"]["load_average_last_1_min"] = "N/A"
        host_dict["Status"]["load_average_last_5_min"] = "N/A"
        host_dict["Status"]["load_average_last_15_min"] = "N/A"
    return host_dict

def sas2ircu_status(host_dict):
    # Extract the SAS2IRCU information
    sas2ircu_pattern = r"Status of volume .*: (.*) .*\n"
    sas2ircu_match = re.findall(sas2ircu_pattern, host_dict.get("sas2ircu", ""))
    if sas2ircu_match:
        host_dict["Status"]["Status_of_volume"] = sas2ircu_match[0]
    else:
        host_dict["Status"]["Status_of_volume"] = "N/A"
    Hard_disk_2_0_pattern = r"State.*: (.*) .*\n.*Size"
    Hard_disk_2_0_pattern_match = re.findall(Hard_disk_2_0_pattern, host_dict.get("sas2ircu", ""))

    hard_dict = dict(enumerate(Hard_disk_2_0_pattern_match))
    if Hard_disk_2_0_pattern_match:
        host_dict["Status"]["Hard_disk_2_0"] = hard_dict.get(0)
        host_dict["Status"]["Hard_disk_2_1"] = hard_dict.get(1)
        host_dict["Status"]["Hard_disk_2_2"] = hard_dict.get(2,"N/A")
        host_dict["Status"]["Hard_disk_2_3"] = hard_dict.get(3,"N/A")
    return host_dict

if __name__ == "__main__":
    # uptime_status()
    # Extract the uptime information
    pass