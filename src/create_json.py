import json 
import os
import re
# print(os.environ)

def extract(data, prefix, suffix) -> str:
  try:
    prefix_index = data.index(prefix) 
    suffix_index = prefix_index + data[prefix_index:].index(suffix)
    # print(f"Prefix {prefix}|{prefix_index}|{len(prefix)}, suffix {suffix}|{suffix_index}")
    d = data[prefix_index+len(prefix):suffix_index]

    # print("d: ",d)
    return d
  except ValueError as ex:
    if str(ex).find("substring not found") != -1:
      raise Exception(f"Certain markers are missing |{prefix}|. Create a new request")

# data = os.environ["issue_data"]
data_raw =  '"Request Header:\\r\\n\\r\\nRequest Name: test-deployment \\r\\nRequest Config:\\r\\n\\r\\n[CONFIG_BEGIN]\\r\\n```json\\r\\n{\\r\\n \\"key\\" : \\"value\\"\\r\\n}\\r\\n```\\r\\n[CONFIG_END]\\r\\n"'

# start = data_raw.index("[CONFIG_BEGIN]") + len("[CONFIG_BEGIN]")
# end = data_raw.index("[CONFIG_END]")

parsed_data = data_raw.strip("\\r\\n")
parsed_data = parsed_data.replace("\\r\\n","\n")
# print(parsed_data)

# header_index = parsed_data.index("Request Header:")
# header_end = parsed_data[header_index:].index("\n")
# header = header_index+len("Request Header:")

header = extract(parsed_data,"Request Header:","\n")
# print(header)
name = extract(parsed_data,"Request Name:","\n").strip(" \n")
json_data = extract(parsed_data,"[CONFIG_BEGIN]","[CONFIG_END]")
# print("1:",json_data)

print(f"Name:{name}|")

json_data = json_data.strip(" \n").lstrip(" ` ").rstrip(" ` ").removeprefix("json")
json_data = json_data.replace('\\"','"')

# print("2:", json_data)

data = json.loads(json_data)

print(data)

import os

dir_name = os.path.join("deployments",name)
os.mkdir(dir_name)

with open(os.path.join(dir_name,"config.json"), "w") as fp:
  json.dump(json_data,fp)
