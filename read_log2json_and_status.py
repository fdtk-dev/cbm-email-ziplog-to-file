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
        host_dict["Status"]["Hard_disk_2_0"] = hard_dict.get(0,"N/A")
        host_dict["Status"]["Hard_disk_2_1"] = hard_dict.get(1,"N/A")
        host_dict["Status"]["Hard_disk_2_2"] = hard_dict.get(2,"N/A")
        host_dict["Status"]["Hard_disk_2_3"] = hard_dict.get(3,"N/A")
    else:
        host_dict["Status"]["Hard_disk_2_0"] = "N/A"
        host_dict["Status"]["Hard_disk_2_1"] = "N/A"
        host_dict["Status"]["Hard_disk_2_2"] = "N/A"
        host_dict["Status"]["Hard_disk_2_3"] = "N/A"
    return host_dict

def zpool_status(host_dict):
    # Extract the zpool information
    '''NAME   SIZE  ALLOC  FREE  CAP  DEDUP  HEALTH  ALTROOT
       rpool  556G  48.6G  507G   8%  1.00x  ONLINE  - '''
    zpool_pattern = r"rpool *\d*G *(\d*\.?\d*)G *(\d*)G *(\d*)% *\d.\d*x *(\w*)  "
    zpool_match = re.findall(zpool_pattern, host_dict.get("zpool", ""))
    if zpool_match:
        zpool_dict = dict(enumerate(zpool_match[0]))
        # print(zpool_dict)
        host_dict["Status"]["rpool_state"] = zpool_dict.get(3)
        host_dict["Status"]["rpool_CAP"] = zpool_dict.get(2)
    else:
        host_dict["Status"]["rpool_state"] = "N/A"
        host_dict["Status"]["rpool_CAP"] = "N/A"
    return host_dict

def netstat_aun_status(host_dict):
    # Extract the netstat -aun information
    netstat_aun_pattern = r"\n {6}\*\.(\d+)[ \.\*]*(\w*) *(\d*) (\w*.\w*).*LISTEN"
    netstat_aun_match = re.findall(netstat_aun_pattern, host_dict.get("netstat_aun", ""))
    # print(netstat_aun_match)
    netstat_aun_listen_list = list(set([item[0] for item in netstat_aun_match]))
    if netstat_aun_match:
        netstat_aun_dict = dict(enumerate(netstat_aun_listen_list))
        # print(sorted(list(netstat_aun_dict.values()),key=int))
        host_dict["Status"]["IPv4_LISTEN"] = "/".join(sorted(list(netstat_aun_dict.values()),key=int))
    else:
        host_dict["Status"]["netstat_aun_LISTEN"] = "N/A"
    return host_dict

def ipadm_status(host_dict):
    # Extract the ipadm information
    ipadm_pattern = r"(net\d\d?\/v4) *\w* *(\w*) *-- *[\d\.\/]*\n"
    ipadm_match = re.findall(ipadm_pattern, host_dict.get("ipadm", ""))
    ipadm_dict = dict(ipadm_match)
    if ipadm_match:
        ipadm_dict = dict(ipadm_match)
        # print(ipadm_dict)
        host_dict["Status"]["net0/v4_STATE"] = ipadm_dict.get("net0/v4","N/A")
        host_dict["Status"]["net1/v4_STATE"] = ipadm_dict.get("net1/v4","N/A")
        host_dict["Status"]["net2/v4_STATE"] = ipadm_dict.get("net2/v4","N/A")
        host_dict["Status"]["net3/v4_STATE"] = ipadm_dict.get("net3/v4","N/A")
        host_dict["Status"]["net4/v4_STATE"] = ipadm_dict.get("net4/v4","N/A")
        host_dict["Status"]["net5/v4_STATE"] = ipadm_dict.get("net5/v4","N/A")
        host_dict["Status"]["net6/v4_STATE"] = ipadm_dict.get("net6/v4","N/A")
        host_dict["Status"]["net7/v4_STATE"] = ipadm_dict.get("net7/v4","N/A")
        host_dict["Status"]["net8/v4_STATE"] = ipadm_dict.get("net8/v4","N/A")
        host_dict["Status"]["net9/v4_STATE"] = ipadm_dict.get("net9/v4","N/A")
        host_dict["Status"]["net10/v4_STATE"] = ipadm_dict.get("net10/v4","N/A")
        host_dict["Status"]["net11/v4_STATE"] = ipadm_dict.get("net11/v4","N/A")
                                                     
    else:
        host_dict["Status"]["net0/v4_STATE"] = "N/A"
        host_dict["Status"]["net1/v4_STATE"] = "N/A"   
        host_dict["Status"]["net2/v4_STATE"] = "N/A"
        host_dict["Status"]["net3/v4_STATE"] = "N/A"
        host_dict["Status"]["net4/v4_STATE"] = "N/A"
        host_dict["Status"]["net5/v4_STATE"] = "N/A"
        host_dict["Status"]["net6/v4_STATE"] = "N/A"
        host_dict["Status"]["net7/v4_STATE"] = "N/A"
        host_dict["Status"]["net8/v4_STATE"] = "N/A"
        host_dict["Status"]["net9/v4_STATE"] = "N/A"
        host_dict["Status"]["net10/v4_STATE"] = "N/A"
        host_dict["Status"]["net11/v4_STATE"] = "N/A"
    return host_dict

