import re


def showhardconf_status(hostname, host_dict):
    # print("showhardconf_status")
    # Create a dictionary to store the extracted content
    host_dict[hostname]["Status"] = {}
    # Extract the CPU informatioGn
    cpu_pattern = r"CPU#0 Status:.*?;"
    cpu_match = re.search(cpu_pattern, host_dict[hostname].get("showhardconf", ""))
    if cpu_match:
        host_dict[hostname]["Status"]["CPU#0 Status"] = re.split(
            r"\W+", cpu_match.group()
        )[-2]
        # print(host_dict[hostname]["Status"]["CPU#0 Status"])

    # Extract the memory information
    mem_pattern = r"MEM#.*? Status:.*?;"
    mem_match = re.findall(mem_pattern, host_dict[hostname].get("showhardconf", ""))
    if mem_match:
        host_dict[hostname]["Status"]["MEM#00A Status"] = re.split(r"\W+", mem_match[0])[
            -2
        ]
        host_dict[hostname]["Status"]["MEM#01A Status"] = re.split(r"\W+", mem_match[1])[
            -2
        ]
        host_dict[hostname]["Status"]["MEM#02A Status"] = re.split(r"\W+", mem_match[2])[
            -2
        ]
        host_dict[hostname]["Status"]["MEM#03A Status"] = re.split(r"\W+", mem_match[3])[
            -2
        ]
        if (
            len(mem_match) > 4
        ):  # Check if there are more than 4 memory modules 這裏南港站的例外處理
            host_dict[hostname]["Status"]["MEM#10A Status"] = re.split(
                r"\W+", mem_match[4]
            )[-2]
            host_dict[hostname]["Status"]["MEM#11A Status"] = re.split(
                r"\W+", mem_match[5]
            )[-2]
            host_dict[hostname]["Status"]["MEM#12A Status"] = re.split(
                r"\W+", mem_match[6]
            )[-2]
            host_dict[hostname]["Status"]["MEM#13A Status"] = re.split(
                r"\W+", mem_match[7]
            )[-2]
        # print(host_dict[hostname]["Status"]["MEM#03A Status"])

    # Extract the power supply information
    psu_pattern = r"PSU#.*? Status:.*?;"
    psu_match = re.findall(psu_pattern, host_dict[hostname].get("showhardconf", ""))
    if psu_match:
        host_dict[hostname]["Status"]["PSU#0 Status"] = re.split(r"\W+", psu_match[0])[
            -2
        ]
        host_dict[hostname]["Status"]["PSU#1 Status"] = re.split(r"\W+", psu_match[1])[
            -2
        ]
        # print(host_dict[hostname]["Status"]["PSU#1 Status"])

    # Extract the fan information
    fan_pattern = r"FANU#.*? Status:.*?;"
    fan_match = re.findall(fan_pattern, host_dict[hostname].get("showhardconf", ""))
    if fan_match:
        host_dict[hostname]["Status"]["FANU#0 Status"] = re.split(r"\W+", fan_match[0])[
            -2
        ]
        host_dict[hostname]["Status"]["FANU#1 Status"] = re.split(r"\W+", fan_match[1])[
            -2
        ]
        host_dict[hostname]["Status"]["FANU#2 Status"] = re.split(r"\W+", fan_match[2])[
            -2
        ]
        host_dict[hostname]["Status"]["FANU#3 Status"] = re.split(r"\W+", fan_match[3])[
            -2
        ]
        host_dict[hostname]["Status"]["FANU#4 Status"] = re.split(r"\W+", fan_match[4])[
            -2
        ]
        host_dict[hostname]["Status"]["FANU#5 Status"] = re.split(r"\W+", fan_match[5])[
            -2
        ]
        host_dict[hostname]["Status"]["FANU#6 Status"] = re.split(r"\W+", fan_match[6])[
            -2
        ]
        # print(host_dict[hostname]["Status"]["FANU#6 Status"])
    return host_dict
