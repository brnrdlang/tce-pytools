import tempfile
import os
import shutil
import subprocess

from .generate import generate

def pack(config):
  with tempfile.TemporaryDirectory() as tmpdir:
    for cat, desc in config['pack'].items():
      _, root, rel_path = os.path.splitroot(desc['path'])
      if root == '':
        raise ValueError('Absolute paths must be provided for destination paths')

      p = os.path.join(tmpdir, config['name'], rel_path)
      os.makedirs(p)

      for f in desc['content']:
        if not os.path.isfile(f):
          if os.path.isdir(f):
            shutil.copytree(f, p, dirs_exist_ok=True)
          else:
            try:
              generate(f, p, config)
            except FileNotFoundError:
              raise FileNotFoundError('Could not find %s or a corresponding template file' % f)
        else:
          shutil.copy2(f, p)

    # Make everything owned by root/root
    # TODO Support custom ownership 
    subprocess.run(['mksquashfs', os.path.join(tmpdir, config['name']), config['name'] + '.tcz', '-noappend', '-force-uid', '0', '-force-gid', '0']) 
