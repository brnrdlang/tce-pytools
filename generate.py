import os
import re

def replace(text, config):
  tl = re.split(r':([\w\.]+):', text)

  result = ''
  ct = 0
  for t in tl:
    if ct % 2 == 0:
      result = result + t
    else:
      cl = re.split(r'\.', t)
      rt = config 
      for c in cl:
        rt = rt[c]
      result = result + rt
    ct += 1

  return result

def generate(file_path, destination, config):

  file_name = os.path.basename(file_path)

  with open(file_path + '.template', 'r') as template:
    with open(os.path.join(destination, file_name), 'w') as f:
      t = template.read()
      f.write(replace(t, config))
