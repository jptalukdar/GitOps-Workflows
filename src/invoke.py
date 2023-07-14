import os
import json
from datetime import datetime

class Deployment():
  base_path = ""
  base_name = ""
  subfiles = []
  config = {}
  def set_base_name(self, name):
    self.base_name = name
  
  def deploy(self):
    print(f"Processing {self.base_name}")
    self.mark_completed()

  def delete(self):
    print(f"Deleting {self.base_name}")
    for file in self.subfiles:
      os.remove(os.path.join(self.base_path, file))
    os.rmdir(self.base_path)

  
  def mark_completed(self):
    with open(os.path.join(self.base_path,"completed.keep") , "w") as fp:
      fp.write(self.base_name+"\n")
      fp.write(str(datetime.now()))

  def mark_failed(self):
    with open(os.path.join(self.base_path,"failed.keep") , "w") as fp:
      fp.write(self.base_name+"\n")
      fp.write(str(datetime.now()))

def mark_changed():
  with open(os.path.join("changed.nokeep") , "w") as fp:
      fp.write("\n")
      fp.write(str(datetime.now()))

def read_json(path: str) -> dict:
  with open(path, "r") as fp:
    data = json.load(fp)
  return data

def get_deployments(root_dir):
  deployments = []
  deletions = []
  for root, dirs, files in os.walk(root_dir):
    print("Found deployments: ",dirs, " on ", root_dir, files)
    for dir in dirs:
      print("Parsing Directory: " + os.path.join(root, dir))
      d_ = Deployment()
      d_.base_path = os.path.join(root, dir)
      d_.set_base_name(os.path.basename(dir))
      subfiles = os.listdir(d_.base_path)
      subfiles = [f for f in subfiles if os.path.isfile(os.path.join(d_.base_path, f))] #Filtering only the files.
      d_.subfiles = subfiles
      if "delete.keep" in subfiles:
        deletions.append(d_)
        continue
      if "completed.keep" in subfiles:
        continue # Directory allready processed so skip 
      if "config.json" in subfiles:
        d_.config = read_json(os.path.join(d_.base_path, "config.json"))
      deployments.append(d_)
    break

  return deployments,deletions

def process_deployment_creation(deploy_list: list[Deployment]) -> None:
  for d in deploy_list:
    print(f"Deploying {d.base_name}")
    d.deploy()
    mark_changed()

def process_deployment_deletion(deploy_list: list[Deployment]) -> None:
  for d in deploy_list:
    print(f"Deleting {d.base_name}")
    d.delete()
    mark_changed()

if __name__ == "__main__":
  d_list = get_deployments("deployments")
  process_deployment_creation(d_list[0])
  process_deployment_deletion(d_list[1])