def temp_status(host_dict):
    # Extract the temperature information
    temp_pattern = r"(\w*#?\w*):([\d\.]*)C\n"
    temp_match = re.findall(temp_pattern, host_dict.get("temp", ""))
    if temp_match:
        temp_dict = dict(temp_match)
        # print(temp_dict)
        host_dict["Status"]["Temperature"] = temp_dict.get("Temperature","N/A")
        host_dict["Status"]["CPU_0_Temperature"] = temp_dict.get("CPU#0","N/A")
        host_dict["Status"]["MEM_00A_Temperature"] = temp_dict.get("MEM#00A","N/A")
        host_dict["Status"]["MEM_01A_Temperature"] = temp_dict.get("MEM#01A","N/A")
        host_dict["Status"]["MEM_02A_Temperature"] = temp_dict.get("MEM#02A","N/A")
        host_dict["Status"]["MEM_03A_Temperature"] = temp_dict.get("MEM#03A","N/A")
        host_dict["Status"]["SAS_Temperature"] = temp_dict.get("SAS","N/A")
    else:
        host_dict["Status"]["Temperature"] = "N/A"
        host_dict["Status"]["CPU_0_Temperature"] = "N/A"
        host_dict["Status"]["MEM_00A_Temperature"] = "N/A"
        host_dict["Status"]["MEM_01A_Temperature"] = "N/A"
        host_dict["Status"]["MEM_02A_Temperature"] = "N/A"
        host_dict["Status"]["MEM_03A_Temperature"] = "N/A"
        host_dict["Status"]["SAS_Temperature"] = "N/A"
    return host_dict

def volt_status(host_dict):
    # Extract the voltage information
    volt_pattern = r"(\d\.\d*V#?\d?).*:(\d\.\d*)V"
    volt_match = re.findall(volt_pattern, host_dict.get("volt", ""))
    if volt_match:
        volt_dict = dict(volt_match)
        # print(volt_dict)
        host_dict["Status"]["MBU_1_35V_0_volt"] = volt_dict.get("1.35V#0","N/A")
        host_dict["Status"]["MBU_1_35V_1_volt"] = volt_dict.get("1.35V#1","N/A")
        host_dict["Status"]["MBU_1_5V_0_volt"] = volt_dict.get("1.5V#0","N/A")
        host_dict["Status"]["MBU_1_5V_1_volt"] = volt_dict.get("1.5V#1","N/A")
        host_dict["Status"]["PSUBP_3_3V"] = volt_dict.get("3.3V","N/A")
        host_dict["Status"]["PSUBP_5_0V"] = volt_dict.get("5.0V","N/A")
    else:
        host_dict["Status"]["MBU_1_35V_0_volt"] = "N/A"
        host_dict["Status"]["MBU_1_35V_1_volt"] = "N/A"
        host_dict["Status"]["MBU_1_5V_0_volt"] = "N/A"
        host_dict["Status"]["MBU_1_5V_1_volt"] = "N/A"
        host_dict["Status"]["PSUBP_3_3V"] = "N/A"
        host_dict["Status"]["PSUBP_5_0V"] = "N/A"
    return host_dict

