import json 
import os

print(os.environ)

with open("issue_data", "r") as fp:
  data = fp.read()

print(data)