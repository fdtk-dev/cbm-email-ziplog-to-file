import os
import csv
import re
import json
import re
import read_log2json_and_status

# Specify the directory path
directory = "./cbm_log"

# Get the list of files in the directory
files = os.listdir(directory)

# Sort the files by modification time (newest first)
files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

# Get the two newest files
newest_files = files[:2]
today = newest_files[0].split("_")[0][:10]

# Read the contents of the files and store them in the 'lines-1' and 'lines-2' variables
lines_1_raw = ""
lines_2_raw = ""
lines_1 = []
lines_2 = []
for i, file in enumerate(newest_files):
    file_path = os.path.join(directory, file)
    print(file_path)
    with open(file_path, "r") as f:
        if i == 0:
            lines_1_raw = f.read()
            lines_1.extend(f.readlines())
        elif i == 1:
            lines_2_raw = f.read()
            lines_2.extend(f.readlines())
lines_raw = lines_1_raw + lines_2_raw

# Print the contents of the 'lines-1' and 'lines-2' variables
# print(lines_1_raw)
# Define the regex pattern
pattern = r"<div hostname=(.*?)>(.*?)</div hostname=\1>"

# Create a dictionary to store the extracted strings
extracted_strings = {}

# Find all matches of the pattern in the line
matches = re.findall(pattern, lines_raw, re.DOTALL)
# Iterate over the matches
for match in matches:
    # Extract the keyword and the string
    hostname = match[0]
    string = match[1]
    # Add the string to the dictionary using the keyword as the key
    extracted_strings[hostname] = string

# Print the extracted strings
host_list = list(extracted_strings.keys())
host_dict = {}
print(host_list)

for hostname in host_list:
    filename = directory + "/" + today + "_" + hostname + ".raw"
    # Use regex to extract the content between <div id=key> and </div id=key>
    div_pattern = r"<div id=(.*?)>(.*?)</div id=\1>"
    div_content = re.findall(div_pattern, extracted_strings[hostname], re.DOTALL)
    host_dict[hostname] = dict(div_content)

    host_dict = read_log2json_and_status.showhardconf_status(hostname, host_dict)

    # Write the dictionary to a JSON file
    json_filename = f"./cbm_log_json/{today}_{hostname}.json"
    with open(json_filename, "w") as json_file:
        json.dump(host_dict[hostname], json_file)

    csv_filename = f"./cbm_log_csv/{today}_{hostname}.csv"
    status_dict = host_dict[hostname].get("Status")
    header = status_dict.keys()
    rows = [header] + [status_dict.values()]
    print(header)
    print(rows)
    with open(csv_filename, "w") as csv_file:

        writer = csv.writer(csv_file)
        writer.writerows(rows)
    # with open(filename, "w") as f:
    #    f.write(extracted_strings[keyword])