def Fan_status(host_dict):
    # Extract the fan information
    fan_pattern = r"    (FAN#\d): (.*)\n.*FAN#0:  (\d*)rpm\n.*FAN#1:  (\d*)rpm\n"
    fan_match = re.findall(fan_pattern, host_dict.get("Fan", ""))
    fan_not_available_dict_return = ["N/A","N/A","N/A"]
    fan_dict = {item[0]: item[1:] for item in fan_match}
    if fan_match:
        host_dict["Status"]["FAN_0_0"] = fan_dict.get("FAN#0",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_0_1"] = fan_dict.get("FAN#0",fan_not_available_dict_return)[2]
        host_dict["Status"]["FAN_1_0"] = fan_dict.get("FAN#1",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_1_1"] = fan_dict.get("FAN#1",fan_not_available_dict_return)[2]
        host_dict["Status"]["FAN_2_0"] = fan_dict.get("FAN#2",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_2_1"] = fan_dict.get("FAN#2",fan_not_available_dict_return)[2]
        host_dict["Status"]["FAN_3_0"] = fan_dict.get("FAN#3",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_3_1"] = fan_dict.get("FAN#3",fan_not_available_dict_return)[2]
        host_dict["Status"]["FAN_4_0"] = fan_dict.get("FAN#4",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_4_1"] = fan_dict.get("FAN#4",fan_not_available_dict_return)[2]
        host_dict["Status"]["FAN_5_0"] = fan_dict.get("FAN#5",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_5_1"] = fan_dict.get("FAN#5",fan_not_available_dict_return)[2]
        host_dict["Status"]["FAN_6_0"] = fan_dict.get("FAN#6",fan_not_available_dict_return)[1]
        host_dict["Status"]["FAN_6_1"] = fan_dict.get("FAN#6",fan_not_available_dict_return)[2]
    else:
        host_dict["Status"]["FAN_0_0"] = "N/A"
        host_dict["Status"]["FAN_0_1"] = "N/A"
        host_dict["Status"]["FAN_1_0"] = "N/A"
        host_dict["Status"]["FAN_1_1"] = "N/A"
        host_dict["Status"]["FAN_2_0"] = "N/A"
        host_dict["Status"]["FAN_2_1"] = "N/A"
        host_dict["Status"]["FAN_3_0"] = "N/A"
        host_dict["Status"]["FAN_3_1"] = "N/A"
        host_dict["Status"]["FAN_4_0"] = "N/A"
        host_dict["Status"]["FAN_4_1"] = "N/A"
        host_dict["Status"]["FAN_5_0"] = "N/A"
        host_dict["Status"]["FAN_5_1"] = "N/A"
        host_dict["Status"]["FAN_6_0"] = "N/A"
        host_dict["Status"]["FAN_6_1"] = "N/A"
    return host_dict

def power_status(host_dict):
    # Extract the power information
    power_pattern = r"Actual AC power consumption   :(\d*)W\n"
    power_match = re.findall(power_pattern, host_dict.get("power", ""))
    if power_match:
        # print(power_match)
        host_dict["Status"]["Actual_AC_power_consumption"] = power_match[0]
    else:
        host_dict["Status"]["Actual_AC_power_consumption"] = "N/A"
    return host_dict

def air_status(host_dict):
    # Extract the air information
    air_pattern = r"Air Flow:(\d*)CMH"
    air_match = re.findall(air_pattern, host_dict.get("air", ""))
    if air_match:
        # print(air_match)
        host_dict["Status"]["Air_Flow"] = air_match[0]
    else:
        host_dict["Status"]["Air_Flow"] = "N/A"
    return host_dict

def showboard_status(host_dict):
    # Extract the showboard information
    showboard_pattern = r"00-0 00\(00\) *\w* *\w* *\w *\w *\w* *(\w*)"
    showboard_match = re.findall(showboard_pattern, host_dict.get("showboards", ""))
    # print(showboard_match)
    if showboard_match:
        host_dict["Status"]["PSB_00_0_Fault"] = showboard_match[0]
    else:
        host_dict["Status"]["PSB_00_0_Fault"] = "N/A"
    return host_dict

def cmmc_status(host_dict):
    # Extract the cmmc information
    cmmc_pattern = r"Own Status.*\[(.*)\]\n"
    cmmc_match = re.findall(cmmc_pattern, host_dict.get("cmmc", ""))
    cmmc_process_pattern = r"  Number of Process \[(\w*)\]\n"
    cmmc_process_match = re.findall(cmmc_process_pattern, host_dict.get("cmmc", ""))
    if cmmc_match:
        # print(cmmc_match)
        host_dict["Status"]["Own_Status"] = cmmc_match[0]
    else:
        host_dict["Status"]["Own_Status"] = "N/A"
    if cmmc_process_match:
        # print(cmmc_process_match)
        host_dict["Status"]["CEDS_Number_of_Process"] = cmmc_process_match[0]
    else:
        host_dict["Status"]["CEDS_Number_of_Process"] = "N/A"
    return host_dict

def oracle_status(host_dict):
    # Extract the oracle information
    oracle_pattern = r"----------\n *(\d*)\n"
    oracle_match = re.findall(oracle_pattern, host_dict.get("oracle", ""))
    oracle_usage_pattern = r"rpool\/oradata *\w* *\w* *\w* *(\w*)% *\/oradata\n"
    oracle_usage_match = re.findall(oracle_usage_pattern, host_dict.get("df", ""))
    if oracle_match:
        # print(oracle_match)
        host_dict["Status"]["CEDS_almevt_k_dbt_count"] = oracle_match[0]
    else:
        host_dict["Status"]["CEDS_almevt_k_dbt_count"] = "N/A"
    if oracle_usage_match:
        # print(oracle_usage_match)
        host_dict["Status"]["CEDS_oradata_Usage"] = oracle_usage_match[0]
    else:
        host_dict["Status"]["CEDS_oradata_Usage"] = "N/A"
    return host_dict

def bmode_status(host_dict):
    # Extract the bmode information
    bmode_pattern = r"Own System  > From mode\[.*\] -> To mode:\[(.*)\] \n"
    bmode_match = re.findall(bmode_pattern, host_dict.get("bmode", ""))
    if bmode_match:
        # print(bmode_match)
        host_dict["Status"]["SCADA_To_mode"] = bmode_match[0]
    else:
        host_dict["Status"]["SCADA_To_mode"] = "N/A"
    return host_dict


if __name__ == "__main__":
    # uptime_status()
    # Extract the uptime information
    pass