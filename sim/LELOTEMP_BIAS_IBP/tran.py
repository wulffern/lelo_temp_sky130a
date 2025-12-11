#!/usr/bin/env python3
import pandas as pd
import yaml

def fromEng(ss):
  if(type(ss) is float):
    return ss
  else:
    return float(ss.replace("u","e-6").replace("n","e-9"))

def main(name):
  # Delete next line if you want to use python post processing
  yamlfile = name + ".yaml"
  # Read result yaml file
  with open(yamlfile) as fi:
    obj = yaml.safe_load(fi)

  with open("replace.yaml") as fi:
    replace = yaml.safe_load(fi)

  obj["t_settle"] = fromEng(replace["t_end"]) -fromEng(obj["t_settle_rev"]) - fromEng(replace["t_start"])

  # Save new yaml file
  with open(yamlfile,"w") as fo:
    yaml.dump(obj,fo)
