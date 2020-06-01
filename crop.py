import os
from os import path
import sys

EXTENSION = '.jpeg'

# test if source arg is present
args = sys.argv
if len(args) == 1:
    sys.exit('Aucun dossier source indiqué.')
source = args[1]

# test if source exist
if not path.exists(source):
    sys.exit("Le dossier source n'existe pas.")

# test if source is a dir
if not path.isdir(source):
    sys.exit("Le dossier source n'est pas un dossier.")

# create target directory
target = f'{source}_cropped'
try:
    os.makedirs(target)
except FileExistsError:
    sys.exit(f'Le dossier cible {target} existe déjà !')

# get images in folder
images = []
for (dirpath, directories, files) in os.walk(source):
    for file in files:
        extension = path.splitext(file)[1]
        if extension == EXTENSION:
            images.append(file)

# count images
count = len(images)
if not count:
    sys.exit('Aucune image trouvée.')

# convert images
for index, image in enumerate(images):
    # get source and target paths
    sourcepath = '/'.join([source, image])
    targetpath = '/'.join([target, image])
    # crop image
    subcommand = f"convert '{sourcepath}' -virtual-pixel edge -blur 0x15 -fuzz 15% -trim -format '%wx%h%O' info:"
    command = f"convert '{sourcepath}' -crop `{subcommand}` +repage '{targetpath}'"
    os.system(command)
    print(f'[{index + 1} / {count}] Conversion de {image}.')
