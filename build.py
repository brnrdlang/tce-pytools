import subprocess
import os
def build(config):
  print(os.getcwd())
  
  build_path = os.path.join(os.getcwd(), config['build']['path'])
  if 'version' in config['build']:
    subprocess.run([build_path, config['build']['version']])
  else:
    subprocess.run([build_path])
