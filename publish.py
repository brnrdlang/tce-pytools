import os
import hashlib
import tarfile
import subprocess

from .generate import generate

def find_size(filepath):
  size = os.stat(filepath).st_size
  for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
      if size < 1024.0 or unit == 'PiB':
        break
      size /= 1024.0
  return f"{size:.{1}f} {unit}"

def publish(config):
  # measure file size
  config['pack']['size'] = find_size(config['name'] + '.tcz')

  # create .info from template
  generate(config['name'] + '.tcz.info', '.', config)

  # create list from unsquashfs - should this be created by pack script instead?
  imagelist = subprocess.check_output(['unsquashfs', '-lc', config['name'] + '.tcz'])
  with open(config['name'] + '.tcz.list', 'wb') as lfile:
    lfile.writelines([line[13:] + b'\n' for line in imagelist.splitlines()])

  # md5 hash 
  with open(config['name'] + '.tcz', 'rb') as f:
    digest = hashlib.file_digest(f, "md5")

  with open(config['name'] + '.tcz.md5', 'w') as md5:
    md5.write(digest.hexdigest())
    md5.write("  " + config['name'] + '.tcz\n')

  # tarball source code
  if 'source' in config['build']:
      vs = ''
      if 'version' in config['build']:
          vs = config['build']['version']
      with tarfile.open(config['name'] + '-' + vs + '-source.tar', 'w') as tar:
        tar.add(config['build']['source'])

  # archive extension + metadata files for publishing
