"""Usage:
    tce-pytools [--version=<version>] 
    tce-pytools build [--version=<version>]
    tce-pytools pack
    tce-pytools publish
"""

from docopt import docopt
import tomllib

from . import build, pack, publish
arguments = docopt(__doc__)

with open("extension.toml", "rb") as f:
  config = tomllib.load(f)

  if not 'name' in config:
    raise ValueError('Name of extension is not defined')
  else:
    extension_name = config['name']

  if not 'build' in config:
    config['build'] = dict()
  # if no path for a compile script is given, assume the default naming convention
  if not 'path' in config['build']:
    config['build']['path'] = 'compile_' ++ config['name']
    print('Build script not defined. Assuming %s as default location', config['build']['path'])

  if not 'pack' in config:
    raise ValueError('No packing instructions for extension found')

# overwrite config version by cmd argument if given
if arguments['--version']:
  config['build']['version'] = arguments['--version']

# Executed the script asked for by the user.
# Option build compiles the software.
# Option pack creates the path structure, copies the relevant files, and packs the extension .tcz file.
# Publish creates the metadata files like info, list, md5 sum and packs them into a bce archive for sending to the official repositories
#
# If no option is given, assume the user wants to build and pack the extension
if arguments['build']:
  build(config)
elif arguments['pack']:
  pack(config)
elif arguments['publish']:
  publish(config)
else:
  build(config)
  pack(config)
