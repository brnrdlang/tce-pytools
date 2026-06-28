# tce-pytools

a small toolbox for creating tinycore extensions from source.
It will build the code, pack the files, and prepare the needed meta files for publishing the extension.

## Usage

Copy tce-pytools into your project folder. Use it by calling
`python -m tce-pytools`

## Config

tce-pytools expects an 'extension.toml' config file in your project's folder.

For building you also need a program or shell script with the build instructions.
It may take one command line argument for the version to build
(e.g. by checking out that tag in a git submodule for the source code).
The default name would be 'compile_*your_extension_name*'.

## Template files

Some files may depend on values from the config,
e.g. which version of the software was built or the path where the binaries will be installed.
To not have to change these values by hand you can create a template file instead and have tce-pytools substitute values from the config to create the actual file.

Currently this is support in the pack module. If a file is not found, pack will look for a corresponding .template file instead.

The publish module will always create the *your_extension_name*.tcz.info from a .template file, since the file size of the extension has to be created dynamically.
